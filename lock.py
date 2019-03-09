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

def lock(text, pw):
    text_l = len(text)
    pw_l = len(pw)
    encrypted = text
    idx = 0

    # seed text with password
    for i in range(len(pw)):
        encrypted[i] = __rangemod(pw_l[i] + text[i], ord('A'), ord('Z'))  # for now, stay in uppercase range
        idx += 1

    # build further characters with prior characters
    for i in range(idx + 1, len(text)):
        encrypted[idx] = __rangemod(text[i-1] + text[i], ord('A'), ord('Z'))

    return encrypted

def unlock(encrypted, pw):
    raise NotImplementedError

def main():
    if len(sys.argv) != 3:
        print("Usage: python lock.py <file>")
        return 1

    option = sys.argv[1]
    filename = sys.argv[2]

    pw = getpass.getpass()

    if option == '-e' or '--encrypt':
        with open(filename, "r") as f:
            text = f.read()
            f.close()
        if text is None:
            print("Failed to read file")
            return 1
        
        encrypted = lock(text, pw)
        with open(filename, "w") as f:
            f.write(encrypted)
            f.close()

    elif option == '-d' or '--decrypt':
        with open(filename, "r") as f:
            encrypted = f.read()
            f.close()

        if encrypted is None:
            print("Failed to read file")
            return 1
        
        text = unlock(encrypted, pw)
        with open(filename, "w") as f:
            f.write(text)
            f.close()

    else:
        print("Unrecognized option: {}".format(option))
        return 1

    return 0

if __name__ == "__main__":
    sys.exit(main())
