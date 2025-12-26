#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Elliptic_curves - contains and implementation of the elliptic curve cryptography 
algorithm, based on the blog posts of Jeremy Kun
"""


class Point(object):
    """
    Implements a 2D point
    """
    
    def __init__(self, curve, x , y):
        self.curve = curve
        self.x = x
        self.y = y 
        
        if not curve.isOnCurve(self.x, self.y):
            raise Exception("The point %s is not on the curve %s" % (self, curve))
    
    def __str__(self):
        return '(%G, %G)' %(self.x, self.y)
    
    
        
    def __neg__(self):
        """
        Returns the negative of an point on the elliptic curve, i.e.,
        a relection around the x-axis.
        """
        return Point(self.curve, self.x, -self.y)
    
   ## Arithmetic (actually application of the group operation)   
    
    def __add__(self, other):
        """
        Performs the group multipicaton operator 'adding' two points on the
        elliptic curve. 
        To add two points we calculate the intersection of the line connecting
        the two points with the elliptic curve self.curve, and reflect around 
        the x-axis.
        """  
        
        # case 1: adding 0 from the right
        if isinstance(other, Ideal):
            return self
        
        # case 2: adding P + (-P) = 0
        if self.y == - other.y and self.x == other.x:
            return Ideal(self.curve)     
        else:
            # case 3: addition of the same point
            if (self.x, self.y) == (other.x, other.y):
                # slope of the tangent line
                s = (3*self.x**2 + self.curve.a)/(2*self.y)
            
            # case 4: addition of two diffenent lines on the curve    
            # linear line's slope
            else:
                s = (self.y-other.y)/(self.x-other.x) 
            
            # third intersection coordinates
            x3 = s**2 -self.x -other.x
            y3 = s*(x3-other.x) + other.y
            
            # reflection around the x-axis
            p = Point(self.curve, x=x3, y=-y3)
            return p
   
    def __sub__(self, other):
        """Add a point on the elliptic curve to the negative of another"""
        return self + (-other)
    
    
    def __mul__(self, n: int):
        """Performs efficient multipication by an integer"""
        
        # non integer scalar
        if not isinstance(n, int):
            raise Exception("Can only multiply by an integer")
        
        # multipication by 0
        if n==0:
            return Ideal(self.curve)
        # if n is negative multiply the negative of self
        elif n < 0:
            return (-self)*(-n)
        # n is a positive integer - implement multipication by adding
        # P * n = b_0 * P + b_1 * P^2 +...+ b_k * 2^P
        else: 
            S = Ideal(self.curve)  # stores the updating sum
            T = P # temparory variable
            
            # loop over all the binary digits of integer n
            for _ in range(len(bin(n))-2):   
                R = T if n & 1 == 1 else Ideal(self.curve)
                S += R
                n = n >> 1
                T += T
            return S
                
                
    def __rmul__(self, n: int):
        """Multipication by an integer from the left"""
        return self * n
        
        
      
    ## Comparison 
     
    def __eq__(self, other):
        return (self.x, self.y) == (other.x, other.y)
    
    
    def __lt__(self, other):
        if self.x < other.x:
            return True
        elif self.x > other.x:
            return False
        else:
            if self.y < other.y:
                return True
            else:
                return False
            
            
    def __gt__(self, other):
        
        if self.__lt__(other) == False and self.__eq__(other)== False:
            return True
        else: 
            return False
        
    def __ge__(self, other):
        return self > other or self == other
    
    def __le___(self, other):
        return self < other or self == other
        
        


    
    
    
        
class Ideal(Point):
    
    def __init__(self, curve):
        self.curve = curve
    
    def __str__(self):
        return 'Ideal'
    
    def __add__(self, other):
        return other        
    
    def __neg__(self):
        return self
        
    
    

    
    
class EllipticCurve(object):

    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.discriminant = 4*self.a**3 + 27*self.b**2
        
        if not self.isSmooth():
            raise Exception("The curve %s is not smooth" % self)
        
    def isSmooth(self):
        """Checks if the curve is smooth"""
        return self.discriminant != 0
    
    def isOnCurve(self, x, y):
        """Checks if the point is on the curve"""
        return y**2 == x**3 + self.a * x + self.b
    
    
    def __str__(self):
        return 'y^2 = x^3 + %Gx + %G' % (self.a, self.b)
    
    
    
if __name__ == "__main__":
    
    # The use of fractions prevents floating point arithmetic issues.
    import fractions
    frac = fractions.Fraction
    
    print("--------------- TESTS ---------------")
    ## Point is not on the curve
    #c1 = EllipticCurve(a=17, b=1)
    #print(c1)
    #p1 = Point(curve=c1, a=1, b=2)
    
    ## Curve isn't smooth
    #c2 = EllipticCurve(a=0, b=0)
    
    ## Point is on the curve
    #c1 = EllipticCurve(a=1, b=2)
    #p1 = Point(curve=c1, x=1, y=2)
    
    
    ## Check addition
    c = EllipticCurve(a=frac(-2), b=frac(4))
    P = Point(curve=c, x=frac(3), y=frac(5))
    Q = Point(curve=c, x=frac(-2), y=frac(0))
    print(f"Addition check: {P+Q == Point(c,0, -2)}")
    
    ## Check the addition of P + 0 = 0 + P = P
    O = Ideal(c)
    print(f"Addition of zero from the left: {P + O == P}")
    print(f"Addition of zero from the right: {O + P == P}")

    # check of an addition of three number
    print(f"Addition of three numbers: {P+P+P == Point(c,frac(-237, 121), frac(845, 1331))}")    
    
    # Substraction, addition and multipication test
    c = EllipticCurve(a=frac(-2), b=frac(4))
    P = Point(c, x=frac(3), y=frac(5))
    Q = Point(c, x=frac(-2), y=frac(0))
    print(f"Substraction check: {P-Q == Point(c, frac(0, 1), frac(-2, 1))}")
    print(f"Five additions of P: {P+P+P+P+P == Point(c, frac(2312883, 1142761), frac(-3507297955, 1221611509))}")  
    print(f"Multipicatoin check: {(5*P == P + P + P + P + P)  & (5*P == P*5)}")
    print(f"Greater than check: {(P > Q) & (P > -P)}")
    print(f"Less than check: {(Q <= P) & (-P <= P)}")
    print(f"Q-3*P: {Q-3*P == Point(c, frac(240, 1), frac(3718, 1))}")
    