# Minimal implementation for generating from the Iannis Xenakis sieves and operations on them.


class SV:
    def __init__(self, a: int = 1, b: int = 0):
        self.a = a
        self.b = b
        if a > 0 and b >= 0:
            self.contains = lambda n: (n % self.a) == self.b
            self.b = b % a
        else:
            self.contains = lambda n: False

    def visualization_string(self, start=0, n=101, chars=".■", ruler=False) -> str:
        result = ""
        for i in range(start, start + n):
            if self.contains(i):
                result = result + chars[1]
            else:
                result = result + chars[0]
        if ruler:
            result += "\n"
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
        result.contains = lambda n: (self.contains(n) ^ other.contains(n))
        return result

    def toList(self, start: int, end: int) -> list[int]:
        return [i for i in range(start, end) if self.contains(i)]

    def asGenerator(self, start=0):
        """Infinite generator from start"""
        while True:
            if self.contains(start):
                yield start
            start += 1

    def interval_generator(self, start: int = 0, end: int = 10000):
        prior = None
        i = start
        while True:
            if prior is None and self.contains(i):
                prior = i
            elif self.contains(i):
                diff = i - prior
                yield diff
                prior = i
            i += 1
            if i >= end:
                break

    def toIntervalList(self, start: int, end: int) -> list[int]:
        result = []
        prior = None
        for i in range(start, end):
            if prior is None and self.contains(i):
                prior = i
                continue
            if self.contains(i):
                diff = i - prior
                result.append(diff)
                prior = i
        return result


if __name__ == "__main__":
    pass
