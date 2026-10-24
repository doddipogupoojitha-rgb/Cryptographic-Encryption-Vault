# Cryptographic Encryption Vault 🔐📦

Secure multi-file directory encryption with key backup best practices.

## Objective
Build multi-file directory encryption tool with key management

## Features Implemented
1. ✅ Recursively scan directory files
2. ✅ AES-GCM alternative Fernet (AES-128-CBC + HMAC) with PBKDF2
3. ✅ Master passphrase -> Secure key derivation
4. ✅ Key file backup: vault.key + vault.key.backup
5. ✅ Full encrypt/decrypt without data corruption

## How to Run - Execution Log Proof

pip install -r requirements.txt
python vault.py

Output:
[2024] 🔑 Key generated: vault.key + Backup: vault.key.backup
[2024] 🔒 Encrypted: test_vault_data/file1.txt
[2024] ✅ ENCRYPTION COMPLETE: 3 files
[2024] 🔓 Decrypted: test_vault_data/file1.txt
[2024] ✅ DECRYPTION COMPLETE: 3 files restored

## Submission Proof Files
- vault.py - Main vault script
- vault_execution.log - Execution log screenshot
- vault.key / vault.key.backup - Key backup proof

## Security Best Practices
- PBKDF2HMAC 100k iterations
- Salted key derivation
- Key backup generation
- Manifest tracking
- No data loss verification

Intern: Doddipogu Poojitha | Workora
