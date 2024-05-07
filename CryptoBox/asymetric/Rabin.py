import random

from CryptoBox.arithmetic.prime import randprime
from CryptoBox.arithmetic.modulo import ChineseRemainder

from typing import List, Tuple, Callable


from functools import reduce

	
class Rabin():
	def __init__(self, p=-1, q=-1):
		""" len(pq) >= 1024 bits and p,q  = 3 mod 4"""
		#self.modulus = modulus
		self.n, (self.p, self.q) = self.keys(p, q)

	def PrivateKey(self,)->Tuple[int]:
		return (self.p, self.q)
		
	def PublicKey(self,)->Tuple[int]:
		return (self.n)
			
		
	def keys(self,p:int, q:int)->Tuple[int, Tuple[int]]:
		"""
			Function to compute public and private key.
			Input:
				n - modulus 
			Output:
				n - public key, (p, q) - private key
		opt.
		"""
		if p==-1 or q ==-1:
			raise Exception("\n\033[{}m[-]Error: p, q not valid.\033[0m".format("0;33"))
				
		n = p*q
		return n, (p, q)
	
	
	def encrypt(self, plain:str, key:int)->str:
		"""
			Function to encrypt a message.
			Input:
				plain - message to encrypt
				key - public key (used to encrypt)
			Output:
				cipher (text)
		opt. 
		"""
		if type(plain) == str:
			plain = [ord(i) for i in plain]
			
		cipher = [(i**2)%key for i in plain]
		return "".join([chr(i) for i in cipher])
	


	def decrypt(self, cipher:str)->List[List[str]]:
		"""
			Function to decrypt a message.
			Input:
				cipher - message to decrypt
				key - private key (used to decrypt)
			Output:
				plain (text)
					- 4 possible solutions for each char of plaintext -
		opt. use (p,q) to find 4 solutions of eq. ci = x² mod n
			  compute square root mod p and mod q 
		"""			
		if type(cipher) == str:
			cipher = [ord(i) for i in cipher]
		
		plain = [[chr(x) for x in ChineseRemainder(i, self.p, self.q)] for i in cipher]	
		return plain

	def signature(self, msg:str, R:Callable)->List[List[str]]:
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
		sign = [ord(i) for i in sign]
		
		print(f"\n\nSignature:")
		for i in sign:
			u = ChineseRemainder(i, self.p, self.q)
			v = [pow(a,2,self.n) for a in u]
			print(f"\n{i} : {u} -> {v}")
			
		sign = [[chr(x) for x in ChineseRemainder(i, self.p, self.q)] for i in sign]
		return sign
	
	def verification(self, msg:str, sign:List[List[str]], key:int)->bool:
		"""
			Function to verify signature.
			Input:
				msg - received message
				sign - signature
				key -  public key (used to decrypt)
			Output:
				verification
		"""
		def modulo(x:int, y:int)->int:
			return x - (x//y)*y
		
		print(f"\n\nVerification:")
		for i in range(len(sign)):
			n = [pow(ord(x),2,key) for x in sign[i]]	
			print(f"{ord(msg[i])} -> {n}")
			input()
		return True
