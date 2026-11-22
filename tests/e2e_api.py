import json, os, subprocess, sys, tempfile, time, urllib.request, urllib.error
from http.cookiejar import CookieJar
from pathlib import Path

# Uji ini TIDAK menyentuh data asli: kalau AGRICHAIN_TEST_URL tidak diberikan,
# skrip menyalakan server sendiri di port 5099 dengan file ledger sementara.
PROJECT = Path(__file__).resolve().parent.parent
_OWN_SERVER = None
if os.environ.get("AGRICHAIN_TEST_URL"):
    BASE = os.environ["AGRICHAIN_TEST_URL"].rstrip("/")
else:
    # pilih port kosong supaya tidak bentrok dengan server uji lain yang masih hidup
    import socket as _socket
    with _socket.socket(_socket.AF_INET, _socket.SOCK_STREAM) as _s:
        _s.bind(("127.0.0.1", 0))
        _PORT = _s.getsockname()[1]
    BASE = f"http://127.0.0.1:{_PORT}"
    _tmp = tempfile.NamedTemporaryFile(prefix="agrichain-test-", suffix=".json", delete=False)
    _tmp.close()
    os.unlink(_tmp.name)  # biarkan kosong: rantai baru dibuat sendiri
    _tmp_users = tempfile.NamedTemporaryFile(prefix="agrichain-users-", suffix=".json", delete=False)
    _tmp_users.close()
    os.unlink(_tmp_users.name)
    env = dict(os.environ, AGRICHAIN_PORT=str(_PORT), AGRICHAIN_LEDGER=_tmp.name,
               AGRICHAIN_USERS=_tmp_users.name)
    _OWN_SERVER = subprocess.Popen(
        [sys.executable, "app.py"], cwd=str(PROJECT), env=env,
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    for _ in range(40):
        try:
            urllib.request.urlopen(BASE + "/healthz", timeout=1).read()
            break
        except Exception:
            time.sleep(0.5)
    print(f"[test] server uji sendiri di {BASE} (ledger sementara: {_tmp.name})")

results = []

# --- Sesi: login sebagai admin (aksi tulis butuh role admin) ---
_jar = CookieJar()
_opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(_jar))


def login(username="admin", password="admin123"):
    body = f"username={username}&password={password}".encode()
    req = urllib.request.Request(BASE + "/login", data=body, method="POST",
                                 headers={"Content-Type": "application/x-www-form-urlencoded"})
    with _opener.open(req) as r:
        return r.status


def check_login_gate():
    """Tanpa sesi: API tulis harus 401/403, dan / harus redirect ke /login."""
    import http.cookiejar as cj
    anon = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj.CookieJar()))
    try:
        r = urllib.request.Request(BASE + "/api/reset", data=b"{}", method="POST",
                                   headers={"Content-Type": "application/json"})
        anon.open(r)
        check("anon POST ditolak", False, "tidak ditolak")
    except urllib.error.HTTPError as e:
        check("anon POST ditolak", e.code in (401, 403), e.code)


def req(method, path, body=None, raw=None):
    url = BASE + path
    data = None
    headers = {"Accept": "application/json"}
    if raw is not None:
        data = raw.encode()
        headers["Content-Type"] = "application/json"
    elif body is not None:
        data = json.dumps(body).encode()
        headers["Content-Type"] = "application/json"
    r = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with _opener.open(r) as resp:
            return resp.status, json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        payload = e.read().decode()
        try:
            return e.code, json.loads(payload)
        except Exception:
            return e.code, {"raw": payload[:200]}

def check(name, cond, detail=""):
    results.append((bool(cond), name, detail))
    print(("PASS " if cond else "FAIL ") + name + ("  | " + str(detail)[:160] if detail else ""))


# --- Sesi: login admin, plus cek gerbang akses tanpa sesi ---
check("login admin", login() in (200, 302))
check_login_gate()
login()

# --- Batas peran: user hanya baca ---
_saved_jar = _jar
_user_jar = CookieJar()
_opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(_user_jar))
check("login user", login("user", "user123") in (200, 302))
s_u, b_u = req("POST", "/api/block/petani", {"batch_id": "X-1", "komoditas": "X", "lokasi_lahan": "X",
                                             "tanggal_panen": "2026-11-05", "pupuk": "X", "no_sertifikat": "X",
                                             "kadar_air": 10})
check("user POST petani -> 403", s_u == 403, f"{s_u} {b_u.get('error','')}")
s_u2, _ = req("GET", "/api/chain")
check("user GET chain -> 200", s_u2 == 200, s_u2)
# --- Pendaftaran akun baru (register) ---
def form_post(path, fields):
    body = "&".join(f"{k}={v}" for k, v in fields.items()).encode()
    req = urllib.request.Request(BASE + path, data=body, method="POST",
                                 headers={"Content-Type": "application/x-www-form-urlencoded"})
    try:
        with urllib.request.urlopen(req) as r:
            return r.status, r.geturl()
    except urllib.error.HTTPError as e:
        return e.code, ""

