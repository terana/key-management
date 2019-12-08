from Crypto.Cipher import Salsa20


def encrypt(secret, key, prime=128):
    key = key.to_bytes(prime // 8, 'big')
    secret = bytearray(secret, 'utf-8')
    cipher = Salsa20.new(key=key)
    return cipher.nonce + cipher.encrypt(secret)


def decrypt(message, key, prime=128):
    key = key.to_bytes(prime // 8, 'big')
    nonce, cipher_text = message[:8], message[8:]
    cipher = Salsa20.new(key=key, nonce=nonce)
    return cipher.decrypt(cipher_text).decode('utf-8')
