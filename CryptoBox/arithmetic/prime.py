import copy
import random
import math

from typing import List, Tuple, Dict


class primerange(): 
	"""
		Iterator to generate prime numbers (in a range).
		Input:
			upper - upper bound of the interval
			lower - lower bound of the interval
		Output:
			prime number (list)
	"""
	def __init__(self, lower, upper, step=1):
		self.x = lower
		self.upper = upper 
		self.step = step

		self.primes = []
		
	def __iter__(self):
		return self
		
	def __next__(self):   		
		if self.x < self.upper:
			y = self.x					
			while 1:
				if y >= self.upper:
					raise StopIteration
					
				flag = True
				if y > 1:
					for i in self.primes:
						if y % i == 0:
							flag = False
				else:
					flag = False
	
								
				if flag:
					self.primes.append(y)
					self.x = y
					break
					
				y += self.step
			return self.x			
		else:
			raise StopIteration
			
			
def isprime(n:int)->bool:
	"""
		Function to check if a number is prime (or not).
		Input:
			n - number to check
		Output:
			bool
	"""
	if n > 1:
		for i in primerange(2,n): #range(2, n):
			if n % i == 0:
				return False
		return True
	return False

			

def randprime(lower:int, upper:int)->int:
	"""
		Function to generate (random) prime number (in a range).
		Input:
			upper - upper bound of the interval
			lower - lower bound of the interval
		Output:
			prime number (random)
	"""
	x = list(primerange(lower, upper))
	n = random.randint(0, len(x)-1)		
	return x[n]
	


def Fermat(n:int)->Tuple[int]:
	"""
		Function to implement Fermat factorization (of a number).
		Input:
			x - number
		Output:
			factorization (prime number)
	opt. 
	"""
	if n == 0:
		return 0, 0
	if n%2==0:
		return 2, n//2
	
	if int(math.sqrt(n))**2 == n:
		return math.sqrt(n), math.sqrt(n)
		
	x = math.ceil(math.sqrt(n))
	while 1:
		y = int(math.sqrt(x**2-n))
		if y**2 == x**2-n:
			break
		else:
			x += 1
	return x - y, x + y
	

def primefact(n:int)->Dict[int, int]:
	"""
		Function to get prime number factorization (of a number).
		Input:
			x - number
		Output:
			factorization (prime number)
	opt. 
	"""
	def getfact(n:int)->List[int]:
		fact = []
		
		a, b = Fermat(n)
		
		if isprime(a) or a==1: # a == 0
			fact.append(a)
		if isprime(b) or b ==1: # b == 0
			fact.append(b)
		
		if not isprime(a) and a != 1: # a != 0
			x = primefact(a)
			fact += x
		if not isprime(b) and b != 1: # b != 0
			x = primefact(b)
			fact += x			
		return fact
		
	primes = getfact(n)
	fact = {}
	for i in set(primes):
		fact[i] = primes.count(i)
	return fact
		
	
def Euclidean(x:int, y:int)->Tuple[int]:
	"""
		Function to implement Euclid algorithm (extend.).
		Input:
			x, y - input for Bezout formula
		Output:
			pgcd(), Bezout coeff.
	opt. u*e + v*phi(n) = pgcd(e, phi(n))
	         ed = 1 mod phi(n)
	"""	
	if math.gcd(x, y) != 1:
		raise Exception("\n\033[{}m[-]Error: pgcd({},{}) has to be equal to 1.".format("0;33", x, y))
		
	r = [x, y]
	s = [1, 0]
	t = [0, 1]
	q = [-1, x//y]
		
	i = 1
	while 1:
		
		ri = r[i-1] - q[i] * r[i]		
		si = s[i-1] - q[i] * s[i]		
		ti = t[i-1] - q[i]*t[i]
				
		if ri == 0:
			break

		qi = r[i] // ri
		
		r.append(ri)
		s.append(si)
		t.append(ti)
		q.append(qi)
				
		i += 1
	
	if s[i] < 0:
		s[i] = s[i]%y
	if t[i] < 0:
		t[i] = t[i]%x
		
	return r[i], s[i], t[i]
			

		




	
