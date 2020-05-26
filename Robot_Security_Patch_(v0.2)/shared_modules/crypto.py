###################################################################
# crypto

# HANDLES ALL ENCRYPTION AND DECRYPTION #

# Utilises PyCryptodome:  https://github.com/Legrandin/pycryptodome

###################################################################

#RSA - Asymmetric Key Encryption for session key


def keypair():
    # Generates public and private RSA keys
    from Crypto.PublicKey import RSA

    key = RSA.generate(2048)

    private_key = key.export_key()
    public_key = key.publickey().export_key()

    return private_key, public_key


def generate_session_key():
    from Crypto.Random import get_random_bytes
    key = get_random_bytes(16)
    return key


def session_key_encrypt(recipient_key, session_key):
    
    from Crypto.PublicKey import RSA
    from Crypto.Cipher import AES, PKCS1_OAEP

    #Encrypt the session key with the public RSA key
    cipher_rsa = PKCS1_OAEP.new(RSA.import_key(recipient_key))
    enc_session_key = cipher_rsa.encrypt(session_key)

    return enc_session_key


def session_key_decrypt(private_key, encrypted_session_key):
    
    from Crypto.PublicKey import RSA
    from Crypto.Cipher import AES, PKCS1_OAEP

    # Decrypt the session key with the private RSA key
    cipher_rsa = PKCS1_OAEP.new(RSA.import_key(private_key))
    session_key = cipher_rsa.decrypt(encrypted_session_key)

    return session_key

###################################################################

# AES - Symmetric key encryption for robot movement commands

def AES_encrypt(raw_data, key):

    from Crypto.Cipher import AES

    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(raw_data)

    encrypted_data = cipher.nonce, tag, ciphertext

    return encrypted_data

def AES_decrypt(encrypted_data, key):
    from Crypto.Cipher import AES

    nonce = encrypted_data[0]
    tag = encrypted_data[1]
    ciphertext = encrypted_data[2]
     
    cipher = AES.new(key, AES.MODE_EAX, nonce)
    decrypted_data = cipher.decrypt_and_verify(ciphertext, tag)
    
    return decrypted_data

###################################################################
