import random
import string
import hashlib

from CryptoBox.asymetric.RSA import RSA
from CryptoBox.asymetric.ElGamal import ElGamal
from CryptoBox.asymetric.Rabin import Rabin

from CryptoBox.arithmetic.prime import *
from CryptoBox.arithmetic.modulo import *


from typing import Callable



def randprimesss(lower:int, upper:int, order:int)->int:
	""" Function to generate random prime number (for Rabin) """
	while 1:
		p = randprime(lower, upper)
		if p%4 == 3:	
			if not (list(generators(p, order)) == []):
				break
	return p


def randprimess(lower:int, upper:int, order:int)->int:
	""" Function to generate random prime number (for ElGamal) """
	while 1:
		p = randprime(lower, upper)
		if not (list(generators(p, order)) == []):
				break
	return p


def randprimes(rand:Callable, lower:int, upper:int, order:int, n:int)->List[int]:
	primes = []			
	while  1:
		x = rand(60,1024,1000)
		if not x in primes:
			primes.append(x)
		if len(primes) == 4:
			break
	return	primes
	
	
	
if __name__ == "__main__":
	
	error = 0
	count = 1
	for i in range(count): 
		
		err = False
		
		n = random.randint(10,64)
		#msg = ascii("".join([random.choice(string.printable) for _ in range(n)]))
		msg = ascii("".join([chr(random.randint(0,65536)) for _ in range(n)]))
	
		########### Verification for encryption ###########
		
		""" Prime numbers for key generation """
		p = randprimes(randprimesss, 60, 1024, 1000, 4)
		print(f"Primary: {p[0]},{p[1]}, {p[2]},{p[3]}")
		
		""" Choice of method of encryption """
		A = RSA(n=1024, p=p[0], q=p[1])
		B = RSA(n=1024, p=p[2], q=p[3])
		
		#A = Rabin(p=p[0], q=p[1])
		#B = Rabin(p=p[2], q=p[3])
		
		#A = ElGamal(p=p[0],order=1000)
		#B = ElGamal(p=p[1],order=1000)
	
		
		""" Test of encryption/decryption """		
		cipher = A.encrypt(msg, B.PublicKey())
		plain = B.decrypt(cipher)
		
		
		""" Verification for RSA, ElGamal """
		
		if not (msg == plain):
			print(f"\033[0;33m[-]Error: encryption/decryption not working.\033[0m")
			err = True
			#break
		
		""" Verification for Rabin """
		"""	
		for j in range(len(plain)):
			if not (msg[j] in plain[j]):
				print(f"\033[0;33m[-]Error: encryption/decryption not working.\033[0m")
				#for n in range(len(plain)):
					#print(f"{msg[n]} : {plain[n]}")
				break
		
		"""
		########### Verification for signature ###########
		
		""" Select redundancy function (hash) from hashlib """
		sha1 = lambda x: (hashlib.sha1(x.encode())).hexdigest()
		R = sha1 
		
		""" Falsify message (or not) """
		
		sign = A.signature(msg, R)
		
		flag = random.randint(0,1)
		if flag == 0:
			sign = sign.replace(sign[random.randint(0, len(sign)-1)], random.choice(string.printable))
		
	
		verif = B.verification(R(msg), sign, A.PublicKey())

		if (flag == 0 and verif == True) or (flag == 1 and verif == False):
			print(f"\033[0;35m[-]Error: signature not working. \033[0m")
			err = True
			#break
	
			
		if err:
			error += 1
		print(f"\033[0;34m[+]Done : test {i} ({error}/{(i+1)})\033[0m.\n")
		#input()
	
	print(f"\033[0;34mError: {error}/{count}.\033[0m\n")
		

		

	

	
	
		

