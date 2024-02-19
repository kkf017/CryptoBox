import random

from prime import randprime
from modulo import ChineseRemainder

from typing import Tuple
	
	
def keys(n:int)->Tuple[int, Tuple[int]]:
	"""
		Function to compute public and private key.
		Input:
			n - modulus 
		Output:
			n - public key, (p, q) - private key
	opt. 
	"""
	while 1:
		p = randprime(2, n//2)
		q = randprime(2,n//2)
		if p*q >= 1024: # len(p*q) >= 1024
			break
	n = p*q
	print("\np {}, q {}, n {}".format(p,q,n))
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
	


def decrypt(cipher:str, key:Tuple[int])->None:
	"""
		Function to decrypt a message.
		Input:
			cipher - message to decrypt
			key - private key (used to decrypt)
		Output:
			plain (text)
	opt. use (p,q) to find 4 solutions of eq. ci = x² mod n
		  compute square root mod p and mod q 
	"""
	(p, q) = key
		
	if type(cipher) == str:
		cipher = [ord(i) for i in cipher]
	
	plain = []	
	for i in cipher:
		x1, x2, x3, x4 = ChineseRemainder(i, p, q)
		x = "".join([chr(x1), chr(x2), chr(x3), chr(x4)])
		print(i, "->", x1, x2, x3, x4)	
	return None

if __name__ == "__main__":
 
	msg = "helo:)iamurfriendsmilly."
	print("\nPlain:")
	for i in msg:
		print("{}->{}".format(i, ord(i)))
	
	n, (p, q) = keys(1024)
	
	cipher = encrypt(msg, n)
	print("\nEncrypt:\n{}".format(cipher))

	plain = decrypt(cipher, (p, q)) # not working !!
	print("\nEncrypt:\n{}".format(plain))
