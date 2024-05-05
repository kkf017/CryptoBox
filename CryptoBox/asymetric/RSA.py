import copy
import random
import math

from typing import List, Tuple, Union, Callable

from CryptoBox.arithmetic.prime import randprime, Euclidean
from CryptoBox.arithmetic.modulo import FastExponent



class RSA():
	def __init__(self, n=1024, p=-1, q=-1):
		""" p, q of size ~n/2, with sizeof(n)=1024 or sizeof(n)=2048 """
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
		opt.
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
			raise Exception("\n\033[{}m[-]Error: p, q not valid.\033[0m".format("0;33"))
		if q == -1:
			raise Exception("\n\033[{}m[-]Error: p, q not valid.\033[0m".format("0;33"))
		
		n = p*q
		phi = (p-1)*(q-1)
		
		if p == q or phi <= 2:
			raise Exception("\n\033[{}m[-]Error: p, q not valid.\033[0m".format("0;33"))
		
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
		
		
	def signature(self, msg:str, R: Callable)->str:
		"""
			Function to compute signature.
			Input:
				msg - message to sign
				R - Redundancy function (hash)
			Output:
				signature
		"""
		# compute redundancy function
		sign = R(msg)		
		sign = [ord(i) for i in sign]
		sign = [FastExponent(i, self.d, self.n) for i in sign]
		return "".join([chr(i) for i in sign])
	
	def verification(self, msg:str, sign:str, key:Tuple[int])->bool:
		"""
			Function to verify signature.
			Input:
				msg - received message
				sign - signature
				key -  public key (used to decrypt)
			Output:
				verification
		"""
		n, e = key
		check = [ord(i) for i in sign]
		check = [FastExponent(i, e, n) for i in check]
		check = "".join([chr(i) for i in check])
		if not (msg == check):
			return False
		return True



