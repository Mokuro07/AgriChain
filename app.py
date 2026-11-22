"""SimpleAgriChain Web Server & REST API
Menyediakan REST API ketertelusuran rantai pasok pangan organik
sesuai kontrak di docs/architecture.md.
"""

from datetime import datetime
import json
import os
from pathlib import Path
import re
from typing import Any, Dict

from flask import Flask, jsonify, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from blockchain import SimpleAgriChain

BASE_DIR = Path(__file__).resolve().parent
LEDGER_PATH = Path(os.environ.get("AGRICHAIN_LEDGER") or (BASE_DIR / "ledger_data.json"))

app = Flask(
    __name__,
    template_folder=str(BASE_DIR / "templates"),
    static_folder=str(BASE_DIR / "static"),
)
app.secret_key = os.environ.get("AGRICHAIN_SECRET", "agrichain-dev-secret-key")

agrichain = SimpleAgriChain(storage_path=str(LEDGER_PATH))

# --- AKUN & BATAS AKSES ---------------------------------------------------
# admin : boleh mencatat transaksi, menguji tamper, dan mereset buku besar
# user  : hanya membaca (dashboard, lacak batch, buku besar)
# Akun disimpan di users.json supaya pendaftaran baru tetap ada setelah server restart.
USERS_PATH = Path(os.environ.get("AGRICHAIN_USERS") or (BASE_DIR / "users.json"))


def _seed_users() -> Dict[str, Dict[str, str]]:
    """Akun awal: satu admin (operator) dan satu konsumen contoh."""
    return {
        "admin": {"name": "Admin Operasional", "role": "admin", "pw": generate_password_hash("admin123")},
        "user": {"name": "Konsumen", "role": "user", "pw": generate_password_hash("user123")},
    }


def load_users() -> Dict[str, Dict[str, str]]:
    """Baca daftar akun; kalau file belum ada/rusak, buat ulang akun awal."""
    if USERS_PATH.exists():
        try:
            data = json.loads(USERS_PATH.read_text(encoding="utf-8"))
            if isinstance(data, dict) and data:
                return data
        except (OSError, ValueError):
            pass
    users = _seed_users()
    save_users(users)
    return users


def save_users(users: Dict[str, Dict[str, str]]) -> None:
    """Tulis atomic supaya file tidak rusak kalau server mati di tengah proses."""
    tmp = USERS_PATH.with_suffix(".json.tmp")
    tmp.write_text(json.dumps(users, ensure_ascii=False, indent=1), encoding="utf-8")
    tmp.replace(USERS_PATH)

# Endpoint POST yang hanya boleh dipakai admin
ADMIN_ONLY_PATHS = {"/api/block/petani", "/api/block/distributor", "/api/tamper", "/api/reset"}
# logout ikut publik: kalau anonim buka /logout, cukup diarahkan ke halaman masuk
PUBLIC_ENDPOINTS = {"login", "logout", "register", "static", "healthz"}

DATE_REGEX = re.compile(r"^\d{4}-\d{2}-\d{2}$")
USERNAME_RE = re.compile(r"^[a-z0-9_]{3,20}$")


def lan_addresses(port: int) -> list:
    """Alamat IP LAN yang bisa dipakai perangkat lain (HP/laptop) di jaringan yang sama."""
    import socket

    ips = set()
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(("8.8.8.8", 80))
        ips.add(sock.getsockname()[0])
        sock.close()
    except Exception:
        pass
    try:
        for ip in socket.gethostbyname_ex(socket.gethostname())[2]:
            if not ip.startswith("127.") and not ip.startswith("169.254."):
                ips.add(ip)
    except Exception:
        pass
    return [f"http://{ip}:{port}" for ip in sorted(ips)]


def _lan_url():
    """Alamat pertama yang bisa dipakai HP/laptop lain (None kalau tidak ada)."""
    urls = lan_addresses(int(os.environ.get("AGRICHAIN_PORT", "5000")))
    return urls[0] if urls else None


def validate_date(date_str: str) -> bool:
    """Memvalidasi format tanggal YYYY-MM-DD."""
    if not isinstance(date_str, str) or not DATE_REGEX.match(date_str):
        return False
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def get_dict_payload():
    """Mengambil dan memvalidasi bahwa payload request adalah JSON object/dict."""
    raw = request.get_json(silent=True)
    if raw is None and not request.data:
        return {}
    if not isinstance(raw, dict):
        return None
    return raw


# Pastikan file akun sudah ada saat server start (berisi admin + user contoh)
load_users()


