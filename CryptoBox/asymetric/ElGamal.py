import random

from CryptoBox.arithmetic.prime import randprime
from CryptoBox.arithmetic.modulo import Zn_, generators, order, FastExponent

from typing import List, Tuple, Union


BOUND = 60
UPPER = 256
LOWER = 20

class ElGamal():
	def __init__(self,):
		(self.p, self.alpha, self.exp), self.a = self.keys()

	def keys(self,)->Tuple[Union[Tuple[int], int]]:
		"""
			Function to compute public and private key.
			Input:
				...
			Output:
				public and private keys (for encryption)
		opt.   (p, alpha, alpha^a mod p) - pubic key, a - private key
		"""
		while 1:
			p = randprime(LOWER, UPPER)
			if p > BOUND: # len(p*q) >= 1024 bits
				break
		
		zn_ = list(Zn_(p))	
		g = list(generators(p))
		
		# check for empty sequence
		
		alpha = random.choice(g)
		
		a = random.randint(1, p-2) 
		exp = FastExponent(alpha, a, p)
		
		return (p, alpha, exp), a


	def encrypt(self, plain:str, key:Tuple[int])->List[Tuple[int]]:
		"""
			Function to encrypt a message.
			Input:
				plain - message to encrypt
			Output:
				cipher (text) 
		"""
		(p, alpha, exp) = key
			
		if type(plain) == str:
			plain = [ord(i) for i in plain]
		
		cipher = []	
		for x in plain:		
			k = random.randint(1, p-2)
			lambda_ = FastExponent(alpha,k,p) # lambda = alpha^k mod p
			delta = (x * FastExponent(exp,k,p))%p # delta = mi(alpha^a)^k mod p
			cipher.append((lambda_, delta))
		return cipher

	
	def decrypt(self, cipher:List[Tuple[int]])->str:
		"""
			Function to decrypt a message.
			Input:
				cipher - message to decrypt
			Output:
				plain (text) 
		"""
		plain = []	
		for x in cipher:
			(lambda_, delta) = x
			pi = (FastExponent(lambda_,self.p-1-self.a,self.p) * delta)%self.p
			plain.append(chr(pi))
		return "".join(plain)
		
		
	def signature(self,)->None:
		"""
			Function to compute signature.
			Input:
				cipher - ...
			Output:
				...
		"""
		def R()->None: 
			return None
		return None
	
	def verification(self,)->None:
		"""
			Function to verify signature.
			Input:
				cipher -...
			Output:
				...
		"""
		return None
	
