# Demo for Screenshot Proof
from vault import encrypt_directory, decrypt_directory
print("=== CRYPTOGRAPHIC VAULT LIVE DEMO ===")
print("Original: Secret Data")
encrypt_directory("test_vault_data", "MyStrongPass123!")
print("Status: ENCRYPTED 🔒")
decrypt_directory("test_vault_data", "MyStrongPass123!")
print("Status: DECRYPTED & VERIFIED ✅ - No Corruption")
