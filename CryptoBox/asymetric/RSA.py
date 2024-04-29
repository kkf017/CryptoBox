import copy
import random
import math

from typing import List, Tuple, Union

from CryptoBox.arithmetic.prime import randprime, Euclidean
from CryptoBox.arithmetic.modulo import FastExponent



class RSA():
	def __init__(self, n=1024, p=-1, q=-1):
		self.n = n
		(self.n, self.e), self.d = self.keys(p,q)
		
	def PrivateKey(self,)->Tuple[int]:
		return (self.d)
		
	def PublicKey(self,)->Tuple[int]:
		return (self.n, self.e)
			

	def keys(self,p:int, q:int)->Tuple[Union[Tuple[int], int]]:
		"""
			Function to compute public and private key.
			Input:
				n - modulus (1024, 2048...) 
			Output:
				(n,e) - pubic key, d - private key 
		"""
		def publicKey(phi:int)->int:
			"""
				Function to compute public key.
				Input:
					phi - phi(n) = (p-1)(q-1) and n = pq 
				Output:
					e 
			opt. - A : generate e, 1<e<phi(n) with pgcd(e, phi(n))=1
			"""
			while 1:
				e = random.randint(1+1,phi-1) # get only prime numbers - randprime(1+1,phi-1)
				if 1 < e and e < phi:
					if math.gcd(e, phi) == 1:
						break
			return e


		def privateKey(e:int, phi:int)->int:
			"""
				Function to compute private key.
				Input:
					phi - phi(n) = (p-1)(q-1) and n = pq 
				Output:
					e 
			opt. - A :  ed = 1 mod phi(n) - Euclide algorithm, fast exponentiation
			"""
			pgcd, b1, b2 = Euclidean(phi, e)
			return b2
		
		if p == -1:	
			p = randprime(2, self.n//2)
		if q == -1:
			q = randprime(2, self.n//2)	
		
		n = p*q
		phi = (p-1)*(q-1)
		
		if p == q or phi <= 2:
			raise Exception("\n\033[{}m[-]Error: p, q not valid.".format("0;33"))
		
		e = publicKey(phi)
		d = privateKey(e, phi)
		
		return (n,e), d 
		

	def encrypt(self, plain:str, key:Tuple[int])->str:
		"""
			Function to encrypt a message.
			Input:
				plain - message to encrypt
				key -  public key (used to encrypt)
			Output:
				cipher (text) 
		"""
		n, e = key
		
		if type(plain) == str:
			plain = [ord(i) for i in plain]
			
		cipher = [FastExponent(i, e, n) for i in plain]
		return "".join([chr(i) for i in cipher])
		
		
	def decrypt(self, cipher:str)->str:
		"""
			Function to decrypt a message.
			Input:
				cipher - message to decrypt
				key -  private key (used to decrypt)
			Output:
				plain (text) 
		"""
		if type(cipher) == str:
			cipher = [ord(i) for i in cipher]
			
		plain = [FastExponent(i, self.d, self.n) for i in cipher]
		return "".join([chr(i) for i in plain])
		
		
	def signature(self, msg:str)->str:
		"""
			Function to compute signature.
			Input:
				msg - ...
			Output:
				signature
		"""
		def R(x:int)->int: # signature redundancy function
			return x
			
		if type(msg) == str:
			msg = [ord(i) for i in msg]
		
		sign = [R(i) for i in msg]
		sign = [FastExponent(i, self.d, self.n) for i in sign]
		sign = [chr(i) for i in sign]
		return "".join(sign)
	
	def verification(self, sign:str, msg:str, key:Tuple[int])->str:
		"""
			Function to verify signature.
			Input:
				msg -...
			Output:
				verification
		"""
		def Rinv(x:int)->int: # signature redundancy function (inv.)
			return x
			
		n, e = key
		
		if type(msg) == str:
			msg = [ord(i) for i in msg]
			
		x = [FastExponent(i, e, n) for i in msg]
		
		# Warning !! check if x E MR - send verification
		
		sign = [Rinv(i) for i in x]
		sign = [chr(i) for i in sign]
		return "".join(sign)



