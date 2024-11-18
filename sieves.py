# Minimal implementation for generating from the Iannis Xenakis sieves and operations on them.


class Sieve:
    def __init__(self, a: int = 1, b: int = 0):
        self.a = a
        self.b = b
        if a > 0 and b >= 0:
            self.contains = lambda n: (n % self.a) == self.b
            self.b = b % a
        else:
            self.contains = lambda n: False

    def __contains__(self, x: int) -> bool:
        return self.contains(x)

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
        result = Sieve(0, 0)
        result.contains = lambda n: (not (self.contains(n)))
        return result

    def __mul__(self, other):
        result = Sieve(0, 0)
        result.contains = lambda n: (self.contains(n) and other.contains(n))
        return result

    def __add__(self, other):
        result = Sieve(0, 0)
        result.contains = lambda n: (self.contains(n) or other.contains(n))
        return result

    def __xor__(self, other):
        result = Sieve(0, 0)
        result.contains = lambda n: (self.contains(n) ^ other.contains(n))
        return result

    def __repr__(self):
        if self.a > 0 and self.b >= 0:
            return f"Sieve({self.a}, {self.b})"
        return f"Compound Sieve id={id(self)}, detailed repr not available"

    def get_list(self, start: int, end: int) -> list[int]:
        """Get as list between start (inclusive) and end (exclusive).

        (SV(12, 1) + SV(30, 0)).get_list(0, 30) produces
        [0, 1, 13, 25]

        (SV(12, 1) + SV(30, 0)).get_list(1, 31) produces
        [1, 13, 25, 30]
        """
        return [i for i in range(start, end) if self.contains(i)]

    def get_generator(self, start=0):
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

    def get_intervals(self, start: int, end: int) -> list[int]:
        """Get list of intervals between start and end.

        (SV(12, 1) + SV(30, 0)).get_intervals(0, 31) produces :
        [1, 12, 12, 5]

        (SV(4, 1) + SV(3, 0)).get_intervals(0, 13) produces :
        [1, 2, 2, 1, 3, 3]
        """
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