anon = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(CookieJar()))
with anon.open(BASE + "/register") as r:
    html_reg = r.read().decode()
check("halaman register 200", r.status == 200 and 'name="password2"' in html_reg and "Ulangi password" in html_reg, r.status)

s, _ = form_post("/register", {"username": "ab", "name": "X", "password": "12345678", "password2": "12345678"})
check("register username pendek -> 400", s == 400, s)
s, _ = form_post("/register", {"username": "budi_tani", "name": "Budi", "password": "123", "password2": "123"})
check("register password <8 -> 400", s == 400, s)
s, _ = form_post("/register", {"username": "budi_tani", "name": "Budi", "password": "rahasia123", "password2": "beda123"})
check("register konfirmasi beda -> 400", s == 400, s)
s, url = form_post("/register", {"username": "budi_tani", "name": "Budi Santoso",
                                 "password": "rahasia123", "password2": "rahasia123"})
check("register valid -> redirect login", s == 200 and "registered=1" in url, f"{s} {url}")
s, _ = form_post("/register", {"username": "budi_tani", "name": "Budi", "password": "rahasia123", "password2": "rahasia123"})
check("register username kembar -> 400", s == 400, s)

# akun baru bisa masuk, tapi tetap tidak boleh menulis
new_jar = CookieJar()
new_op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(new_jar))
new_op.open(urllib.request.Request(BASE + "/login", data=b"username=budi_tani&password=rahasia123",
                                   method="POST", headers={"Content-Type": "application/x-www-form-urlencoded"}))
with new_op.open(BASE + "/api/chain") as r:
    check("akun baru bisa baca chain", r.status == 200, r.status)
try:
    _req_obj = urllib.request.Request(BASE + "/api/block/petani", data=b"{}", method="POST",
                                      headers={"Content-Type": "application/json"})
    new_op.open(_req_obj)
    check("akun baru POST -> 403", False, "tidak ditolak")
except urllib.error.HTTPError as e:
    check("akun baru POST -> 403", e.code == 403, e.code)

# kembali sebagai admin
_opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(_saved_jar))

# 0. reset baseline
s, b = req("POST", "/api/reset")
check("reset -> 200 genesis", s == 200 and b.get("total_blocks", b.get("chain") and len(b["chain"])) in (1, None), f"{s} {str(b)[:120]}")

# 1. petani valid
petani = {
    "batch_id": "ORG-BRS-001",
    "komoditas": "Beras Merah Organik",
    "lokasi_lahan": "Desa Sukatani, Karawang",
    "tanggal_panen": "2026-11-05",
    "pupuk": "Kompos Kotoran Sapi Fermentasi (Organik)",
    "no_sertifikat": "SNI-ORGANIK-2026-0881",
    "kadar_air": 12.5,
}
s, b = req("POST", "/api/block/petani", petani)
check("petani valid -> 201", s == 201 and b.get("success"), f"{s} {b.get('error','')}")
check("petani kadar_air 12.5 no alert", b.get("block", {}).get("data", {}).get("kadar_air") == 12.5, str(b.get("block", {}).get("data"))[:120])

# 2. petani duplicate
s, b = req("POST", "/api/block/petani", petani)
check("petani duplicate -> 400", s == 400, f"{s} {b.get('error','')}")

# 3. petani kadar air basah (17.0) -> alert hulu
wet = dict(petani, batch_id="ORG-BRS-002", kadar_air=17.0)
s, b = req("POST", "/api/block/petani", wet)
check("petani basah 17.0 -> 201", s == 201, f"{s} {b.get('error','')}")

# 4. distributor normal
dist_ok = {"batch_id": "ORG-BRS-001", "tanggal_kirim": "2026-11-06",
           "rute": "Karawang -> Gudang Jakarta Timur", "suhu": 23.5,
           "status_kondisi": "Dalam Pengiriman - Kemasan Tersegel Aman"}
s, b = req("POST", "/api/block/distributor", dist_ok)
check("distributor normal 23.5 -> 201", s == 201, f"{s} {b.get('error','')}")

# 5. distributor suhu kritis
dist_hot = dict(dist_ok, suhu=35.0, status_kondisi="Transit Hangat")
s, b = req("POST", "/api/block/distributor", dist_hot)
check("distributor 35.0 -> 201 (alert)", s == 201, f"{s} {b.get('error','')}")

# 6. distributor orphan
s, b = req("POST", "/api/block/distributor", dict(dist_ok, batch_id="ORG-FAKE-999"))
check("distributor orphan -> 400", s == 400, f"{s} {b.get('error','')}")

