from CryptoBox.asymetric.RSA import RSA

	
if __name__ == "__main__":

	msg = "helo:)ThisismyCryptoBox."

	rsa = RSA(1024) 
	
	cipher = rsa.encrypt(msg)
	print("\nEncrypt:\n{}".format(cipher))
	
	plain = rsa.decrypt(cipher)
	print("\nEncrypt:\n{}".format(plain))
