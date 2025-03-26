from Crypto.Cipher import AES
from math import ceil
import sys

BIT_BLOCK_SIZE = 128
BLOCK_BIT_MASK = (1 << BIT_BLOCK_SIZE) - 1 # = 1111...1 BLOCK_SIZE number of times

def encrypt_ctr(key: bytes, message: int, nonce: int):
  """
  Uses the AES cipher to encrypt/decrypt(for CTR they are the same algorithm) 128 bit blocks
  according to the CTR (counter) mode of operation
  """
  cipher = AES.new(key, AES.MODE_ECB)
  number_of_blocks_in_message = ceil(message.bit_length()/BIT_BLOCK_SIZE)
  ciphertext = 0
  for i in range(1, number_of_blocks_in_message + 1):
    message_block = message & BLOCK_BIT_MASK # message = [BLOCK]...[NEXT_BLOCK_TO_TREAT]

    # Encrypting the shifted nonce with the AES function (with byte <--> int conversions)
    shifted_nonce: bytes = (nonce + i).to_bytes(16, sys.byteorder)
    mask_for_encryption_byte_format = cipher.encrypt(shifted_nonce)
    mask_for_encryption: int = int.from_bytes(mask_for_encryption_byte_format, sys.byteorder)

    ciphertext_block = mask_for_encryption ^ message_block
    ciphertext |= (ciphertext_block << BIT_BLOCK_SIZE*(i-1)) # Adding the block to the front : 0000...[ADDED_BLOCK][BLOCK][BLOCK]...[BLOCK]

    message >>= BIT_BLOCK_SIZE # [BLOCK]...[NEXT_BLOCK][TREATED_BLOCK] -> [BLOCK]...[NEXT_BLOCK]
  return ciphertext

def decrypt_ctr(key: bytes, message: int, nonce: int):
  """
  for CTR, decryption is the same algorithm as encryption. Also, the separation can be useful if we ever want
  to verify that the cipher blocks haven't been tampered with.
  """
  return encrypt_ctr(key, message, nonce)