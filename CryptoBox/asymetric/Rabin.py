import random

from CryptoBox.arithmetic.prime import randprime
from CryptoBox.arithmetic.modulo import ChineseRemainder

from typing import List, Tuple, Callable


from functools import reduce

	
class Rabin():
	def __init__(self, p=-1, q=-1):
		""" len(pq) >= 1024 bits """
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
			
		cipher = [i**2%key for i in plain]
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

	def signature(self, msg:str, R:Callable, n)->List[List[str]]:
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
		
		def ChineseRemainderXXX(m:List[int], a: List[int])->None:
			def mul_inv(x, b):
				b0 = b
				x0, x1 = 0, 1
				if b == 1: return 1
				while x > 1:
					q = x // b
					x, b = b, x%b
					x0, x1 = x1 - q * x0, x0
				if x1 < 0: x1 += b0
				return x1
			sum = 0
			prod = reduce(lambda acc, b: acc*b, m)
			for n_i, a_i in zip(m, a):
				p = prod // n_i
				sum += a_i * mul_inv(p, n_i) * p
			return sum % prod
	
			
		sign = R(msg)
		sign = [ord(i) for i in sign]
		#sign = [[chr(x) for x in ChineseRemainder(i, self.p, self.q)] for i in sign]
		
		for i in sign:
			print(f"\n{i} : {[modulo(x**2, n) for x in ChineseRemainder(i, self.p, self.q)]}")
			#x = ChineseRemainderXXX([self.p, self.q], [i**((self.p+1)/4), i**((self.q+1)/4)])
			#print(f"{x}")
			input()
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
			
		for i in range(len(sign)):
			print("\n\n")
			for x in sign[i]:
				print(f"{i}, {ord(msg[i])} {(ord(x))**2%key} : {ord(x)} {ord(x)**2} - {key}")
				input()
		return True