@app.before_request
def guard_access():
    """Wajib login; aksi tulis hanya untuk admin."""
    if request.endpoint in PUBLIC_ENDPOINTS:
        return None

    role = session.get("role")
    if not role:
        if request.path.startswith("/api/"):
            return jsonify({"success": False, "error": "Belum login. Silakan login dulu."}), 401
        nxt = request.full_path if request.query_string else request.path
        return redirect(url_for("login", next=nxt.rstrip("?")))

    if request.method != "GET" and request.path in ADMIN_ONLY_PATHS and role != "admin":
        return jsonify({"success": False, "error": "Aksi ini hanya untuk admin."}), 403
    return None


@app.route("/login", methods=["GET", "POST"])
def login():
    """Halaman login. Dua peran: admin (boleh menulis) dan user (hanya baca)."""
    if request.method == "GET":
        if session.get("role"):
            return redirect(url_for("index"))
        return render_template(
            "login.html",
            error=None,
            registered=request.args.get("registered"),
            next_url=request.args.get("next", ""),
            lan_url=_lan_url(),
        )

    username = (request.form.get("username") or "").strip().lower()
    password = request.form.get("password") or ""
    account = load_users().get(username)

    next_url = request.form.get("next", "")

    if not account or not check_password_hash(account["pw"], password):
        return render_template(
            "login.html",
            error="Username atau password salah.",
            registered=None,
            next_url=next_url,
            lan_url=_lan_url(),
        ), 401

    session.clear()
    session["user"] = username
    session["name"] = account["name"]
    session["role"] = account["role"]

    # hanya izinkan tujuan internal (hindari open redirect)
    if next_url.startswith("/") and not next_url.startswith("//"):
        return redirect(next_url)
    return redirect(url_for("index"))


@app.route("/register", methods=["GET", "POST"])
def register():
    """Pendaftaran akun konsumen. Akun baru selalu berperan 'user' (hanya baca)."""
    if request.method == "GET":
        if session.get("role"):
            return redirect(url_for("index"))
        return render_template("register.html", error=None, form={}, lan_url=_lan_url())

    username = (request.form.get("username") or "").strip().lower()
    display_name = (request.form.get("name") or "").strip()
    password = request.form.get("password") or ""
    password2 = request.form.get("password2") or ""
    form = {"username": username, "name": display_name}

    users = load_users()
    error = None
    if not USERNAME_RE.match(username):
        error = "Username 3–20 karakter: huruf kecil, angka, atau garis bawah."
    elif username in users:
        error = "Username itu sudah dipakai. Pilih yang lain."
    elif not display_name:
        error = "Nama tampilan wajib diisi."
    elif len(password) < 8:
        error = "Password minimal 8 karakter."
    elif password != password2:
        error = "Konfirmasi password belum sama."

    if error:
        return render_template("register.html", error=error, form=form, lan_url=_lan_url()), 400

    users[username] = {
        "name": display_name,
        "role": "user",  # pendaftaran mandiri tidak pernah jadi admin
        "pw": generate_password_hash(password),
    }
    save_users(users)
    return redirect(url_for("login", registered=1))


@app.route("/logout")
def logout():
    """Keluar dan hapus sesi."""
    session.clear()
    return redirect(url_for("login"))


@app.route("/healthz")
def healthz():
    """Cek kesiapan server tanpa perlu login (dipakai run-agrichain.bat)."""
    port = int(os.environ.get("AGRICHAIN_PORT", "5000"))
    return jsonify({"ok": True, "blocks": len(agrichain.chain), "lan": lan_addresses(port)}), 200


@app.route("/")
def index():
    """Melayani antarmuka Web SPA sesuai peran pengguna."""
    return render_template(
        "index.html",
        role=session.get("role"),
        name=session.get("name"),
        username=session.get("user"),
        lan_url=_lan_url(),
    )


@app.route("/api/chain", methods=["GET"])
def get_chain():
    """Mengambil seluruh data rantai blok beserta status validitas integritas."""
    is_valid, tampered_indices = agrichain.is_chain_valid()
    chain_list = [block.to_dict() for block in agrichain.chain]
    return (
        jsonify(
            {
                "success": True,
                "is_valid": is_valid,
                "tampered_indices": tampered_indices,
                "total_blocks": len(chain_list),
                "chain": chain_list,
            }
        ),
        200,
    )


