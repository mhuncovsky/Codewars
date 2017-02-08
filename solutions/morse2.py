

MORSE_CODE = {
    '.-...': '&', '--..--': ',', '....-': '4', '.....': '5',
    '...---...': 'SOS', '-...': 'B', '-..-': 'X', '.-.': 'R',
    '.--': 'W', '..---': '2', '.-': 'A', '..': 'I', '..-.': 'F',
    '.': 'E', '.-..': 'L', '...': 'S', '..-': 'U', '..--..': '?',
    '.----': '1', '-.-': 'K', '-..': 'D', '-....': '6',
    '-...-': '=', '---': 'O', '.--.': 'P', '.-.-.-': '.',
    '--': 'M', '-.': 'N', '....': 'H', '.----.': "'",
    '...-': 'V', '--...': '7', '-.-.-.': ';', '-....-': '-',
    '..--.-': '_', '-.--.-': ')', '-.-.--': '!', '--.': 'G',
    '--.-': 'Q', '--..': 'Z', '-..-.': '/', '.-.-.': '+',
    '-.-.': 'C', '---...': ':', '-.--': 'Y', '-': 'T',
    '.--.-.': '@', '...-..-': '$', '.---': 'J', '-----': '0',
    '----.': '9', '.-..-.': '"', '-.--.': '(', '---..': '8',
    '...--': '3'
}


# pause between dots/dashes 0, chars 000, words 0000000

def decodeMorse(morseCode):
    words = [word.split() for word in morseCode.split('   ')]
    return ' '.join(''.join(MORSE_CODE[c] for c in word if c)
                    for word in words if word)


def decodeBits(bits):
    bits = bits.strip('0')
    rate = set(len(x) for x in bits.split('0') if x).union(
        set(len(x) for x in bits.split('1') if x))
    if len(rate) > 1:
        rate = min(rate)
    else:
        rate = rate.pop()

    print(rate, bits)
    bits = bits.replace('0' * rate, '0').replace('1' * rate, '1')
    bits = bits.replace('0' * 7, '   ')
    bits = bits.replace('0' * 3, ' ')
    bits = bits.replace('1' * 3, '-').replace('1', '.')
    bits = bits.replace('0', '')
    return bits


def decodeBitsAdvanced(bits):
    from sklearn.cluster import KMeans
    from numpy import array
    # print(bits)

    bits = bits.strip('0')
    ones = [float(len(x)) for x in bits.split('0') if x][::-1]
    zeros = [float(len(x)) for x in bits.split('1') if x][::-1]

    if not ones:
        return ''
    if len(ones) < 10:
        ret = short(ones, zeros)
    else:
        km0 = KMeans(n_clusters=3)
        km1 = KMeans(n_clusters=2)
        km0.fit(array(zeros).reshape(-1, 1))
        km1.fit(array(ones).reshape(-1, 1))
        cc0 = km0.cluster_centers_.reshape(1, -1)
        cc1 = km1.cluster_centers_.reshape(1, -1)
        cc0.sort()
        cc1.sort()

        ret = short(ones,
                    zeros,
                    0.5 * (cc1[0, 1] + cc1[0, 0]),
                    0.5 * (cc0[0, 0] + cc0[0, 1]),
                    0.5 * (cc0[0, 1] + cc0[0, 2]),
                    True)

    # print(ret)
    # print(decodeMorse(ret))

    return ret


def short(ones, zeros, c1=1.7, c01=1.7, c02=5.2, m=False):
    if not m:
        rate1 = [x for x in ones if x <= sum(ones) / float(len(ones))]
        rate1 = float(sum(rate1)) / float(len(rate1))
        rate0 = sum(zeros) / float(len(zeros)) if zeros else 99999.0
        rate = min(rate1, rate0)
    else:
        rate = 1.0

        # print('Rate: ', rate)

    ret = ''
    while ones:
        c = ones.pop()
        if c / rate > c1:
            ret += '-'
        else:
            ret += '.'
        c = zeros.pop() if zeros else 0
        if c / rate > c02:
            ret += '   '
        elif c / rate > c01:
            ret += ' '
    return ret
