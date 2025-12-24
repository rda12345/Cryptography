#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
RSA 

Setup:
    The algorithm uses two different keys
    1. Public key - shared with everyone
    2. Private key - kept secret
    Data encrypted by the public key can only be decrypted with the private key
    and vice versa.
    
The algorithm includes the following steps:
    1. Pick two large primes: p and q
    2. Compute their product n = p * q
    3. Compute Euler's totient, phi(n), i.e, the number of number co-prime to n between 1 and n.
        phi(n) = (p-1)*(q-1)
    4. Chose a public exponent, 1 < e < phi(n), coprime to ph(n)
    5. Compute the private exponent d (modular inverse of e mod phi(n))
    
    Public key: (e,n)
    Private key: (d,n)
    
Encyrption: sending a message m<n, the sender evaluates c = m^e mod n.
Decyrption: Reciever computes m = c^d mod n.

The algorithm works since e*d = 1 mod phi(n), therefore 
e*d = 1 phi(n)*k, as a result m^{ed} = m*(m^{phi(n)})^k, Euler's theorem states that
m^phi(n) = 1 mod n, therefore m^{ed} = m mod n
    
Digital signatures with RSA:
    
"""

class SimpleRSA(object):
    """Simple implementation of the RSA algorithm"""
    
    def __init__(self, n, e, d):
        self.public_key = (e,n)
        self.private_key = (d,n)
    
        
    def encode(self, messege):
        """
        Encodes the messege using the public key
        Parameters:
            messege: int, the messege to be encrypted
            e: int
            n: int
        """
        e, n = self.public_key
        return messege**e % n 
        
    def decode(self, encoded_messege):
        """
        Decodes the messege using the private key   
        Parameters:
            encoded_messege: int, the messege to be dencrypted 
            d: int, modular inverse of e w.r.t. phi(n)
            n: int
        """
        d, n = self.private_key
        return encoded_messege**d % n

#--------------------------------- Long bits RSA ------------------------------


class RSA(object):
    """Implementation of RSA, employing long bit strings"""

    NameError("Not yet implemented")
    
    
if __name__ == "__main__":
    messege = 10
    p = 11
    q = 17 
    n = p * q
    phi = (p-1)*(q-1)
    e = 7
    d = 23 
    rsa = SimpleRSA(n, e, d)
    encoded_messege = rsa.encode(messege)
    decrypted_messege = rsa.decode(encoded_messege)
    
    print(f'messege: {messege}')
    print(f'encoded messege: {encoded_messege}')
    print(f'decrypted messege: {decrypted_messege}')


