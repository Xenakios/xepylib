# Minimal implementation of the Iannis Xenakis sieves and their operations

class SV:
    def __init__(self,a,b):
        self.a = a
        self.b = b
        if a>0 and b>=0:
            self.match = lambda n : (n % self.a) == self.b
            self.b = b % a
        else:
            self.match = lambda n : False
        
    def dump(self, start = 0, n = 101, chars=".■", ruler=False):
        result = ""
        for i in range(start,start+n):
            if (self.match(i))==True:
                result = result + chars[1]
            else:
                result = result + chars[0]
        print (result)
        if ruler:
            result = ""
            i = start
            while i<start+n:
                if i % 5 == 0:
                    result+=(f"{i:<5}")
                i += 1
            print (result)

    def __neg__(self):
        result = SV(0,0)
        result.match = lambda n : (not (self.match(n)))
        return result
    
    def __mul__(self, other):
        result = SV(0,0)
        result.match = lambda n : (self.match(n) and other.match(n))
        return result
    
    def __add__(self, other):
        result = SV(0,0)
        result.match = lambda n : (self.match(n) or other.match(n))
        return result
    
    def __xor__(self, other):
        result = SV(0,0)
        result.match = lambda n : (self.match(n) ^ other.match(n))
        return result
    
    def toSequenceList(self,start,end):
        return [i for i in range(start,end) if self.match(i)]
    
    def asGenerator(self,start):
        """Infinite generator from start"""
        while True:
            if self.match(start):
                yield start
            start += 1
    
    def toIntervalList(self,start,end):
        # Seems inefficient to get the temp list first, but it's fast enough
        # up to hundreds of thousands of entries
        temp = self.toSequenceList(start,end)
        if len(temp)<2:
            return []
        return [temp[i+1]-temp[i] for i in range(0,len(temp)-1)]

if __name__ == "__main__":
    pass
