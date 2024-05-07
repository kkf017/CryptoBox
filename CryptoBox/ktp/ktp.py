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
	def __init__(self, A):
		self.A = A
		
	def PrivateKey(self,)->Tuple[int]:
		return self.A.PrivateKey()
		
	def PublicKey(self,)->Tuple[int]:
		return self.A.PublicKey()
	
	def exchange(self, key:Tuple[int], *args:Tuple[str])->Tuple[int]:
		pass
	
	def verification(self, key:Tuple[int], *args:Tuple[int])->Tuple[int]:
		pass 
		
class EKE:
	def __init__(self,):
		pass
	
