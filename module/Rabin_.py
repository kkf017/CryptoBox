import random

from prime import randprime
from modulo import ChineseRemainder

from typing import List, Tuple


	# WARNING !!
	# See condition. 
		# func. keys(): -> generate p (prime number)
			# randprime() - range - (modulus n)
			# p*q >= 1024: # len(p*q) >= 1024 bits

BOUND = 1024
LOWER = 2
UPPER = 1024//2				
	
def keys()->Tuple[int, Tuple[int]]:
	"""
		Function to compute public and private key.
		Input:
			n - modulus 
		Output:
			n - public key, (p, q) - private key
	opt. 
	"""
	while 1:
		p = randprime(LOWER, UPPER)
		q = randprime(LOWER, UPPER)
		if p%4==3 and q%4==3 and p!=q and p*q >= BOUND: # len(p*q) >= 1024 bits
			break
	n = p*q
	return n, (p, q)
	
	
def encrypt(plain:str, key:int)->str:
	"""
		Function to encrypt a message.
		Input:
			plain - message to encrypt
			key - public key (used to encrypt)
		Output:
			cipher (text)
	opt. 
	"""
	if type(plain) == str:
		plain = [ord(i) for i in plain]
		
	cipher = [i**2%key for i in plain]
	return "".join([chr(i) for i in cipher])
	


def decrypt(cipher:str, key:Tuple[int])->List[List[str]]:
	"""
		Function to decrypt a message.
		Input:
			cipher - message to decrypt
			key - private key (used to decrypt)
		Output:
			plain (text)
				- 4 possible solutions for each char of plaintext -
	opt. use (p,q) to find 4 solutions of eq. ci = x² mod n
		  compute square root mod p and mod q 
	"""
	(p, q) = key
		
	if type(cipher) == str:
		cipher = [ord(i) for i in cipher]
	
	plain = [[chr(x) for x in ChineseRemainder(i, p, q)] for i in cipher]	
	return plain
	
"""
if __name__ == "__main__":
 
	msg = "helo:)iamurfriendsmilly."
	
	n, (p, q) = keys()
	
	cipher = encrypt(msg, n)
	print("\nEncrypt:\n{}".format(cipher))

	plain = decrypt(cipher, (p, q))
	print("\nEncrypt:".format())

	for i in range(len(msg)):
		print("{} ({}) -> {} ({}), {} ({}), {} ({}), {} ({})".format(msg[i], ord(msg[i]), plain[i][0], ord(plain[i][0]), plain[i][1], ord(plain[i][1]), plain[i][2], ord(plain[i][2]), plain[i][3], ord(plain[i][3]) ))
"""
