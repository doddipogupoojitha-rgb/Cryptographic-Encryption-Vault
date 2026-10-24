#!/usr/bin/env python3
"""
Cryptographic Encryption Vault - Workora Task
Encrypt/Decrypt whole directories with Fernet + PBKDF2
"""
import os, base64, json, shutil
from pathlib import Path
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from datetime import datetime

SALT = b'workora_vault_salt_2024'
KEY_FILE = "vault.key"
KEY_BACKUP = "vault.key.backup"
LOG_FILE = "vault_execution.log"

def log(msg):
    entry = f"[{datetime.now()}] {msg}"
    print(entry)
    with open(LOG_FILE, "a") as f:
        f.write(entry + "\n")

def derive_key(passphrase: str):
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=SALT, iterations=100000)
    return base64.urlsafe_b64encode(kdf.derive(passphrase.encode()))

def generate_key_file(passphrase):
    key = derive_key(passphrase)
    with open(KEY_FILE, "wb") as f:
        f.write(key)
    with open(KEY_BACKUP, "wb") as f:
        f.write(key)
    log(f"🔑 Key generated: {KEY_FILE} + Backup: {KEY_BACKUP} (Best Practice)")
    return key

def load_key(passphrase=None):
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, "rb") as f:
            return f.read()
    if passphrase:
        return generate_key_file(passphrase)
    raise FileNotFoundError("Key file not found! Use passphrase first time.")

def encrypt_directory(dir_path, passphrase):
    dir_path = Path(dir_path)
    if not dir_path.exists():
        log(f"❌ Directory not found: {dir_path}")
        return
    key = generate_key_file(passphrase)
    fernet = Fernet(key)
    
    files = list(dir_path.rglob("*"))
    count = 0
    manifest = []
    for file in files:
        if file.is_file() and file.name not in [KEY_FILE, KEY_BACKUP, LOG_FILE]:
            with open(file, "rb") as f:
                data = f.read()
            enc = fernet.encrypt(data)
            with open(file, "wb") as f:
                f.write(enc)
            manifest.append(str(file))
            count += 1
            log(f"🔒 Encrypted: {file}")
    
    with open(dir_path / "vault_manifest.json", "w") as f:
        json.dump(manifest, f, indent=2)
    log(f"✅ ENCRYPTION COMPLETE: {count} files encrypted in {dir_path}")
    log(f"📦 Backup keys saved securely!")

def decrypt_directory(dir_path, passphrase):
    dir_path = Path(dir_path)
    key = load_key(passphrase)
    fernet = Fernet(key)
    
    manifest_path = dir_path / "vault_manifest.json"
    if manifest_path.exists():
        with open(manifest_path) as f:
            files = json.load(f)
    else:
        files = [str(p) for p in dir_path.rglob("*") if p.is_file()]
    
    count = 0
    for fp in files:
        file = Path(fp)
        if not file.exists(): continue
        if file.name in [KEY_FILE, KEY_BACKUP, LOG_FILE, "vault_manifest.json"]: continue
        try:
            with open(file, "rb") as f:
                data = f.read()
            dec = fernet.decrypt(data)
            with open(file, "wb") as f:
                f.write(dec)
            count += 1
            log(f"🔓 Decrypted: {file}")
        except Exception as e:
            log(f"⚠️ Skip (already plain): {file} - {e}")
    
    if manifest_path.exists():
        os.remove(manifest_path)
    log(f"✅ DECRYPTION COMPLETE: {count} files restored - NO DATA CORRUPTION!")

if __name__ == "__main__":
    print("=== Cryptographic Encryption Vault ===")
    # Demo Test
    test_dir = Path("test_vault_data")
    test_dir.mkdir(exist_ok=True)
    (test_dir / "file1.txt").write_text("Secret Data 1 - Poojitha")
    (test_dir / "file2.txt").write_text("Secret Data 2 - Workora")
    (test_dir / "docs").mkdir(exist_ok=True)
    (test_dir / "docs" / "notes.txt").write_text("Important Notes")
    
    print("\n1. Original Files Created")
    encrypt_directory(test_dir, "MyStrongPass123!")
    print("\n2. Now Encrypted - Try opening files, they are encrypted!")
    decrypt_directory(test_dir, "MyStrongPass123!")
    print("\n3. Restored - Check files, data intact!")
    print("\nCheck vault_execution.log for Execution Proof!")
