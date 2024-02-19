import copy
import random
import math

from typing import List, Tuple, Union

from prime import randprime, Euclidean
from modulo import FastExponent

		

def publicKey(phi:int)->int:
	"""
		Function to compute public key.
		Input:
			phi - phi(n) = (p-1)(q-1) and n = pq 
		Output:
			e 
	opt. - A : generate e, 1<e<phi(n) with pgcd(e, phi(n))=1
	"""
	while 1:
		e = random.randint(1+1,phi-1) # get only prime numbers - randprime(1+1,phi-1)
		if 1 < e and e < phi:
			if math.gcd(e, phi) == 1:
				break
	return e


def privateKey(e:int, phi:int)->int:
	"""
		Function to compute private key.
		Input:
			phi - phi(n) = (p-1)(q-1) and n = pq 
		Output:
			e 
	opt. - A :  ed = 1 mod phi(n) - Euclide algorithm, fast exponentiation
	"""
	pgcd, b1, b2 = Euclidean(phi, e)
	return b2
	

def keys(n:int)->Tuple[Union[Tuple[int], int]]:
	"""
		Function to compute public and private key.
		Input:
			n - modulus (1024, 2048...) 
		Output:
			(n,e) - pubic key, d - private key 
	"""
	p = randprime(2, n//2)
	q = randprime(2,n//2)	
	
	n = p*q
	phi = (p-1)*(q-1)
	
	if p == q or phi <= 2:
		raise Exception("\n\033[{}m[-]Error: p, q not valid.".format("0;33"))
	
	e = publicKey(phi)
	d = privateKey(e, phi)
	
	return (n,e), d 
	

def encrypt(plain:str, key:Tuple[int])->str:
	"""
		Function to encrypt a message.
		Input:
			plain - message to encrypt
			key -  public key (used to encrypted)
		Output:
			cipher (text) 
	"""
	n, e = key
	
	if type(plain) == str:
		plain = [ord(i) for i in plain]
		
	cipher = [FastExponent(i, e, n) for i in plain]
	return "".join([chr(i) for i in cipher])
	
	
def decrypt(cipher:str, key:Tuple[int])->str:
	"""
		Function to decrypt a message.
		Input:
			cipher - message to decrypt
			key -  private key (used to decrypted)
		Output:
			plain (text) 
	"""
	n, d = key
	
	if type(cipher) == str:
		cipher = [ord(i) for i in cipher]
		
	plain = [FastExponent(i, d, n) for i in cipher]
	return "".join([chr(i) for i in plain])
	

"""
if __name__ == "__main__":
	
	msg = "helo:)iamurfriendsmilly."
	
	n = 1024 # 1024, 2048 

	(n,e), d = keys(n)
	
	cipher = encrypt(msg, (n,e))
	print("\nEncrypt:\n{}".format(cipher))
"""
	
	plain = decrypt(cipher, (n,d))
	print("\nEncrypt:\n{}".format(plain))

