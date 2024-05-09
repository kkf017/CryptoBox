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
			
		
		
##################################################################################################
# EKE
	
class EKEA:
	def __init__(self, password, asym, sym):
		self.password = password
		self.A = asym
		self.B = sym
		
	def KeyPublic(self, )->Tuple[int]:
		if type((self.A).PublicKey()) == int:
			i = (self.A).PublicKey()
			return (self.B).encrypt(str(i), self.password)
		
		elif type((self.A).PublicKey()) == tuple:
			keys = tuple([(self.B).encrypt(str(i), self.password) for i in (self.A).PublicKey()])
			return keys
		
		else:
			raise Exception("\n\033[0;33m[-]Error: Unknown type for KeyPublic.\033[0m")

	def KeySession(self, key:str)->str:				
		key = (self.B).decrypt(key, self.password) # symetric
		#key = ascii((self.A).decrypt(key)) # asymetric
		self.k = key
		return self.k
	
	def RandomNumber(self,)->Tuple[str]:
		self.ra = str(random.randint(0,65536))
		return ((self.B).encrypt(self.ra, self.k), (self.B).encrypt(self.k, self.k))
	
	def check(self, rb:str, ra:str)->str:
		ra = (self.B).decrypt(ra, self.k)
		if not (ra == self.ra):
			#raise Exception("\n\033[0;33m[-]Error: Random number ra are not equal (for A and B).\033[0m")
			return ("\033[0;31mError for ra.\033[0m")
		rb = eval((self.B).decrypt(rb, self.k))
		return (self.B).encrypt(str(rb), self.k)
			
			
			

class EKEB:
	def __init__(self, password, asym, sym):
		self.password = password
		self.A = asym
		self.B = sym

	
	def KeyPublic(self, pub:Tuple[int])->Tuple[int]:
		if type(pub) == str:
			self.pub = int((self.B).decrypt(pub, self.password), base=10)
			#self.pub = eval((self.B).decrypt(pub, self.password))
		
		elif type(pub) == tuple:
			self.pub = tuple([int((self.B).decrypt(i, self.password), base=10) for i in pub])
			#self.pub = tuple([eval((self.B).decrypt(i, self.password)) for i in pub])
		else:
			raise Exception("\n\033[0;33m[-]Error: Unknown type for KeyPublic.\033[0m")
		return ()
		

	def KeySession(self, n:int)->str:
		#key = ascii("".join([random.choice(string.printable) for _ in range(n)]))[:n]
		key = ascii("".join([chr(random.randint(0,65536)) for _ in range(n)]))[:n]
		self.k = key
		#key = (self.A).encrypt(key, self.pub) # asymetric
		key = (self.B).encrypt(key, self.password) # symetric
		return key

	def RandomNumber(self, ra:str, k:str)->Tuple[str]:
		# check session
		k = (self.B).decrypt(k, self.k)
		if not (self.k == k):
			raise Exception("\n\033[0;33m[-]Error: Key session are different (for A and B).\033[0m")
			#return ("\033[0;31mError\033[0m")
		self.ra = eval((self.B).decrypt(ra, self.k)) # int(, base=10)
		self.rb = random.randint(0,65536)
		return  ((self.B).encrypt(str(self.rb), self.k), (self.B).encrypt(str(self.ra), self.k))

	def check(self,rb:str)->str:
		rb = eval((self.B).decrypt(rb, self.k))
		if not (self.rb == rb):
			#raise Exception("\n\033[0;33m[-]Error: Random number ra are not equal (for A and B).\033[0m")
			return "\033[0;31mError\033[0m"
		return "\033[0;32mOK\033[0m"

class EKE:
	def __init__(self, password, asym, sym, profile):
		match profile:
			case "A":
				self.eke = EKEA(password, asym, sym)
			case "B":
				self.eke = EKEB(password, asym, sym)
			case _:
				raise Exception("\n\033[0;33m[-]Error: Unknown profile for EKE (only A or B).\033[0m")
				
	def KeyPublic(self,*args:Tuple[Any])->Tuple[int]:
		return (self.eke).KeyPublic(*args)
	
	def KeySession(self, *args:Tuple[Any])->str:
		return (self.eke).KeySession(*args)

	def RandomNumber(self, *args:Tuple[Any])->Tuple[str]:
		return (self.eke).RandomNumber(*args)

	def check(self, *args:Tuple[Any])->str:
		return (self.eke).check(*args)
	
		
################################################################################################
	
