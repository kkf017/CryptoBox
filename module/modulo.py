import math

from prime import Euclidean

from typing import Tuple



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
	
	p = 43
	q = 47
	n =  p*q
	x = 741
	m1, m2, m3, m4 = ChineseRemainder(x**2%n, 43, 47)
"""
