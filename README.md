# CryptoBox
Toolbox for cryptography.

### Libraries
* Requires python>=3.5 and hashlib library.

### Example

#### Arithmetic

It contains the **prime module** to perform operations with prime numbers. (see documentation)<br />


It also contains the **modulo module** to perform operations with modulo. (see documentation)<br />


#### Symmetric

This module contains **symmetric functions** for encryption.

```python
from CryptoBox.symetric.AES128 import AES128
from CryptoBox.symetric.AES256 import AES256

if __name__ == "__main__":

    key = "Hi<3iamurfriend."
    msg = "helo:)ThisismyCryptoBox."
    	
    aes = AES128()
    	
    cipher = aes.encrypt(msg, key)
    plain = aes.decrypt(cipher, key)
    	
    print(f"Msg : {msg}")
    print(f"Plain : {plain}")
```



#### Asymmetric
This module contains **asymmetric functions** for encryption.

###### Example 1
```python
from CryptoBox.arithmetic.prime import randprime
from CryptoBox.asymetric.RSA import RSA

if __name__ == "__main__":

    msg = "helo:)ThisismyCryptoBox."
    
    A = RSA(n=1024, p=3041, q=131)
    B = RSA(n=1024, p=1021, q=113)
    		
    cipher = A.encrypt(msg, B.PublicKey())
    plain = B.decrypt(cipher)
    
    print(f"Msg : {msg}")
    print(f"Plain : {plain}")
```

###### Example 2
```python
from CryptoBox.asymetric.Rabin import Rabin

if __name__ == "__main__":

    msg = "helo:)ThisismyCryptoBox."
    
    A = Rabin(p=191, q=21001)
    B = Rabin(p=251, q=1051)
    		
    cipher = A.encrypt(msg, B.PublicKey())
    plain = B.decrypt(cipher)
    
    print(f"Msg : {msg}")
    print(f"Plain : {plain}")

```


###### Example 3
```python
from CryptoBox.arithmetic.prime import randprime
from CryptoBox.asymetric.ElGamal import ElGamal

if __name__ == "__main__":

    msg = "helo:)ThisismyCryptoBox."
    
    A = ElGamal(p=113, order=100)
    B = ElGamal(p=701, order=100)
    		
    cipher = A.encrypt(msg, B.PublicKey())
    plain = B.decrypt(cipher)
    
    print(f"Msg : {msg}")
    print(f"Plain : {plain}")
```


#### Signatures

This module contains **signature**  functions.

###### Example 1
```python
import hashlib

from CryptoBox.arithmetic.prime import randprime
from CryptoBox.asymetric.RSA import RSA

if __name__ == "__main__":

	msg = "helo:)ThisismyCryptoBox."

	A = RSA(n=1024, p=3041, q=131)
	B = RSA(n=1024, p=1021, q=113)

	sha1 = lambda x: (hashlib.sha1(x.encode())).hexdigest()
	R = sha1
	
	sign = A.signature(msg, R)
	verif = B.verification(R(msg), sign, A.PublicKey())
	
	print(f"Signature : {sign}")
	print(f"Verification : {verif}")
```

###### Example 2
```python
import hashlib

from CryptoBox.arithmetic.prime import randprime
from CryptoBox.asymetric.ElGamal import ElGamal

if __name__ == "__main__":
	
	msg = "helo:)ThisismyCryptoBox."
	
	A = ElGamal(p=113, order=100)
	B = ElGamal(p=701, order=100)

	sha1 = lambda x: (hashlib.sha1(x.encode())).hexdigest()
	R = sha1
	
	sign = A.signature(msg, R)
	verif = B.verification(R(msg), sign, A.PublicKey())
	
	print(f"Signature : {sign}")
	print(f"Verification : {verif}")
```

#### KTP

This module contains functions **key agreement protocol** (KAP) and **key transport protocol** (KTP).

###### Example 1
```python
import random
from CryptoBox.arithmetic.prime import randprime
from CryptoBox.arithmetic.modulo import generators
from Cryptobox.ktp.ktp import  DiffieHellman

if __name__ == "__main__":

    p = randprime(0, 1024)
    g =  list(generators(p))
    alpha = g[random.randint(0, len(g)-1)]
    	
    A = DiffieHellman(p=p, alpha=alpha)
    B = DiffieHellman(p=p, alpha=alpha)
    	
    A.word(random.randint(0,124))
    B.word(random.randint(0,124))
    	
    A.key(B.exp)
    B.key(A.exp)
    	
    print(f"A : {A.key}")
    print(f"B : {B.key}")
```

###### Example 2
```python
import random

from CryptoBox.ktp.ktp import *
from CryptoBox.asymetric.RSA import RSA
from CryptoBox.arithmetic.prime import *
from CryptoBox.hash.hash import *

if __name__ == "__main__":

    p = [randprime(60,1024) for i in range(4)]
    
    A = NeedhamSchroeder(RSA(n=1024, p=p[0], q=p[1]), hash=sha256)
    B = NeedhamSchroeder(RSA(n=1024, p=p[0], q=p[1]), hash=sha256)
    
    # (1) A generates a random number k1 and send it encrypted	
    k1 = chr(random.randint(0,1024))
    fromAtoB = A.exchange(B.PublicKey(), k1)
    
    # (2) B generates a random number k2 and send i with k1 (both encrypted)	
    k2 = chr(random.randint(0,1024))
    fromAtoB1, fromAtoB2 = B.exchange(A.PublicKey(), k2, fromAtoB)
    
    # (3) A verifies k1, and encrypt k2 (received), if it is ok.
    fromAtoB = A.verification(B.PublicKey(), fromAtoB1, fromAtoB2)
    
    # (4) B verifies k2
    fromBtoA = B.verification(A.PublicKey(), fromAtoB)
    	
    print(f"A: k1 {A.k1}, k2 {A.k2}")
    print(f"B: k1 {B.k1}, k2 {B.k2}")
    print(f"A: {A.key} \nB: {B.key}")
```
###### Example 3
```python
import random

from CryptoBox.arithmetic.prime import *
from CryptoBox.symetric.AES128 import AES128
from CryptoBox.asymetric.RSA import RSA
from CryptoBox.asymetric.ElGamal import ElGamal
from CryptoBox.ktp.ktp import *


if __name__ == "__main__":

    p = [randprime(60,1024,1000) for i in range(4)]			
    		
    """ Verification for EKE (RSA, ElGamal) """
    password = ascii("".join([chr(random.randint(0,65536)) for _ in range(16)]))[:16]
    
    A = EKE(password, asym=RSA(n=1024, p=p[0], q=p[1]), sym=AES128(), profile="A")
    B = EKE(password, asym=RSA(n=1024, p=p[2], q=p[3]), sym=AES128(), profile="B")
    		
    # (1) A generates a public/private key and send public key to B, encrypted with password
    fromAtoB = A.KeyPublic()
    fromBtoA = B.KeyPublic(fromAtoB)
    		
    # (2) B generates a key session and send it encrypted
    fromBtoA = B.KeySession(16)
    fromAtoB = A.KeySession(fromBtoA)
    
    # (3) A generates a random number and send it encrypted with k
    fromAtoB1, fromAtoB2 =  A.RandomNumber()
    		
    # (4) B generates a random number rb and send it with ra, encrypted with k 
    fromBtoA1, fromBtoA2 = B.RandomNumber(fromAtoB1, fromAtoB2)
    fromAtoB = A.check(fromBtoA1, fromBtoA2)
    		
    fromBtoA = B.check(fromAtoB)
    
    print(f"Code ({i}): {fromBtoA}")
```

