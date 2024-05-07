from CryptoBox.asymetric.RSA import RSA
from CryptoBox.asymetric.ElGamal import ElGamal
from CryptoBox.asymetric.Rabin import Rabin

from CryptoBox.arithmetic.prime import *
from CryptoBox.arithmetic.modulo import *
from CryptoBox.hash.hash import *

import random
import string
import hashlib




def rstring(n:int, mode:str)->str:
	""" Function to generate random string of n ascii/utf-8 char."""
	match mode:
		case "ascii":
			return "".join([random.choice(string.printable) for _ in range(n)])
		case "utf8":
			return "".join([chr(random.randint(0,65536)) for _ in range(n)])
		case _ :
			raise Exception("\033[{}m[-]Error: Unknown type of char. \033[0m".format("0;33"))



def falsify(msg:str)->str:
	""" Function to modify a string."""
	return msg.replace(msg[random.randint(0, len(msg)-1)], random.choice(string.printable))

def randrandprime(lower:int, upper:int, order:int)->int:
	""" Function to generate random prime number (for ElGamal) """
	while 1:
		p = randprime(lower, upper)
		
		if p%4 == 3:
			zn_ = list(Zn_(p))	
			g = list(generators(p, order))
				
			if not (g == []):
				break
	return p
	
	
if __name__ == "__main__":
	 
	for i in range(1): 
		
		msg = ascii(rstring(20, "utf8"))

		########### Verification for encryption ###########
		
		""" Prime numbers for key generation """
		#p=[3041,131,1021,113]
		#p=[191, 21001, 251, 1051]
		#p=[113, 701, 251, 1051]
		#p = [randrandprime(124,1024,1000) for i in range(4)]
		p = [randrandprime(60,1024,1000) for i in range(4)]
		
		
		print(f"Primary: {p[0]},{p[1]}, {p[2]},{p[3]}")
		
		""" Choice of method of encryption """
		#A = RSA(n=1024, p=p[0], q=p[1])
		#B = RSA(n=1024, p=p[2], q=p[3])
		
		A = Rabin(p=p[0], q=p[1])
		B = Rabin(p=p[2], q=p[3])
		
		#A = ElGamal(p=p[0],order=1000)
		#B = ElGamal(p=p[1],order=1000)
	
		
		""" Test of encryption/decryption """		
		cipher = A.encrypt(msg, B.PublicKey())
		plain = B.decrypt(cipher)

		#print(f"Msg : {msg}")
		#print(f"Plain : {plain}")
		
		""" Verification for RSA, ElGamal """
		#if not (msg == plain):
			#print(f"\033[0;33m[-]Error: encryption/decryption not working.\033[0m")
			#break
		
		""" Verification for Rabin """
			
		for j in range(len(plain)):
			if not (msg[j] in plain[j]):
				print(f"\033[0;33m[-]Error: encryption/decryption not working.\033[0m")
				for n in range(len(plain)):
					print(f"{msg[n]} : {plain[n]}")
				break
		
		
		########### Verification for signature ###########
		
		""" Select redundancy function (hash) from hashlib """
		R = sha1 #(hashlib.sha1(x.encode())).hexdigest()
		
		
		encode = R(msg)
		flag = random.randint(0,1)
		if flag == 0:
			encode = R(falsify(msg))
		
		sign = A.signature(msg, R)
		verif = B.verification(encode, sign, A.PublicKey())
		
		#print(f"Signature: {flag} {sign}")

		if (flag == 0 and verif == True) or (flag == 1 and verif == False):
			print(f"\033[0;35m[-]Error: signature not working. \033[0m")
			#break
		
		
		print(f"\033[0;34m[+]Done : test {i} \033[0m.\n")
		#input()
		

		

	

	
	
		

