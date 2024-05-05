import math
import random

from CryptoBox.arithmetic.prime import randprime, Euclidean
from CryptoBox.arithmetic.modulo import Zn_, generators, order, FastExponent

from typing import List, Tuple, Union, Callable



class ElGamal():
	def __init__(self, p=-1, order=1000):
		""" len(p) >= 1024 bits """
		self.order = order
		(self.p, self.alpha, self.exp), self.a = self.keys(p)

	def PrivateKey(self,)->Tuple[int]:
		return (self.a)
		
	def PublicKey(self,)->Tuple[int]:
		return (self.p, self.alpha, self.exp)


	def keys(self, p:int)->Tuple[Union[Tuple[int], int]]:
		"""
			Function to compute public and private key.
			Input:
				...
			Output:
				public and private keys (for encryption)
		opt. 
		"""		
		if p == -1:
			raise Exception("\n\033[{}m[-]Error: p not valid.\033[0m".format("0;33"))
			
		zn_ = list(Zn_(p))	
		g = list(generators(p, self.order))
			
		# check for empty sequence
		if g == []:
			raise Exception("\n\033[{}m[-]Error: no generator of multiplicative group found (p not valid).\033[0m".format("0;33"))
		
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
		
		
	def signature(self, msg:str, R:Callable)->Tuple[str]:
		"""
			Function to compute signature.
			Input:
				msg - message to sign
				R - Redundancy function (hash)
			Output:
				signature
		"""
		def modulo(x:int, y:int)->int:
			return x - (x//y)*y
			
		sign = R(msg)
		
		while 1:
			x = random.randint(1, self.p-2)
			if math.gcd(x, self.p-1) == 1:
				break
		_, x1, _ = Euclidean(x,self.p-1)
	
		r = FastExponent(self.alpha, x, self.p)
		s = [modulo(x1*(ord(mi)-self.a*r), self.p-1)  for mi in sign]
		
		s = "".join([chr(i) for i in s])
		
		return r, s
	
	def verification(self, msg:str, sign:Tuple[str], key:int)->bool:
		"""
			Function to verify signature.
			Input:
				msg - received message
				sign - signature
				key -  public key (used to decrypt)
			Output:
				verification
		
		# https://github.com/jnyryan/elgamal-digital-signiture/blob/master/elsig.py
		"""
		def modulo(x:int, y:int)->int:
			return x - (x//y)*y
			
		(p, alpha, exp) = key
		(r, s) = sign
		
		if not (1<=r and r<=self.p-2):
			return False
			
		v1 =  [(FastExponent(exp,r,p)*FastExponent(r,ord(i),p)) % p for i in s]
		v1 = "".join([chr(i) for i in v1])
		
		v2 = [FastExponent(alpha, ord(i), p) for i in msg]
		v2 = "".join([chr(i) for i in v2])

		if not (v1 == v2):
			return False
		return True
	
