def to_ascii85(b):

    b = b.encode() if type(b) is str else b

    if not b:
        return '<~~>'
    if b in b'\x00 \x00\x00 \x00\x00\x00'.split(b' '):
        return '<~!' + len(b) * '!' + '~>'

    tmp = [b[i:i + 4] for i in range(0, len(b), 4)]
    pad = 4 - len(tmp[-1])
    tmp[-1] += bytes(pad)
    tmp = [int.from_bytes(b, 'big') for b in tmp]

    ret = ''
    for x in tmp:
        d, m = divmod(x, 85)
        part = chr(m + 33)
        for i in range(4):
            d, m = divmod(d, 85)
            part += chr(m + 33)
        ret += part[::-1].replace('!!!!!', 'z')

    return '<~' + (ret[:-pad] if pad else ret) + '~>'


def from_ascii85(s):

    if len(s) < 5:
        return b''

    b = (s[2:-2].replace('z', '!!!!!').encode() if not type(s) is bytes
         else s[2:-2].replace(b'z', b'!!!!!'))
    tmp = [b[i:i + 5] for i in range(0, len(b), 5)]
    pad = 5 - len(tmp[-1])
    tmp[-1] += pad * b'\x75'

    tmp = [sum((group[x] - 33) * 85 ** (4 - x)
               for x in range(5)) for group in tmp]
    tmp = [x.to_bytes(4, 'big') for x in tmp]
    tmp[-1] = tmp[-1][:-pad] if pad else tmp[-1]

    return b''.join(part for part in tmp)

# Codewars Python 2
# from struct import unpack, pack
#
# def toAscii85(b):
#    if not b:
#        return '<~~>'
#    if b in '\x00 \x00\x00 \x00\x00\x00'.split(' '):
#        return '<~!' + len(b)*'!' + '~>'
#    tmp = [b[i:i+4] for i in range(0,len(b),4)]
#    pad = 4 - len(tmp[-1])
#    tmp[-1] += b'\x00' * pad
#    tmp = [unpack('>I', b)[0] for b in tmp]
#
#    ret = ''
#    for x in tmp:
#        d, m = divmod(x, 85)
#        part = chr(m + 33)
#        for i in range(4):
#            d, m = divmod(d, 85)
#            part += chr(m + 33)
#        ret += part[::-1].replace('!!!!!','z')
#
#    return ('<~' + (ret[:-pad] if pad else ret) + '~>')
#
#
# def fromAscii85(s):
#    s = "".join(s.split())
#    if len(s) < 5: return ''
#    b = s[2:-2].replace('z','!!!!!')
#    tmp = [b[i:i+5] for i in range(0,len(b),5)]
#    pad = 5 - len(tmp[-1])
#    tmp[-1] += pad * b'\x75'
#
#    tmp = [sum((ord(group[x])-33)*85**(4-x) for x in range(5)) for group in tmp]
#    tmp = [pack('>I', x) for x in tmp]
#    tmp[-1] = tmp[-1][:-pad] if pad else tmp[-1]
#
#    try:
#        return ''.join(part.decode() for part in tmp)
#    except UnicodeDecodeError:
#        return ''.join(part for part in tmp)
#

# print(to_ascii85('qwertyuiop'))
# print(to_ascii85(b'qwertyuiop'))
# print(from_ascii85('<~EHbu7FEr"CDf>~>'))
