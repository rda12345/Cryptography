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

class DomainElement(object):
    """
    Introducing a class which symmetrizes left and right arithmetic operations
    """
    def __radd__(self, other): return self + other
    def __rsub__(self, other): return -self + other
    def __rmul__(self, other): return self * other
    operatorPrecedence = 1


class FieldElement(DomainElement):
    def __truediv__(self, other): return self * other.inverse()
    def __rtruediv__(self, other): return self.inverse() *other

# the IntegerModPrime is encapsulated within a function IntegerModP
# in order to typecast of an int
def IntegerModP(p):
    class IntegerModPrime(FieldElement):
        """
        Integer modular prime field elements. The class includes all the
        field arithmetic and comparison functions.
        """

        def __init__(self, n):
            self.n = n % p
            self.p = p


        def __add__(self, other):
            return IntegerModPrime(self.n + other.n)


        def __sub__(self, other):
            return IntegerModPrime(self.n + other.n)

        def __mul__(self, other):
            return IntegerModPrime(self.n * other.n)

        def __truediv__(self, other):
            return IntegerModPrime(self.n) * other.inverse()

        def __divmod__(self, other):
            """
            Returns the (quotient, remainder) of the division of self by other
            as IntegerModPrime numbers.
            """
            q, r = divmod(self.n, other.n)
            return (IntegerModPrime(q), IntegerModPrime(r))

        def __neg__(self):
            return IntegerModPrime(-self.n)

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
            return IntegerModPrime(x)

    IntegerModP.p = p
    IntegerModP.__name__ = f"Z/{p}"
    return IntegerModPrime
    
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
    
    
# Building a generic type system
def typecheck(f):
    def new_f(self, other):
        # checking operatorPrecedence, if other's type has precendence ignore add and perform radd of other
        if (hasattr(other.__class__, "operatorPrecedence")) and other.__class__.operatorPrecedence > self.__class__.operatorPrecedence:
            return NotImplemented
        if type(self) is not type(other):
            try: self.__class__(other)
            except TypeError:
                raise TypeError(f"Cannot transform {other} of type {type(other)} to type {type(self)}")
            except Exception as e:
                raise TypeError(f"Type error on arguments {self}, {other} for function f.__name__. Reason: {e}")
        return f(self, other)
    return new_f


if __name__ == "__main__":
    
    print('#------------ TESTS ------------#')
    P = IntegerModP(7)(3)
    Q = IntegerModP(7)(6)
    print(f"P: {P}, Q: {Q}")
    print(f"P + Q: {P + Q}")
    print(f"invese(P) = {P.inverse()}")
    print(f"P == Q : {P==Q}")
    print(f"P*inverse(P): {P*P.inverse()}")
    
    
    
    