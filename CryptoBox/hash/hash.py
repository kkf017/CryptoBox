import hashlib


def md4(x: str)->None:
	"""
		Function to compute md4 (hash).
		Input:
			x - message
		Output:
			digest 
	opt. 
	"""
	return None

def md5(x: str)->str:
	"""
		Function to compute md5 (hash).
		Input:
			x - message 
		Output:
			digest 
	opt. 
	"""
	return (hashlib.md5(x.encode())).hexdigest()
	
def sha1(x: str)->str:
	"""
		Function to compute sha1 (hash).
		Input:
			x - message 
		Output:
			digest 
	opt. 
	"""
	return (hashlib.sha1(x.encode())).hexdigest()
	

def sha224(x: str)->str:
	"""
		Function to compute sha224 (hash).
		Input:
			x - message 
		Output:
			digest 
	opt. 
	"""
	return (hashlib.sha224(x.encode())).hexdigest()
	
def sha256(x: str)->str:
	"""
		Function to compute sha256 (hash).
		Input:
			x - message 
		Output:
			digest 
	opt. 
	"""
	return (hashlib.sha256(x.encode())).hexdigest()
	
def sha384(x: str)->None:
	"""
		Function to compute sha384 (hash).
		Input:
			x - message 
		Output:
			digest 
	opt. 
	"""
	return (hashlib.sha224(x.encode())).hexdigest()
	

def sha512(x: str)->str:
	"""
		Function to compute sha512 (hash).
		Input:
			x - message 
		Output:
			digest 
	opt. 
	"""
	return (hashlib.sha512(x.encode())).hexdigest()
	

def sha3_224(x: str)->str:
	"""
		Function to compute sha3_224 (hash).
		Input:
			x - message 
		Output:
			digest 
	opt. 
	"""
	return (hashlib.sha3_224(x.encode())).hexdigest()
	

def sha3_256(x: str)->str:
	"""
		Function to compute sha3_256 (hash).
		Input:
			x - message 
		Output:
			digest 
	opt. 
	"""
	return (hashlib.sha3_256(x.encode())).hexdigest()
	
def sha3_384(x: str)->str:
	"""
		Function to compute sha3_384 (hash).
		Input:
			x - message 
		Output:
			digest 
	opt. 
	"""
	return (hashlib.sha3_384(x.encode())).hexdigest()

def sha3_512(x: str)->None:
	"""
		Function to compute sha3_512 (hash).
		Input:
			x - message 
		Output:
			digest 
	opt. 
	"""
	return (hashlib.sha3_512(x.encode())).hexdigest()
	
def sha512_224(x: str)->None:
	"""
		Function to compute sha512_224 (hash).
		Input:
			x - message 
		Output:
			digest 
	opt. 
	"""
	return None

def  sha512_256(x: str)->None:
	"""
		Function to compute sha512_256 (hash).
		Input:
			x - message 
		Output:
			digest 
	opt. 
	"""
	return None


