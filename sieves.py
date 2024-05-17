class SV:
    def __init__(self,a,b):
        self.a = a
        self.b = b
        if a>0 and b>=0:
            self.match = lambda n : (n % self.a) == self.b
        else:
            self.match = lambda n : False
        
    def dump(self, start = 0, n = 100):
        result = ""
        for i in range(start,start+n):
            if (self.match(i))==True:
                result = result + "■"
            else:
                result = result + "·"
        print (result)

    def __neg__(self):
        # print("negate")
        result = SV(0,0)
        result.match = lambda n : (not (self.match(n)))
        return result
    
    def __mul__(self, other):
        # print(f"intersection {self.a},{self.b} * {other.a},{other.b}")
        result = SV(0,0)
        result.match = lambda n : (self.match(n) and other.match(n))
        return result
    
    def __add__(self, other):
        # print(f"union {self.a},{self.b} + {other.a},{other.b}")
        result = SV(0,0)
        result.match = lambda n : (self.match(n) or other.match(n))
        return result
    
    def __xor__(self, other):
        # print("xor")
        result = SV(0,0)
        result.match = lambda n : (self.match(n) ^ other.match(n))
        return result
    
    def toSequenceList(self,start,end):
        result = []
        for i in range(start,end):
            if self.match(i):
                result.append(i)
        return result

    def toIntervalList(self,start,end):
        # maybe this could be implemented better...
        result = []
        previous = None
        for i in range(start,end):
            if self.match(i):
                if previous == None:
                    previous = i
                else:
                    result.append(i - previous)
                    previous = i
        return result

if __name__ == "__main__":
    pass
