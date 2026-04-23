from collections import defaultdict


def normalize_text(text):
    return ''.join(c for c in text.upper() if c.isalpha())


def caesar_encrypt(text, shift):
    res = ""
    for c in text:
        if c.isalpha():
            res += chr((ord(c.upper()) - 65 + shift) % 26 + 65)
        else:
            res += c
    return res


def caesar_decrypt(text, shift):
    return caesar_encrypt(text, -shift)


def vigenere_encrypt(text, key):
    text = normalize_text(text)
    key = normalize_text(key)
    res = ""

    for i, c in enumerate(text):
        k = ord(key[i % len(key)]) - 65
        res += chr((ord(c) - 65 + k) % 26 + 65)
    return res


def vigenere_decrypt(text, key):
    text = normalize_text(text)
    key = normalize_text(key)
    res = ""

    for i, c in enumerate(text):
        k = ord(key[i % len(key)]) - 65
        res += chr((ord(c) - 65 - k) % 26 + 65)
    return res


def kasiski(text, seq_len=3):
    text = normalize_text(text)
    positions = defaultdict(list)

    for i in range(len(text) - seq_len + 1):
        seq = text[i:i + seq_len]
        positions[seq].append(i)

    distances = []
    for seq, pos in positions.items():
        if len(pos) > 1:
            for i in range(len(pos) - 1):
                distances.append(pos[i + 1] - pos[i])

    return distances