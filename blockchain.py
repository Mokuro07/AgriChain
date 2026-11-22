"""SimpleAgriChain Core Engine
Implementasi blockchain permissioned sederhana tanpa PoW (Zero-mining) untuk
ketertelusuran rantai pasok pangan organik.
"""

from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


class Block:
    """Representasi satu blok pada rantai SimpleAgriChain."""

    def __init__(
        self,
        index: int,
        batch_id: str,
        actor: str,
        data: Dict[str, Any],
        previous_hash: str,
        timestamp: Optional[str] = None,
        current_hash: Optional[str] = None,
    ) -> None:
        self.index: int = index
        self.timestamp: str = timestamp or datetime.now(timezone.utc).isoformat()
        self.batch_id: str = batch_id
        self.actor: str = actor
        self.data: Dict[str, Any] = data
        self.previous_hash: str = previous_hash
        self.current_hash: str = current_hash or self.compute_hash()

    def compute_hash(self) -> str:
        """Menghitung SHA-256 kanonikal (sort_keys=True, tanpa spasi ekstra)."""
        block_dict = {
            "index": self.index,
            "timestamp": self.timestamp,
            "batch_id": self.batch_id,
            "actor": self.actor,
            "data": self.data,
            "previous_hash": self.previous_hash,
        }
        block_string = json.dumps(block_dict, sort_keys=True, separators=(",", ":"))
        return hashlib.sha256(block_string.encode("utf-8")).hexdigest()

    def to_dict(self) -> Dict[str, Any]:
        """Konversi blok ke dictionary 7 field wajib."""
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "batch_id": self.batch_id,
            "actor": self.actor,
            "data": self.data,
            "previous_hash": self.previous_hash,
            "current_hash": self.current_hash,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Block":
        """Instansiasi blok dari dictionary persistence."""
        return cls(
            index=data["index"],
            batch_id=data["batch_id"],
            actor=data["actor"],
            data=data["data"],
            previous_hash=data["previous_hash"],
            timestamp=data.get("timestamp"),
            current_hash=data.get("current_hash"),
        )


