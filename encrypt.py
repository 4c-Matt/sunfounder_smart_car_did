# HANDLES ALL ENCRYPTION AND DECRYPTION #

# { the dreamer's hotel } #

def new_key():
    from Crypto.Random import get_random_bytes
    key = get_random_bytes(16)
    return key

def encrypt(raw_data, key):

    from Crypto.Cipher import AES

    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(raw_data)

    encrypted_data = cipher.nonce, tag, ciphertext

    return encrypted_data

def decrypt(encrypted_data, key):
    from Crypto.Cipher import AES

    nonce = encrypted_data[0]
    tag = encrypted_data[1]
    ciphertext = encrypted_data[2]
     
    cipher = AES.new(key, AES.MODE_EAX, nonce)
    decrypted_data = cipher.decrypt_and_verify(ciphertext, tag)
    
    return decrypted_data

key = new_key()
print "\nThe key used for encryption is = ", key

raw_data = "hello world"
print "\nData to be encrypted = ", raw_data

encrypted_data = encrypt(raw_data, key)
print "\nEncrypted Data = ", encrypted_data

decrypted_data = decrypt(encrypted_data, key)
print "\nData decrypted = ", decrypted_data
