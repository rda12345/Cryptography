#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Finite fields programming, based on a blog post of Jeremy kun.
IntegerModPrime class implements the field of integers modular prime

The inverse evaluation employs the extended Euclidian algorithm, which relies on the 
theorem: for any two integers a,b in Z there exist a unique x,y in Z such that
a*x + b*y = gcd(a,b)
After evaluatign a*x +p*y = 1 we take mod p and get a*x mod p = 1, therefore
x is the inverse of a.
"""


class IntegerModPrime(object):
    """
    Integer modular prime field elements. The class includes all the
    field arithmetic and comparison functions.
    """
    
    def __init__(self, n, p):
        self.n = n % p
        self.p = p
        
    
    def __add__(self, other):
        return IntegerModPrime(self.n +other.n, self.p)
    
    
    def __sub__(self, other):
        return IntegerModPrime(self.n +other.n, self.p)

    def __mul__(self, other):
        return IntegerModPrime(self.n * other.n, self.p)
        
    def __truediv__(self, other):
        return IntegerModPrime(self.n) * other.inverse()
    
    def __divmod__(self, other):
        """
        Returns the (quotient, remainder) of the division of self by other 
        as IntegerModPrime numbers.
        """
        q, r = divmod(self.n, other.n)
        return (IntegerModPrime(q, self.p), IntegerModPrime(r, self.p))
    
    def __neg__(self):
        return IntegerModPrime(-self.n, self.p)
        
    def __eq__(self, other):
        return isinstance(other, IntegerModPrime) & self.n == other.n & self.p == other.p
    
    def __abs__(self):
        return abs(self.n)
        
    def __str__(self):
        return f"{self.n} mod {self.p}"
        
    def __repr__(self):
        return f"IntegerModPrime({self.n},{self.p})"
    
    
    
    def inverse(self):
        x, _, _ = extendend_gcd(self.n, self.p)
        # the algorithm may give negative integers, the following line fixes this
        # so x is in Z_p.
        x = x % self.p            
        return IntegerModPrime(x, self.p)
        
    
def extendend_gcd(a, b):
    """Returns x,y in Z such that a*x + b*y = 1"""
    old_r, r = a, b
    old_x, x = 1, 0
      
    while r != 0: 
        q = old_r // r # quotient
        old_r, r = r, old_r - q*r
        old_x, x = x, old_x - q*x
    if b != 0:
        old_y = (old_r - old_x*a) // b
    else:
        old_y = 0
    # returns the Bezout coefficients (x,y) and the greatest common divisor (gcd), old_r
    return old_x, old_y, old_r
    
    
    
    
    
if __name__ == "__main__":
    
    print('#------------ TESTS ------------#')
    P = IntegerModPrime(3, 7)
    Q = IntegerModPrime(6, 7)
    print(f"P: {P}, Q: {Q}")
    print(f"P + Q: {P + Q}")
    print(f"invese(P) = {P.inverse()}")
    print(f"P == Q : {P==Q}")
    print(f"P*inverse(P): {P*P.inverse()}")
    
    
    
    