class SimpleAgriChain:
    """Pengelola rantai pasok pangan terdesentralisasi internal."""

    def __init__(self, storage_path: str = "ledger_data.json") -> None:
        self.storage_path = Path(storage_path)
        self.chain: List[Block] = []
        self.load_chain()

    def create_genesis_block(self) -> Block:
        """Membentuk Genesis Block (Index 0)."""
        genesis = Block(
            index=0,
            batch_id="GENESIS",
            actor="SYSTEM",
            data={
                "message": "Genesis Block SimpleAgriChain",
                "version": "1.0.0",
            },
            previous_hash="0",
            timestamp="2026-11-08T10:00:00.000000Z",
        )
        return genesis

    def load_chain(self) -> None:
        """Membaca chain dari ledger_data.json atau inisialisasi baru bila corrupt/hilang."""
        if self.storage_path.exists():
            try:
                with open(self.storage_path, "r", encoding="utf-8") as f:
                    raw_data = json.load(f)
                if isinstance(raw_data, list) and len(raw_data) > 0:
                    self.chain = [Block.from_dict(item) for item in raw_data]
                    return
            except Exception:
                # Corrupted or unreadable file -> fallback ke Genesis baru
                pass

        # Inisialisasi rantai baru bila file tidak ada atau rusak
        genesis = self.create_genesis_block()
        self.chain = [genesis]
        self.save_chain()

    def save_chain(self) -> None:
        """Menyimpan seluruh rantai blok ke file ledger secara atomik."""
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        temp_path = self.storage_path.with_suffix(".tmp")
        payload = [block.to_dict() for block in self.chain]

        with open(temp_path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2, ensure_ascii=False)

        # Atomic replace
        temp_path.replace(self.storage_path)

    def add_block(self, batch_id: str, actor: str, data: Dict[str, Any]) -> Block:
        """Menambahkan blok baru yang mengikat hash blok sebelumnya."""
        previous_block = self.chain[-1]
        new_index = len(self.chain)
        new_block = Block(
            index=new_index,
            batch_id=batch_id,
            actor=actor,
            data=data,
            previous_hash=previous_block.current_hash,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )
        self.chain.append(new_block)
        self.save_chain()
        return new_block

    def is_chain_valid(self) -> Tuple[bool, List[int]]:
        """Memverifikasi integritas seluruh rantai.

        Mengembalikan (is_valid: bool, tampered_indices: list[int]).
        """
        tampered_indices: List[int] = []
        if not self.chain:
            return False, []

        # Validasi Genesis Block
        genesis = self.chain[0]
        if genesis.previous_hash != "0" or genesis.current_hash != genesis.compute_hash():
            tampered_indices.append(0)

        # Validasi blok selanjutnya
        for i in range(1, len(self.chain)):
            curr = self.chain[i]
            prev = self.chain[i - 1]

            has_error = False
            if curr.previous_hash != prev.current_hash:
                has_error = True
            if curr.current_hash != curr.compute_hash():
                has_error = True

            if has_error and i not in tampered_indices:
                tampered_indices.append(i)

        return len(tampered_indices) == 0, tampered_indices

    def trace_batch(self, batch_id: str) -> Optional[Dict[str, Any]]:
        """Mengambil rekaman penelusuran hulu-ke-hilir untuk batch_id tertentu."""
        matching_blocks = [b for b in self.chain if b.batch_id == batch_id]
        if not matching_blocks:
            return None

        timeline = []
        has_temp_alert = False
        max_temp: Optional[float] = None
        has_moisture_alert = False
        max_moisture: Optional[float] = None
        cert_valid = False
        no_cert = ""

        for step_idx, block in enumerate(matching_blocks, start=1):
            item: Dict[str, Any] = {
                "step": step_idx,
                "index": block.index,
                "actor": block.actor,
                "timestamp": block.timestamp,
                "data": block.data,
                "current_hash": block.current_hash,
            }

            if block.actor == "PETANI":
                cert = str(block.data.get("no_sertifikat", "")).strip()
                if cert:
                    cert_valid = True
                    no_cert = cert

                kadar_air_raw = block.data.get("kadar_air")
                moisture_alert = False
                try:
                    if kadar_air_raw is not None and not isinstance(kadar_air_raw, bool):
                        kadar_air_val = float(kadar_air_raw)
                        if max_moisture is None or kadar_air_val > max_moisture:
                            max_moisture = kadar_air_val
                        if kadar_air_val > 14.0:
                            moisture_alert = True
                            has_moisture_alert = True
                except (ValueError, TypeError):
                    moisture_alert = False
                item["moisture_alert"] = moisture_alert

            elif block.actor == "DISTRIBUTOR":
                suhu_raw = block.data.get("suhu")
                try:
                    suhu_val = float(suhu_raw)
                    if max_temp is None or suhu_val > max_temp:
                        max_temp = suhu_val
                    is_alert = suhu_val > 25.0
                    item["temperature_alert"] = is_alert
                    if is_alert:
                        has_temp_alert = True
                except (ValueError, TypeError):
                    item["temperature_alert"] = False

            timeline.append(item)

        has_quality_risk = bool(has_temp_alert or has_moisture_alert)
        risk_sources: List[str] = []
        if has_moisture_alert:
            risk_sources.append("PETANI")
        if has_temp_alert:
            risk_sources.append("DISTRIBUTOR")

        return {
            "success": True,
            "batch_id": batch_id,
            "total_records": len(timeline),
            "has_temperature_alert": has_temp_alert,
            "max_temperature": max_temp,
            "temperature_threshold": 25.0,
            "has_moisture_alert": has_moisture_alert,
            "kadar_air_max": max_moisture,
            "moisture_threshold": 14.0,
            "has_quality_risk": has_quality_risk,
            "risk_sources": risk_sources,
            "certificate_valid": cert_valid,
            "no_sertifikat": no_cert,
            "timeline": timeline,
        }

    def tamper_block(self, block_index: int, modified_data: Dict[str, Any]) -> bool:
        """Memanipulasi payload data pada blok tertentu tanpa memperbarui hash (simulasi serangan)."""
        if block_index < 0 or block_index >= len(self.chain):
            return False

        self.chain[block_index].data = modified_data
        self.save_chain()
        return True

    def reset_chain(self) -> None:
        """Mereset buku besar ke kondisi awal hanya Genesis Block."""
        genesis = self.create_genesis_block()
        self.chain = [genesis]
        self.save_chain()
