import hashlib

def md5hash(filename):
    with open(filename, mode='rb') as f:
        h = hashlib.md5()
        for chunk in f.read(4096):
            # This was hard to find. Apparently iterating over a bytes object
            # in python 3 returns integers.
            chunk = bytes(chunk)
            h.update(chunk)
        return h.hexdigest()