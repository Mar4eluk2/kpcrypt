from math_crypto import modinv


def rsa_keygen(p, q):
    n = p * q
    phi = (p - 1) * (q - 1)
    e = 65537
    d = modinv(e, phi)
    return (e, n), (d, n)


def rsa_encrypt(m, pub):
    e, n = pub
    return pow(m, e, n)


def rsa_decrypt(c, priv):
    d, n = priv
    return pow(c, d, n)


def diffie_hellman(p, g, a, b):
    A = pow(g, a, p)
    B = pow(g, b, p)
    key1 = pow(B, a, p)
    key2 = pow(A, b, p)
    return key1, key2


def elgamal_encrypt(m, p, g, y, k):
    a = pow(g, k, p)
    b = (m * pow(y, k, p)) % p
    return a, b


def elgamal_decrypt(a, b, x, p):
    return (b * modinv(pow(a, x, p), p)) % p