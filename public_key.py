from math_crypto import modinv, egcd


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
    return {
        "A": A,
        "B": B,
        "key1": key1,
        "key2": key2,
        "shared_equal": key1 == key2,
    }


def elgamal_encrypt(m, p, g, y, k):
    if not (0 <= m < p):
        raise ValueError("Message must satisfy 0 <= m < p")
    if not (0 < k < p - 1):
        raise ValueError("k must satisfy 0 < k < p-1")

    a = pow(g, k, p)
    b = (m * pow(y, k, p)) % p
    return a, b


def elgamal_decrypt(a, b, x, p):
    s = pow(a, x, p)
    return (b * modinv(s, p)) % p


def shamir_encrypt(m, p, ca, cb):
    """
    Simplified Shamir three-pass protocol for a single integer message m < p.
    Returns the final transmitted value after three passes.
    """
    if m >= p:
        raise ValueError("m must be less than p")
    if egcd(ca, p - 1)[0] != 1 or egcd(cb, p - 1)[0] != 1:
        raise ValueError("ca and cb must be invertible modulo p-1")

    da = modinv(ca, p - 1)
    db = modinv(cb, p - 1)

    x1 = pow(m, ca, p)
    x2 = pow(x1, cb, p)
    x3 = pow(x2, da, p)
    x4 = pow(x3, db, p)
    return x4