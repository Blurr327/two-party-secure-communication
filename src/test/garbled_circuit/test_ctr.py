import pytest
from Crypto.Random import get_random_bytes
from garbled_circuit.ctr import encrypt_ctr, decrypt_ctr, BIT_BLOCK_SIZE

# Test basic encryption and decryption
def test_ctr_encrypt_decrypt():
    key = 0xABCD1234EF567890ABCD1234EF567890
    nonce = 230
    message = 1 << BIT_BLOCK_SIZE

    ciphertext = encrypt_ctr(key, message, nonce)
    decrypted = decrypt_ctr(key, ciphertext, nonce)

    assert decrypted == message, "Decryption failed!"

# Test symmetry property
def test_ctr_symmetry():
    key = 0xABCD1234EF567890ABCD1234EF567890
    nonce = 12345
    message = 0xABCD1234EF567890

    ciphertext = encrypt_ctr(key, message, nonce)
    decrypted = encrypt_ctr(key, ciphertext, nonce)

    assert decrypted == message, "CTR encryption should be reversible!"

# Test counter incrementation
def test_ctr_counter_increment():
    key = 0xABCD1234EF567890ABCD1234EF567890
    nonce = 100
    message = 0x1234567890ABCDEF

    ciphertext1 = encrypt_ctr(key, message, nonce)
    ciphertext2 = encrypt_ctr(key, message, nonce + 1)

    assert ciphertext1 != ciphertext2, "Different nonces should produce different ciphertexts!"

# Test different message sizes
def test_ctr_variable_lengths():
    key = 0xABCD1234EF567890ABCD1234EF567890
    nonce = 42

    for length in [(BIT_BLOCK_SIZE // 2)*i for i in range(1, 6)]:
        message = int.from_bytes(get_random_bytes(length), "big")
        ciphertext = encrypt_ctr(key, message, nonce)
        decrypted = decrypt_ctr(key, ciphertext, nonce)

        assert decrypted == message, f"Failed for message length {length} bits"

# Test reproducibility
def test_ctr_reproducibility():
    key = 0xABCD1234EF567890ABCD1234EF567890
    nonce = 77
    message = 0xDEADBEEFCAFEBABE

    ciphertext1 = encrypt_ctr(key, message, nonce)
    ciphertext2 = encrypt_ctr(key, message, nonce)

    assert ciphertext1 == ciphertext2, "Same input should produce the same ciphertext!"

# Test keystream uniqueness
def test_keystream_uniqueness():
    key = 0xABCD1234EF567890ABCD1234EF567890
    nonce1 = 555
    nonce2 = 556  # Different nonce
    message = 0xFEEDFACE

    ciphertext1 = encrypt_ctr(key, message, nonce1)
    ciphertext2 = encrypt_ctr(key, message, nonce2)

    assert ciphertext1 != ciphertext2, "Different nonces should result in different ciphertexts!"

if __name__ == "__main__":
    pytest.main()
