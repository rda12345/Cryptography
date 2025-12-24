#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Elliptic_curves.py
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
        return Point(self.x, -self.y)
    
    #def __eq__(self, other):
    #    return (self.x == other.x  and self.y == other.y)
    
    #program the adition of elliptic curve points
    def __add__(self, other):
        """
        Performs the group multipicaton operator 'adding' two points on the
        elliptic curve. 
        To add two points we calculate the intersection of the line connecting
        the two points with the elliptic curve self.curve, and reflect around 
        the x-axis.
        """
        COMPLETE
        if type(other)    
    
        # case 1: adding P + (-P) = 0
        if self.y == - other.y and self.x == other.x:
            return Ideal(self.curve)     
        else:
            # case 2: addition of the same point
            if (self.x, self.y) == (other.x, other.y):
                # slope of the tangent line
                s = (3*self.x**2 + self.curve.a)/(2*self.y)
            
            # case 3: addition of two diffenent lines on the curve    
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
    
        
class Ideal(Point):
    
    def __init__(self, curve):
        self.curve = curve
    
    def __str__(self):
        return 'Ideal'
    
    def __add__(self, other):
        return other        
    
    def __neg__(self):
        return self
        
    
    

    
    
class EllipticCurve(Point):

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
    
    def __eq__(self, other):
        return (self.a, self.b) == (other.a, other.b)
    
    def __str__(self):
        return 'y^2 = x^3 + %Gx + %G' % (self.a, self.b)
    
    
    
if __name__ == "__main__":

    
    ## Case where the point is not on the curve
    #c1 = EllipticCurve(a=17, b=1)
    #print(c1)
    #p1 = Point(curve=c1, a=1, b=2)
    
    ## Case where the curve isn't smooth
    #c2 = EllipticCurve(a=0, b=0)
    
    ## Case where the point is on the curve
    #c1 = EllipticCurve(a=1, b=2)
    #p1 = Point(curve=c1, x=1, y=2)
    
    
    #TODO
    
    
    ## Check the addition of elliptic curve
    c = EllipticCurve(a=-2, b=4)
    P = Point(curve=c, x=3, y=5)
    Q = Point(curve=c, x=-2, y=0)
    print(f"Addition check: {P+Q == Point(c,0, -2)}")
    ## Check the addition of P + 0 = 0 + P = P
    O = Ideal(c)
    #print(f"Addition of zero from the left: {P + O}")
    print(f"Addition of zero from the right: {O + P}")

    #print(P+P+P)    
    
    
    
    
    
    
    