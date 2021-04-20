# got from https://rosettacode.org/wiki/CRC-32#Python
#CRC Table for exact similarity detection 
def create_table():
    a = []
    for i in range(256):
        k = i
        for j in range(8):
            if k & 1:
                k ^= 0x1db710640
            k >>= 1
        a.append(k)
    return a
 
def crc_update(buf, crc):
    crc ^= 0xffffffff
    for k in buf:
        crc = (crc >> 8) ^ crc_table[(crc & 0xff) ^ k]
    return crc ^ 0xffffffff
 
crc_table = create_table()
#print(hex(crc_update(b"The quick brown fox jumps over the lazy dog", 0)))

# calculate CRC first before processing
# calculate CRC and determine if unique in a set, only return unique links

# got from https://ofstack.com/python/10796/python-implements-an-instance-of-the-simhash-algorithm.html
# Simhash for near similarity detection
class simhash:

    # The constructor 
    def __init__(self, tokens='', hashbits=128):        
        self.hashbits = hashbits
        self.hash = self.simhash(tokens);

    #toString function     
    def __str__(self):
        return str(self.hash)

    # generate simhash value     
    def simhash(self, tokens):
        v = [0] * self.hashbits
        for t in [self._string_hash(x) for x in tokens]: #t for token The ordinary hash value            
            for i in range(self.hashbits):
                bitmask = 1 << i
                if t & bitmask :
                    v[i] += 1 # View the current bit Whether a is 1, If yes, it will be the bit +1
                else:
                    v[i] -= 1 # otherwise , The bit -1
        fingerprint = 0
        for i in range(self.hashbits):
            if v[i] >= 0:
                fingerprint += 1 << i
        return fingerprint # document-wide fingerprint Is the final bits >=0 And of the 

    # Find the hamming distance 
    def hamming_distance(self, other):
        x = (self.hash ^ other.hash) & ((1 << self.hashbits) - 1)
        tot = 0
        while x :
            tot += 1
            x &= x - 1
        return tot

    # O similarity 
    def similarity (self, other):
        a = float(self.hash)
        b = float(other.hash)
        if a > b : 
            return b / a
        else: 
            return a / b

    # for source generate hash value    ( A variable length version Python Built-in hash )
    def _string_hash(self, source):        
        if source == "":
            return 0
        else:
            x = ord(source[0]) << 7
            m = 1000003
            mask = 2 ** self.hashbits - 1
            for c in source:
                x = ((x * m) ^ ord(c)) & mask
            x ^= len(source)
            if x == -1:
                x = -2
            return x