import math

from prime import Euclidean, primefact

from typing import Tuple, Any

"""
	# https://www.apprendre-en-ligne.net/crypto/rabin/mvc.pdf
	# https://homepages.math.uic.edu/~leon/mcs425-s08/handouts/chinese_remainder.pdf
	# https://ccc.cs.uni-duesseldorf.de/~rothe/CRYPTOCOMPLEXITY2/folien-4-rabin.pdf
"""


class Zn(): 
	"""
		Iterator to generate Zn (set of integers modulo n).
		Input:
			n - number
		Output:
			Zn (list)
	"""
	def __init__(self,n):
		self.n = n
		self.x = 0
		
	def __iter__(self):
		return self
		
	def __next__(self):   		
		if self.x < self.n:
			y = self.x
			self.x += 1					
			return y			
		else:
			raise StopIteration

class Zn_(): 
	"""
		Iterator to generate Zn^* (multiplicative group).
		Input:
			n - number
		Output:
			Zn (list)
	opt. 
		Zn^* = {a E Zn | pgcd(a, n) = 1}
	"""
	def __init__(self,n):
		self.n = n
		self.x = 1
		
	def __iter__(self):
		return self
		
	def __next__(self):   		
		if self.x < self.n:
			while math.gcd(self.x, self.n) != 1:
				self.x+=1

			y = self.x
			self.x += 1
			return y			
		else:
			raise StopIteration
			
			
class generators(): 
	"""
		Iterator to compute generators of Zn^* (multiplicative group).
		Input:
			n - number
		Output:
			Zn (list)
	opt. 
		(the powers of a generator generates all elements in Zn^*)
	"""
	def __init__(self,n):
		self.n = n		
		self.zn_ = list(Zn_(n))
		
		self.count = 0
		
	def __iter__(self):
		return self
		
	def __next__(self):   		
		if self.count < len(self.zn_):
			
			flag = False
			while not flag:
			
				if self.count >= len(self.zn_):
					raise StopIteration
			
				x = self.zn_[self.count]
				xorder =  order(x, self.n, 1000) # change limit, for order() function !!
				y = [FastExponent(x, i, self.n) for i in range(xorder, 2*xorder)]		
				if len(y) < len(self.zn_):
					flag = False
				flag = (set(self.zn_) <= set(y))
				
				if flag:
					value = self.zn_[self.count]
				
				self.count += 1	
							
			return value			
		else:
			raise StopIteration
			

def Euler(n:int)->int:
	"""
		Function to compute Phi Euler (function).
		Input:
			n - integer
		Output:
			phi(n)
	opt.
		n = product{pi^ei}, with pi prime numbers (see prime factorization.)
		phi(n) = product{pi^ei-pi^(ei-1)}
	"""
	x = primefact(n)
	print(n,x)
	return math.prod([(p**x[p] - p**(x[p]-1)) for p in x.keys()])

def totient(n:int)->int:
	"""
		Function to compute Euler totient (function).
		Input:
			n - number 
		Output:
			result  
	opt. phi(n) is the size of the following set:
			{x | 0 < x < n, pgcd(x,n) = 1}
	"""
	return len([x for x in range(1,n) if math.gcd(x, n) == 1])
	
	
def order(x:int, n:int, limit:int)->None:
	"""
		Function to compute order (of x modulo n).
		Input:
			x, n - numbers - pgcd(x, n) = 1
		Output:
			ordn() := smallest integer - such that a^x = 1 mod n.
	opt. 
	"""
	if math.gcd(x, n) != 1:
		raise Exception("\n\033[{}m[-]Error: pgcd({},{}) has to be equal to 1.".format("0;33", x, n))
	order = 1
	while 1:
		if FastExponent(x, order, n) == 1:
			return order
			
		if order > limit:
			raise Exception("\n\033[{}m[-]Error: Order of {} mod {}, not found.".format("0;33", x, n))
		order += 1
	return order


###################################################################################################			

def ChineseRemainder(x:int, p:int, q:int)->Tuple[int]:
	"""
		Function to implement Chinese Remainder theorem.
		Input:
			x - number
			p, q - prime numbers
		Output:
	
			solution to solve eq.
	opt. 
	"""	
	n = p*q
	mp = FastExponent(x, (p+1)//4, p)
	mq = FastExponent(x, (q+1)//4, q)
	_, _, p1 = Euclidean(q, p)
	_, _, q1 = Euclidean(p, q)
	
	m1 = (mp*q*q1 + mq*p*p1)%n
	m2 = (mp*q*q1 - mq*p*p1)%n
	m3 = (- mp*q*q1 + mq*p*p1)%n
	m4 = (- mp*q*q1 - mq*p*p1)%n
	
	return m1, m2, m3, m4
	
	
def FastExponent(n:int, exp:int, mod:int)->int:
	"""
		Function to implement fast exponentation.
		Input:
			x - number
			exp - exposant
			mod - modulo
				ex. 12⁴² mod 15
		Output:
			n^exp % mod
	"""
	y = "{0:b}".format(exp)
	polynom = [i for i in range(len(y)) if int(y[-1-i])]
	return math.prod([n**i%mod for i in list(map(lambda x: 2**x, polynom))])%mod
	
"""
if __name__ == "__main__":

	# 2⁶⁴⁴ mod  645, 12⁴² mod 15
	n = 12
	exp = 42
	mod = 15
	res = FastExponent(n, exp, mod)
	print("\n{}^{} mod {} -> {}".format(n,exp,mod,res))
	
	n = 8
	print("\nZn: {}".format(list(Zn(n))))
	print("\nZn^*: {}".format(list(Zn_(n))))
	
	print("\nEuler totient function: {}".format(totient(7)))
	
	print("\norder: {}".format(order(3,10, 1000)))
	
	print("\nGenerators Zn^*: {}".format(list(generators(11))))
	
	print("\nPhi Euler: {}".format(Euler(12)))
	
"""

