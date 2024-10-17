Primes = [
    2,
    3,
    5,
    7,
    11,
    13,
    17,
    19,
    23,
    29,
    31,
    37,
    41,
    43,
    47,
    53,
    59,
    61,
    67,
    71,
    73,
    79,
    83,
    89,
    97,
    101,
    103,
    107,
    109,
    113,
    127,
    131,
    137,
    139,
    149,
    151,
    157,
    163,
    167,
    173,
    179,
    181,
    191,
    193,
    197,
    199,
    211,
    223,
    227,
    229,
    233,
    239,
    241,
    251,
    257,
    263,
    269,
    271,
    277,
    281,
    283,
    293,
    307,
    311,
    313,
    317,
    331,
    337,
    347,
    349,
    353,
    359,
    367,
    373,
    379,
    383,
    389,
    397,
    401,
    409,
    419,
    421,
    431,
    433,
    439,
    443,
    449,
    457,
    461,
    463,
    467,
    479,
    487,
    491,
    499,
    503,
    509,
    521,
    523,
    541,
    547,
    557,
    563,
    569,
    571,
    577,
    587,
    593,
    599,
    601,
    607,
    613,
    617,
    619,
    631,
    641,
    643,
    647,
    653,
    659,
    661,
    673,
    677,
    683,
    691,
    701,
    709,
    719,
    727,
    733,
    739,
    743,
    751,
    757,
    761,
    769,
    773,
    787,
    797,
    809,
    811,
    821,
    823,
    827,
    829,
    839,
    853,
    857,
    859,
    863,
    877,
    881,
    883,
    887,
    907,
    911,
    919,
    929,
    937,
    941,
    947,
    953,
    967,
    971,
    977,
    983,
    991,
    997,
    1009,
    1013,
]

MIDI_0_FREQ = 8.17579891564371

# This is a particularly gnarly thing, perhaps a better implementation could be
# done, but for now...
# Given a Sieve, equal division of octave number and a center frequency in Hz
# This will produce a tuning table for the 128 MIDI keys, trying its best
# to keep things tidy


def sieve_to_tuning_table(sv, edo, centerfreq):
    """Incomplete implementation! This does not yet produce a tuning table suitable for MIDI key mapping"""

    def tun_tab_loop(sv, edo, direction, targetlist, centerfreq):
        i = 0
        while True:
            if sv.contains(i):
                hz = centerfreq * 2.0 ** (i / float(edo))
                if hz < MIDI_0_FREQ or hz > 20000.0:
                    # print(f'{i} {hz}')
                    break
                else:
                    if targetlist.count(hz) == 0:
                        targetlist.append(hz)
            i += direction
            if abs(i > 2048):
                break

    # first generate all frequencies in audible range
    frequencies = []
    tun_tab_loop(sv, edo, -1, frequencies, centerfreq)
    tun_tab_loop(sv, edo, 1, frequencies, centerfreq)
    frequencies.sort()
    temp = 30000.0
    closest = None
    for i in range(0, len(frequencies)):
        diff = abs(frequencies[i] - centerfreq)
        if diff <= temp:
            closest = i
            temp = diff
    if closest == None:
        print(f"could not determine closest index to {centerfreq}")
        return []
    result = [0] * 128
    for i in range(closest, -1, -1):
        if i >= 0 and i < len(frequencies):
            print(frequencies[i])
    for i in range(closest, 128):
        if i >= 0 and i < len(frequencies):
            print(frequencies[i])
    return result


pcNames = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]


def midiKeyToName(key):
    pc = key % 12
    oct = key // 12
    return f"{pcNames[pc]}{oct-1}"


def map_value(
    value: float, leftMin: float, leftMax: float, rightMin: float, rightMax: float
):
    # Figure out how 'wide' each range is
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    # Convert the left range into a 0-1 range (float)
    valueScaled = float(value - leftMin) / float(leftSpan)

    # Convert the 0-1 range into a value in the right range.
    return rightMin + (valueScaled * rightSpan)
