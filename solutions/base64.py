def to_base64(s):
    """ Returns base64 encoded string.

    >>> to_base64('any carnal pleasure.')
    'YW55IGNhcm5hbCBwbGVhc3VyZS4='
    >>> to_base64('any carnal pleasure'
    'YW55IGNhcm5hbCBwbGVhc3VyZQ=='
    >>> to_base64('any carnal pleasur')
    'YW55IGNhcm5hbCBwbGVhc3Vy'
    """
    s = s.encode() if type(s) == str else s  # to_bytes
    s = [s[i:i + 3][::-1] for i in range(0, len(s), 3)]
    ret = ''
    for block in s:
        ret += enc24b(block)
    return ret


def enc24b(b):
    """ Helper function for to_base64 """
    pad = 3 - len(b)
    b = b'\x00' * pad + b

    bb = 0
    for i, x in enumerate(b):
        bb |= (x << (i * 8))

    symbols = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
    ret = ''.join(symbols[(bb & 0x3f << i * 6) >> i * 6] for i in range(3, -1, -1))
    return ret[:4 - pad] + '=' * pad


def from_base64(s):
    """ Returns string decoded from base64 string. """
    s = [s[i:i + 4] for i in range(0, len(s), 4)]
    ret = ''
    for block in s:
        ret += dec24b(block)
    return ret


def dec24b(s):
    """ Helper function for from_base64 """
    symbols = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
    pad = s.count('=')
    s = [symbols.index(x) if x != '=' else 0 for x in s][::-1]

    bb = 0
    for i, x in enumerate(s):
        bb |= (x << (i * 6))

    ret = ''.join(chr((bb & 0xff << i * 8) >> i * 8) for i in range(2, -1, -1))
    # ret = bytes(((bb & 0xff<<i*8) >> i*8) for i in range(2, -1, -1))
    return ret[:3 - pad]


"""
## MangNguyen

CODES = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/";
def to_base_64(string):
    padding = 3 - len(string) % 3 if len(string) % 3 else 0
    binary = ''.join(format(ord(i),'08b') for i in string) + '00'*padding
    return ''.join(CODES[int(binary[i:i+6], 2)] for i in range(0, len(binary), 6))
    
def from_base_64(string):
    binary = ''.join(format(CODES.find(i),'06b') for i in string)
    return ''.join(chr(int(binary[i:i+8], 2)) for i in range(0, len(binary), 8)).rstrip('\x00')
    
"""
