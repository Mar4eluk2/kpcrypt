def simple_hash(text):
    h = 0
    for c in text:
        h = (h * 31 + ord(c)) % (2**32)
    return h


def sign(message, d, n):
    h = simple_hash(message)
    return pow(h, d, n)


def verify(message, signature, e, n):
    h = simple_hash(message)
    return pow(signature, e, n) == h