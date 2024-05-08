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

```bash
from CryptoBox.symetric.AES128 import AES128
from CryptoBox.symetric.AES256 import AES256

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
```bash
from CryptoBox.arithmetic.prime import randprime
from CryptoBox.asymetric.RSA import RSA

msg = "helo:)ThisismyCryptoBox."

A = RSA(n=1024, p=3041, q=131)
B = RSA(n=1024, p=1021, q=113)
		
cipher = A.encrypt(msg, B.PublicKey())
plain = B.decrypt(cipher)

print(f"Msg : {msg}")
print(f"Plain : {plain}")
```

###### Example 2
```bash
from CryptoBox.asymetric.Rabin import Rabin

msg = "helo:)ThisismyCryptoBox."

A = Rabin(p=191, q=21001)
B = Rabin(p=251, q=1051)
		
cipher = A.encrypt(msg, B.PublicKey())
plain = B.decrypt(cipher)

print(f"Msg : {msg}")
print(f"Plain : {plain}")

```


###### Example 3
```bash
from CryptoBox.arithmetic.prime import randprime
from CryptoBox.asymetric.ElGamal import ElGamal

msg = "helo:)ThisismyCryptoBox."

A = ElGamal(p=113, order=100)
B = ElGamal(p=701, order=100)
		
cipher = A.encrypt(msg, B.PublicKey())
plain = B.decrypt(cipher)

print(f"Msg : {msg}")
print(f"Plain : {plain}")
```



#### KTP

This module contains functions **key agreement protocol** (KAP) and **key transport protocol** (KTP).

###### Example 1
```bash
import random
from CryptoBox.arithmetic.prime import randprime
from CryptoBox.arithmetic.modulo import generators
from Cryptobox.ktp.ktp import  DiffieHellman

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
```bash
import random

from CryptoBox.ktp.ktp import *
from CryptoBox.asymetric.RSA import RSA
from CryptoBox.arithmetic.prime import *
from CryptoBox.hash.hash import *

p = [randprime(60,1024) for i in range(4)]

A = NeedhamSchroeder(RSA(n=1024, p=p[0], q=p[1]), hash=sha256)
B = NeedhamSchroeder(RSA(n=1024, p=p[0], q=p[1]), hash=sha256)
	
k1 = chr(random.randint(0,1024))
fromAtoB = A.exchange(B.PublicKey(), k1)
	
k2 = chr(random.randint(0,1024))
fromAtoB1, fromAtoB2 = B.exchange(A.PublicKey(), k2, fromAtoB)
	
fromAtoB = A.verification(B.PublicKey(), fromAtoB1, fromAtoB2)
	
fromBtoA = B.verification(A.PublicKey(), fromAtoB)
	
print(f"A: k1 {A.k1}, k2 {A.k2}")
print(f"B: k1 {B.k1}, k2 {B.k2}")
print(f"A: {A.key} \nB: {B.key}")
```

