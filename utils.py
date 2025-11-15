import hashlib

def hashSenha(senha):
    texto_bytes = senha.encode('utf-8')
    hash_sha256 = hashlib.sha256(texto_bytes)
    return hash_sha256.hexdigest()