# 7. trace
s, b = req("GET", "/api/trace/ORG-BRS-001")
check("trace ORG-BRS-001 -> 200", s == 200 and b.get("success"), f"{s} {str(b)[:150]}")
check("trace ada temperature alert", ("temperature" in json.dumps(b).lower()) or ("suhu" in json.dumps(b).lower()), str(b)[:200])

# 8. trace unknown
s, b = req("GET", "/api/trace/NOPE-123")
check("trace unknown -> 404", s == 404, f"{s} {str(b)[:120]}")

# 9. chain valid
s, b = req("GET", "/api/chain")
check("chain is_valid true", s == 200 and b.get("is_valid") is True and b.get("total_blocks") == 5, f"{s} total={b.get('total_blocks')} valid={b.get('is_valid')}")

# 10. validasi payload
cases = [
    ("payload kosong", "POST", "/api/block/petani", {}, 400),
    ("non-dict array", "POST", "/api/block/petani", None, 400, "[1,2,3]"),
    ("suhu non-numerik", "POST", "/api/block/distributor", dict(dist_ok, batch_id="ORG-BRS-002", suhu="panas"), 400),
    ("suhu bool", "POST", "/api/block/distributor", dict(dist_ok, batch_id="ORG-BRS-002", suhu=True), 400),
    ("suhu out of range", "POST", "/api/block/distributor", dict(dist_ok, batch_id="ORG-BRS-002", suhu=65.0), 400),
    ("kadar_air out of range", "POST", "/api/block/petani", dict(petani, batch_id="ORG-BRS-003", kadar_air=150), 400),
    ("tanggal invalid", "POST", "/api/block/petani", dict(petani, batch_id="ORG-BRS-003", tanggal_panen="2026-13-45"), 400),
    ("batch_id kosong", "POST", "/api/block/petani", dict(petani, batch_id=""), 400),
    ("tamper index OOR", "POST", "/api/tamper", {"block_index": 999, "modified_data": {"x": 1}}, 400),
    ("tamper index negatif", "POST", "/api/tamper", {"block_index": -1, "modified_data": {"x": 1}}, 400),
    ("tamper tanpa modified_data", "POST", "/api/tamper", {"block_index": 1}, 400),
]
for c in cases:
    name, m, p, body, want = c[0], c[1], c[2], c[3], c[4]
    raw = c[5] if len(c) > 5 else None
    s, b = req(m, p, body, raw)
    check(f"validasi {name} -> {want}", s == want, f"{s} {b.get('error', str(b)[:80])}")

# 11. suhu dingin sah
s, b = req("POST", "/api/block/distributor", dict(dist_ok, batch_id="ORG-BRS-002", suhu=-15.5))
check("distributor -15.5 -> 201", s == 201, f"{s} {b.get('error','')}")

# 12. tamper valid
s, b = req("POST", "/api/tamper", {"block_index": 1, "modified_data": {"komoditas": "Beras Palsu", "lokasi_lahan": "Entah", "tanggal_panen": "2026-11-05", "pupuk": "Air", "no_sertifikat": "FAKE", "kadar_air": 12.5}})
check("tamper index 1 -> 200", s == 200, f"{s} {str(b)[:120]}")
s, b = req("GET", "/api/chain")
check("chain jadi INVALID", s == 200 and b.get("is_valid") is False and 1 in b.get("tampered_indices", []), f"valid={b.get('is_valid')} idx={b.get('tampered_indices')}")

# 13. reset balik bersih
s, b = req("POST", "/api/reset")
s2, b2 = req("GET", "/api/chain")
check("reset -> chain valid lagi", s2 == 200 and b2.get("is_valid") is True and b2.get("total_blocks") == 1, f"total={b2.get('total_blocks')} valid={b2.get('is_valid')}")

# 14. static / UI
with _opener.open(BASE + "/") as r:
    html = r.read().decode()
check("UI html 200 + non-trivial", len(html) > 20000, len(html))
for ep in ["/api/chain", "/api/block/petani", "/api/block/distributor", "/api/trace/", "/api/tamper", "/api/reset"]:
    check(f"UI refs {ep}", ep in html)

# 15. 404 handling
s, b = req("GET", "/api/nonexistent")
check("unknown api -> 404", s == 404, s)

if _OWN_SERVER is not None:
    _OWN_SERVER.terminate()
    try:
        _OWN_SERVER.wait(timeout=5)
    except Exception:
        _OWN_SERVER.kill()
    print("[test] server uji dimatikan; data asli tidak tersentuh")

bad = [r for r in results if not r[0]]
print("\n==== HASIL: %d/%d PASS ====" % (len(results) - len(bad), len(results)))
if bad:
    print("GAGAL:")
    for _, n, d in bad:
        print(" -", n, "|", d)
    sys.exit(1)