@app.route("/api/block/petani", methods=["POST"])
def add_petani_block():
    """Mencatat blok panen baru dari Petani."""
    payload = get_dict_payload()
    if payload is None:
        return (
            jsonify({"success": False, "error": "Payload JSON harus berupa objek dictionary"}),
            400,
        )

    batch_id = str(payload.get("batch_id", "")).strip()
    if not batch_id:
        return (
            jsonify({"success": False, "error": "Field wajib 'batch_id' tidak boleh kosong"}),
            400,
        )

    # Validasi keunikan batch_id: tolak batch_id duplikat oleh Petani
    if any(b.actor == "PETANI" and b.batch_id == batch_id for b in agrichain.chain):
        return (
            jsonify(
                {
                    "success": False,
                    "error": f"Batch ID '{batch_id}' sudah pernah diinisiasi oleh Petani",
                }
            ),
            400,
        )

    komoditas = str(payload.get("komoditas", "")).strip()
    if not komoditas:
        return (
            jsonify({"success": False, "error": "Field wajib 'komoditas' tidak boleh kosong"}),
            400,
        )

    lokasi_lahan = str(payload.get("lokasi_lahan", "")).strip()
    if not lokasi_lahan:
        return (
            jsonify({"success": False, "error": "Field wajib 'lokasi_lahan' tidak boleh kosong"}),
            400,
        )

    tanggal_panen = str(payload.get("tanggal_panen", "")).strip()
    if not validate_date(tanggal_panen):
        return (
            jsonify(
                {
                    "success": False,
                    "error": "Field wajib 'tanggal_panen' harus berformat YYYY-MM-DD valid",
                }
            ),
            400,
        )

    pupuk = str(payload.get("pupuk", "")).strip()
    if not pupuk:
        return (
            jsonify({"success": False, "error": "Field wajib 'pupuk' tidak boleh kosong"}),
            400,
        )

    no_sertifikat = str(payload.get("no_sertifikat", "")).strip()
    if not no_sertifikat:
        return (
            jsonify({"success": False, "error": "Field wajib 'no_sertifikat' tidak boleh kosong"}),
            400,
        )

    kadar_air_raw = payload.get("kadar_air")
    if (
        kadar_air_raw is None
        or isinstance(kadar_air_raw, bool)
        or (isinstance(kadar_air_raw, str) and not kadar_air_raw.strip())
    ):
        return (
            jsonify({"success": False, "error": "Field wajib 'kadar_air' tidak boleh kosong"}),
            400,
        )
    try:
        kadar_air_val = float(kadar_air_raw)
    except (ValueError, TypeError):
        return (
            jsonify({"success": False, "error": "Nilai kadar air harus berupa angka numerik"}),
            400,
        )

    if kadar_air_val < 0.0 or kadar_air_val > 100.0:
        return (
            jsonify(
                {
                    "success": False,
                    "error": "Nilai kadar air harus berada dalam rentang 0.0 s.d. 100.0 %",
                }
            ),
            400,
        )

    data = {
        "komoditas": komoditas,
        "lokasi_lahan": lokasi_lahan,
        "tanggal_panen": tanggal_panen,
        "pupuk": pupuk,
        "no_sertifikat": no_sertifikat,
        "kadar_air": kadar_air_val,
    }

    new_block = agrichain.add_block(batch_id=batch_id, actor="PETANI", data=data)
    return (
        jsonify(
            {
                "success": True,
                "message": "Blok Petani berhasil dicatat dalam blockchain",
                "block": new_block.to_dict(),
            }
        ),
        201,
    )


@app.route("/api/block/distributor", methods=["POST"])
def add_distributor_block():
    """Mencatat blok transit logistik baru dari Distributor."""
    payload = get_dict_payload()
    if payload is None:
        return (
            jsonify({"success": False, "error": "Payload JSON harus berupa objek dictionary"}),
            400,
        )

    batch_id = str(payload.get("batch_id", "")).strip()
    if not batch_id:
        return (
            jsonify({"success": False, "error": "Field wajib 'batch_id' tidak boleh kosong"}),
            400,
        )

    # Validasi keterikatan hulu: tolak batch_id yang belum pernah diinisiasi oleh Petani
    if not any(b.actor == "PETANI" and b.batch_id == batch_id for b in agrichain.chain):
        return (
            jsonify(
                {
                    "success": False,
                    "error": f"Batch ID '{batch_id}' belum diinisiasi oleh Petani",
                }
            ),
            400,
        )

    tanggal_kirim = str(payload.get("tanggal_kirim", "")).strip()
    if not validate_date(tanggal_kirim):
        return (
            jsonify(
                {
                    "success": False,
                    "error": "Field wajib 'tanggal_kirim' harus berformat YYYY-MM-DD valid",
                }
            ),
            400,
        )

    rute = str(payload.get("rute", "")).strip()
    if not rute:
        return (
            jsonify({"success": False, "error": "Field wajib 'rute' tidak boleh kosong"}),
            400,
        )

    suhu_raw = payload.get("suhu")
    if suhu_raw is None or isinstance(suhu_raw, bool):
        return (
            jsonify({"success": False, "error": "Nilai suhu harus berupa angka numerik"}),
            400,
        )
    try:
        suhu_val = float(suhu_raw)
    except (ValueError, TypeError):
        return (
            jsonify({"success": False, "error": "Nilai suhu harus berupa angka numerik"}),
            400,
        )

    if suhu_val < -20.0 or suhu_val > 60.0:
        return (
            jsonify(
                {
                    "success": False,
                    "error": "Nilai suhu harus berada dalam rentang -20.0 s.d. 60.0 °C",
                }
            ),
            400,
        )

    status_kondisi = str(payload.get("status_kondisi", "")).strip()
    if not status_kondisi:
        return (
            jsonify({"success": False, "error": "Field wajib 'status_kondisi' tidak boleh kosong"}),
            400,
        )

    data = {
        "tanggal_kirim": tanggal_kirim,
        "rute": rute,
        "suhu": suhu_val,
        "status_kondisi": status_kondisi,
    }

    new_block = agrichain.add_block(batch_id=batch_id, actor="DISTRIBUTOR", data=data)
    return (
        jsonify(
            {
                "success": True,
                "message": "Blok Distributor berhasil dicatat dalam blockchain",
                "block": new_block.to_dict(),
            }
        ),
        201,
    )


