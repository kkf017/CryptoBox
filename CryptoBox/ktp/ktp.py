import random

from CryptoBox.arithmetic.prime import randprime
from CryptoBox.arithmetic.modulo import generators, FastExponent

from typing import Tuple, Any




class DiffieHellman:
	def __init__(self, p: int, alpha: int):
		self.p = p # prime number
		self.alpha = alpha # generator of Zp
	
	def word(self, x:int)->None:
		self.secret = x
		self.exp = FastExponent(self.alpha, x, self.p)
	
	def key(self, beta:int)->None:
		self.key = FastExponent(beta, self.secret, self.p)
		


class NeedhamSchroeder:
	def __init__(self, A, hash):
		self.A = A
		self.hash = hash
	
	def PrivateKey(self,)->Tuple[int]:
		return self.A.PrivateKey()
	
	def PublicKey(self,)->Tuple[int]:
		return self.A.PublicKey()
		
	def exchange(self,key:Tuple[int], *args:Tuple[int])->Tuple[str]:
		def exchangeA(key:Tuple[int], k:int)->Tuple[int]:
			self.k1 = k
			return self.A.encrypt(self.k1, key)
			
		def exchangeB(key:Tuple[int], k:int, k1:int)->Tuple[int]:
			self.k2 = k
			self.k1 = (self.A).decrypt(k1)
			return (self.A).encrypt(self.k1,key), (self.A).encrypt(self.k2,key)
		
		if len(args) == 1:
			return exchangeA(key, args[0])
		if len(args) > 1:
			return exchangeB(key, args[0], args[1])
	
	
	def verification(self,key:Tuple[int], *args:Tuple[int])->Tuple[str]:
		def verificationA(key:Tuple[int], k1:int, k2:int)->Tuple[int]:
			a1 = (self.A).decrypt(k1)
			self.k2 = (self.A).decrypt(k2)
			if not (a1 == self.k1):
				return "Error"
			self.key = self.hash(self.k1+self.k2)
			return (self.A).encrypt(self.k2, key)
		
		def verificationB(key:Tuple[int], k2:int)->Tuple[int]:
			b1 = (self.A).decrypt(k2)
			if not (b1 == self.k2):
				return "Error"
			self.key = self.hash(self.k1+self.k2)
	
		if len(args) == 1:
			return verificationB(key, args[0])
		if len(args) > 1:
			return verificationA(key, args[0], args[1])
			
		
		
class EKE:
	def __init__(self,):
		pass
	
