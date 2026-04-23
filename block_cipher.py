def feistel_round(left, right, key):
    f = (right ^ key) & 0xFFFF
    return right, left ^ f


def feistel_encrypt(block, keys):
    left = (block >> 16) & 0xFFFF
    right = block & 0xFFFF

    for k in keys:
        left, right = feistel_round(left, right, k)

    return (left << 16) | right


def feistel_decrypt(block, keys):
    left = (block >> 16) & 0xFFFF
    right = block & 0xFFFF

    for k in reversed(keys):
        left, right = feistel_round(left, right, k)

    return (left << 16) | right