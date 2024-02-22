from CryptoBox.asymetric.RSA import RSA
from CryptoBox.asymetric.ElGamal import ElGamal
from CryptoBox.asymetric.Rabin import Rabin

	
if __name__ == "__main__":
	
	msg = "helo:)ThisismyCryptoBox."

	rsa = RSA(1024) 
	
	cipher = rsa.encrypt(msg,  (rsa.n, rsa.e))
	print("\nEncrypt:\n{}".format(cipher))
	
	plain = rsa.decrypt(cipher)
	print("\nEncrypt:\n{}".format(plain))
	
	sign = rsa.signature(msg)
	print("\nSignature: {}".format(sign))
	
	verif = rsa.verification(sign, msg, (rsa.n, rsa.e))
	print("\nVerification: {}".format(verif))
	
	
		

