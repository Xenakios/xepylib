Sieves examples

```
from xepylib import xenutils as xu
from xepylib.sieves import Sieve as SV
```

Chromatic scale, assuming elementary displacement is 1 semitone

```
sv = SV(1,0)
print(sv.get_list(60,73))
```

Outputs

```
[60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72]
```

Whole tone scale, at the 2 possible transpositions

```
for i in range(0,2):
    print(SV(2,i).get_list(60,74))
```

```
[60, 62, 64, 66, 68, 70, 72]
[61, 63, 65, 67, 69, 71, 73]
```

Major scale, assuming elementary displacement is 1 semitone,
from Xenakis 1990. This is obviously a very convoluted way to get the
major scale pattern, but it's an example...

```
sv = (
    -SV(3, 2) * SV(4, 0)
    + -SV(3, 1) * SV(4, 1)
    + SV(3, 2) * SV(4, 2)
    + -SV(3, 0) * SV(4, 3)
)
# list output can start from negative numbers
pitchlist = sv.get_list(-12, 13)
print(pitchlist)
# but MIDI keys can't be negative, so center around middle C4 (60)
print([xu.midi_key_to_str(60 + k) for k in pitchlist])
# or the B3 below
print([xu.midi_key_to_str(59 + k) for k in pitchlist])
```
Outputs :
```
[-12, -10, -8, -7, -5, -3, -1, 0, 2, 4, 5, 7, 9, 11, 12]
['C3', 'D3', 'E3', 'F3', 'G3', 'A3', 'B3', 'C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4', 'C5']
['B2', 'C#3', 'D#3', 'E3', 'F#3', 'G#3', 'A#3', 'B3', 'C#4', 'D#4', 'E4', 'F#4', 'G#4', 'A#4', 'B4']
```

Rough matplotlib visualization :
```
# from matplotlib import pyplot as plt
sv = SV(11, 0) + SV(8, 3) + SV(8, 7)
xs = [i for i in range(0,100)]
ys = [1 if i in sv else None for i in xs]
plt.scatter(xs, ys)
plt.show()

```