@app.route("/api/trace/<batch_id>", methods=["GET"])
def trace_batch(batch_id: str):
    """Mengambil riwayat penelusuran batch dan peringatan suhu transit."""
    clean_batch_id = str(batch_id).strip()
    trace_result = agrichain.trace_batch(clean_batch_id)

    if not trace_result:
        return (
            jsonify(
                {
                    "success": False,
                    "error": f"Batch ID '{clean_batch_id}' tidak ditemukan dalam buku besar",
                    "batch_id": clean_batch_id,
                    "timeline": [],
                }
            ),
            404,
        )

    return jsonify(trace_result), 200


@app.route("/api/tamper", methods=["POST"])
def tamper_block():
    """Memanipulasi isi data blok untuk demonstrasi perusakan integritas hash."""
    payload = get_dict_payload()
    if payload is None:
        return (
            jsonify({"success": False, "error": "Payload JSON harus berupa objek dictionary"}),
            400,
        )

    block_index = payload.get("block_index")
    modified_data = payload.get("modified_data")

    if (
        block_index is None
        or not isinstance(block_index, int)
        or isinstance(block_index, bool)
        or not isinstance(modified_data, dict)
    ):
        return (
            jsonify(
                {
                    "success": False,
                    "error": "Indeks blok tidak valid atau di luar jangkauan (0 <= index < panjang rantai)",
                }
            ),
            400,
        )

    if block_index < 0 or block_index >= len(agrichain.chain):
        return (
            jsonify(
                {
                    "success": False,
                    "error": "Indeks blok tidak valid atau di luar jangkauan (0 <= index < panjang rantai)",
                }
            ),
            400,
        )

    agrichain.tamper_block(block_index, modified_data)
    is_valid, tampered_indices = agrichain.is_chain_valid()

    message = (
        "PERINGATAN: Integritas rantai rusak! Hash tidak cocok."
        if not is_valid
        else "Rantai valid."
    )

    return (
        jsonify(
            {
                "success": True,
                "message": f"Data blok index {block_index} berhasil dimanipulasi",
                "block_index": block_index,
                "chain_validity": {
                    "is_valid": is_valid,
                    "tampered_indices": tampered_indices,
                    "message": message,
                },
            }
        ),
        200,
    )


@app.route("/api/reset", methods=["POST"])
def reset_chain():
    """Mereset buku besar ke kondisi awal hanya Genesis Block."""
    payload = get_dict_payload()
    if payload is None:
        return (
            jsonify({"success": False, "error": "Payload JSON harus berupa objek dictionary"}),
            400,
        )

    agrichain.reset_chain()
    is_valid, _ = agrichain.is_chain_valid()
    return (
        jsonify(
            {
                "success": True,
                "message": "Buku besar berhasil direset ke Genesis Block",
                "total_blocks": len(agrichain.chain),
                "is_valid": is_valid,
            }
        ),
        200,
    )


if __name__ == "__main__":
    # AGRICHAIN_DEBUG=1 -> auto-reload saat file diubah (enak buat ngoding)
    debug_on = os.environ.get("AGRICHAIN_DEBUG", "0") == "1"
    port = int(os.environ.get("AGRICHAIN_PORT", "5000"))
    # 0.0.0.0 = bisa diakses dari HP/laptop lain di jaringan yang sama
    host = os.environ.get("AGRICHAIN_HOST", "0.0.0.0")

    print("=" * 62)
    print("  AgriChain siap diakses:")
    print(f"  - Komputer ini : http://127.0.0.1:{port}")
    for url in lan_addresses(port):
        print(f"  - Perangkat lain: {url}")
    if not lan_addresses(port):
        print("  - (alamat LAN tidak terdeteksi; sambungkan dulu ke Wi-Fi/hotspot)")
    print("=" * 62, flush=True)

    app.run(host=host, port=port, debug=debug_on)
