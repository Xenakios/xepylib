# Minimal implementation of the Iannis Xenakis sieves and their operations


class SV:
    def __init__(self, a=1, b=0):
        self.a = a
        self.b = b
        if a > 0 and b >= 0:
            self.contains = lambda n: (n % self.a) == self.b
            self.b = b % a
        else:
            self.contains = lambda n: False

    def toString(self, start=0, n=101, chars=".■", ruler=False) -> str:
        result = ""
        for i in range(start, start + n):
            if self.contains(i):
                result = result + chars[1]
            else:
                result = result + chars[0]
        result += "\n"
        if ruler:
            i = start
            while i < start + n:
                if i % 5 == 0:
                    result += f"{i:<5}"
                i += 1
            
        return result

    def __neg__(self):
        result = SV(0, 0)
        result.contains = lambda n: (not (self.contains(n)))
        return result

    def __mul__(self, other):
        result = SV(0, 0)
        result.contains = lambda n: (self.contains(n) and other.contains(n))
        return result

    def __add__(self, other):
        result = SV(0, 0)
        result.contains = lambda n: (self.contains(n) or other.contains(n))
        return result

    def __xor__(self, other):
        result = SV(0, 0)
        result.contains = lambda n: (self.contains(n) ^ other.match(n))
        return result

    def toSequenceList(self, start:int, end:int):
        return [i for i in range(start, end) if self.contains(i)]

    def asGenerator(self, start=0):
        """Infinite generator from start"""
        while True:
            if self.contains(start):
                yield start
            start += 1

    def toIntervalList(self, start:int, end:int):
        # Seems inefficient to get the temp list first, but it's fast enough
        # up to hundreds of thousands of entries
        temp = self.toSequenceList(start, end)
        if len(temp) < 2:
            return []
        return [temp[i + 1] - temp[i] for i in range(0, len(temp) - 1)]


if __name__ == "__main__":
    pass
