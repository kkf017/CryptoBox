import random

from prime import randprime
from modulo import Zn_, generators, order, FastExponent

from typing import List, Tuple, Union

	# WARNING !!
	# See condition. 
		# func. keys(): -> generate p (prime number)
			# randprime() - range - (modulus n)
			# p < 20: # len(p*q) >= 1024 bits

BOUND = 10
UPPER = 1024//2
LOWER = 2

def keys()->Tuple[Union[Tuple[int], int]]:
	"""
		Function to compute public and private key.
		Input:
			...
		Output:
			public and private keys (for encryption)
	opt.   (p, alpha, alpha^a mod p) - pubic key, a - private key
	"""
	while 1:
		p = randprime(LOWER, UPPER)
		if p > BOUND: # len(p*q) >= 1024 bits
			break
	
	zn_ = list(Zn_(p))	
	g = list(generators(p))

	# check for empty sequence
	
	alpha = random.choice(g)
	
	a = random.randint(1, p-2) 
	exp = FastExponent(alpha, a, p)
	
	return (p, alpha, exp), a


def encrypt(plain:str, key:Tuple[int])->List[Tuple[int]]:
	"""
		Function to encrypt a message.
		Input:
			plain - message to encrypt
			key -  public key (used to encrypt)
		Output:
			cipher (text) 
	"""		
	(p, alpha, exp) = key
	
	if type(plain) == str:
		plain = [ord(i) for i in plain]
	
	cipher = []	
	for x in plain:		
		k = random.randint(1, p-2)
		lambda_ = FastExponent(alpha,k,p) # lambda = alpha^k mod p
		delta = (x * FastExponent(exp,k,p))%p # delta = mi(alpha^a)^k mod p
		cipher.append((lambda_, delta))
	return cipher

	
def decrypt(cipher:List[Tuple[int]], key:int)->str:
	"""
		Function to decrypt a message.
		Input:
			cipher - message to decrypt
			key -  private key (used to decrypt)
		Output:
			plain (text) 
	"""
	(p,a) = key
	
	plain = []	
	for x in cipher:
		(lambda_, delta) = x
		pi = (FastExponent(lambda_,p-1-a,p) * delta)%p
		plain.append(chr(pi))
	return "".join(plain)

"""
if __name__ == "__main__":
	
	msg = "helo:)iamurfriendsmilly."
	#msg = "こんにちはマーフレンド"
	
	(p, alpha, exp), a = keys()
	print("\nPublic key: p {}, alpha ´{}, alpha^a mod p {}".format(p, alpha, exp))
	print("Private key: a ´{}".format(a))
	
	
	cipher = encrypt(msg, (p, alpha, exp))
	plain = decrypt(cipher, (p,a))
	
	print("\n")
	for i in range(len(cipher)):
		print("{} ({}) -> {} -> {} ({})".format(msg[i], ord(msg[i]), cipher[i], plain[i], ord(plain[i])))
	
"""
