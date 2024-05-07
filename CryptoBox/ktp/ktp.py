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
		pass 
		
class EKE:
	def __init__(self,):
		pass
	
