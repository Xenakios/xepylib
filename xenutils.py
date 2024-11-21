import json
import math
import random

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
    if closest is None:
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


def midi_key_to_str(key: int) -> str:
    if key < 0 or key > 127:
        raise ValueError(f"{key} outside allowed range 0..127")
    pc = key % 12
    octave = key // 12
    return f"{pcNames[pc]}{octave-1}"


def random_cauchy(location: float = 0.0, scale: float = 1.0, z: float = None):
    """Generate random number from Cauchy distribution.
    If z in range 0..1 inclusive is provided it will be used instead of random.random()"""
    if z is None:
        z = random.random()
    else:
        if z < 0.0 or z > 1.0:
            raise ValueError("z should be between 0.0 and 1.0, inclusive")
    return location + scale * math.tan(math.pi * (z - 0.5))


def map_value(
    in_value: float,
    source_min: float,
    source_max: float,
    target_min: float,
    target_max: float,
) -> float:
    leftSpan = source_max - source_min
    rightSpan = target_max - target_min
    valueScaled = float(in_value - source_min) / float(leftSpan)
    return target_min + (valueScaled * rightSpan)


def clamp(in_value: float, min_value: float, max_value: float) -> float:
    return max(min_value, min(in_value, max_value))


def reflect(in_value: float, min_value: float, max_value: float) -> float:
    count = 0
    while in_value < min_value or in_value > max_value:
        if in_value < min_value:
            in_value = min_value + (min_value - in_value)
        if in_value > max_value:
            in_value = max_value + (max_value - in_value)
        count += 1
        if count > 1000:
            return clamp(in_value, min_value, max_value)
    return in_value


# probably not the best implementation, but let's have at least something
def quantize_to_closest(val: float, grid: list[float]):
    if len(grid) == 0:
        return val
    if len(grid) == 1:
        return grid[0]
    if val < grid[0]:
        return grid[0]
    if val > grid[-1]:
        return grid[-1]
    mindiff = grid[-1] - grid[0]
    closest_element = None
    for i in grid:
        diff = abs(i - val)
        if diff < mindiff:
            mindiff = diff
            closest_element = i
    return closest_element


def gen_pdarray_preset(data: list, outrange: int = 1):
    if len(data) == 0 or len(data) > 2048:
        raise RuntimeError("data is empty or too large")
    for i in range(len(data)):
        data[i] = clamp(data[i], 0.0, 1.0)
    template = {"plugin": "PdArray", "model": "Array", "version": "2.1.1"}
    template["params"] = [
        {"value": 2.0, "id": 0},
        {"value": outrange, "id": 1},
        {"value": 0.0, "id": 2},
    ]
    template["data"] = {
        "enableEditing": True,
        "boundaryMode": 2,
        "recMode": 0,
        "lastLoadedPath": "",
        "arrayData": [],
    }
    template["data"]["arrayData"] = data
    return json.dumps(template, indent=2)


def plot(plt, xs: list, ys: list):
    plt.style.use("dark_background")
    plt.plot(xs, ys)
    plt.get_current_fig_manager().window.state("zoomed")
    plt.show()


if __name__ == "__main__":
    pass
