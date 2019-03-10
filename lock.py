import sys
import getpass


def __rangemod(x, l, u):
    """
    rangemod: return *x*'s index in the modulus ring of [l,u] i.e. [0,u-l+1] + l
    """
    # place in 0, k range
    x_p = x - l
    u_p = u - l

    # perform mod in ring modulus u-l+2 i.e. [0, u-l+1]
    # and restore range
    return (x_p % u_p) + l

def __key_extend(key, length):
    if len(key) > length:
        return key[:length]
    elif len(key) == length:
        return key

    while len(key) < length:
        key += chr((ord(key[-1]) * ord(key[-2])) % 26 + ord('a'))

    return key

def transform(text, pw):
    transformed = ''
    assert len(pw) == len(text)

    # one time pad the plaintext
    for i in range(len(pw)):
        transformed += chr(ord(pw[i]) ^ ord(text[i]))

    return transformed

def main():
    if len(sys.argv) != 2:
        print("Usage: python lock.py <file>")
        return 1

    filename = sys.argv[1]
    pw = getpass.getpass()
    raw = None

    with open(filename, "r") as f:
        raw = f.read()
        f.close()

    if raw is None:
        print("Failed to read file")
        return 1

    pw = __key_extend(pw, len(raw))
    new = transform(raw, pw)

    with open(filename, "w") as f:
        f.write(new)
        f.close()

    return 0

if __name__ == "__main__":
    sys.exit(main())
