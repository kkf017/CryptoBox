import copy
import math

from typing import List



def polynom(x:int)->List[int]:
	binary = "{0:b}".format(x)	
	y = [i for i in range(len(binary)) if int(binary[-1-i]) == 1]
	y.reverse()
	return y
	
	
def summ(x:List[int], y:List[int])->List[int]:
	res = x + y
	res =  [i for i in set(res) if res.count(i)%2 == 1]
	res.sort()
	res.reverse()
	return res

def product(x:List[int], y:List[int])->List[int]:
	prod = [i+j for i in x for j in y]
	simp = [i for i in set(prod) if prod.count(i)%2 == 1]
	simp.sort()
	simp.reverse()
	return simp

def reduct(x:List[int])->List[int]:
	# P(X)=X⁸+X⁴+X³+X+1
	P = polynom(283)
	deg = x[0]-P[0]
	PX = product(P, [deg])
	res = summ(x,PX)
	return res	

def gf8(x:int, y:int)->int:
	x = polynom(x) 
	y = polynom(y)
	res = product(x,y)
	if res == []:
		return 0
	while(res[0]>7):
		res = reduct(res)
	return sum([2**i for i in res])


def mult2vect(x:List[int], y:List[int])->str:
	prod = [gf8(x[i], y[i]) for i in range(len(x))]
	res = prod[0]^prod[1]
	for i in range(2,len(prod)):
		res = res ^ prod[i]
	return res

def galois(X:str, mtx:List[int])->str:
	res = []
	X = [ord(i) for i in X]
	N = int(math.sqrt(len(mtx)))
	for i in range(N):
		x = mtx[i*N:N*i+(N-1)+1]
		for j in range(N):
			y = [X[0+j], X[N+j], X[2*N+j], X[3*N+j]]
			xy = mult2vect(x, y)
			res.append(chr(xy))
	return "".join(res)

	
