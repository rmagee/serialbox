#!/usr/bin/env python

class GaloisLFSR:
    # 16-bit 
    def __init__(self, seed):
        self.state = seed & 0xFFFF
        
    def getRand(self):
        self.state = (self.state >> 1) ^ (-(self.state&0x01) & 0xB400)
        return self.state & 0x01


class FibonacciLFSR:
    # 16-bit 
    def __init__(self, seed):
        self.state = seed & 0xFFFF
        
    def getRand(self):
        bit = ((self.state >> 0) ^ (self.state >> 2) ^ (self.state >> 3) ^ (self.state >> 5)) & 0x01
        self.state = ((self.state >> 1) | (bit<<15)) & 0xFFFF
        return self.state & 0x01
    

if __name__ == "__main__":
    # Test galois lfsr
    glfsr = GaloisLFSR(0xACE1)
    for i in range(10):  
        print(glfsr.getRand())

    # Test fibonacci lfsr
    flfsr = FibonacciLFSR(0xACE1)
    flfsr.getRand()
    assert(0x5670 == flfsr.state)
    print("Fibonacci LFSR test passed.")