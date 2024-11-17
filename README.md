Sieves examples

```
from xepylib import xenutils
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

Major/diatonic scale, assuming elementary displacement is 1 semitone,
from Xenakis 1990

```
sv = (
    -SV(3, 2) * SV(4, 0)
    + -SV(3, 1) * SV(4, 1)
    + SV(3, 2) * SV(4, 2)
    + -SV(3, 0) * SV(4, 3)
)
pitchlist = sv.get_list(60, 73)
print(pitchlist)
print([xenutils.midi_key_to_name(k) for k in pitchlist])

```

Outputs

```
[60, 62, 64, 65, 67, 69, 71, 72]
['C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4', 'C5']
```


