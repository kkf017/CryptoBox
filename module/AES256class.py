import copy
import math
import operator

from typing import List, Dict

from GF8 import galois



Sbox = [
        [0x63, 0x7c, 0x77, 0x7b, 0xf2, 0x6b, 0x6f, 0xc5, 0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76],
        [0xca, 0x82, 0xc9, 0x7d, 0xfa, 0x59, 0x47, 0xf0, 0xad, 0xd4, 0xa2, 0xaf, 0x9c, 0xa4, 0x72, 0xc0],
        [0xb7, 0xfd, 0x93, 0x26, 0x36, 0x3f, 0xf7, 0xcc, 0x34, 0xa5, 0xe5, 0xf1, 0x71, 0xd8, 0x31, 0x15],
        [0x04, 0xc7, 0x23, 0xc3, 0x18, 0x96, 0x05, 0x9a, 0x07, 0x12, 0x80, 0xe2, 0xeb, 0x27, 0xb2, 0x75],
        [0x09, 0x83, 0x2c, 0x1a, 0x1b, 0x6e, 0x5a, 0xa0, 0x52, 0x3b, 0xd6, 0xb3, 0x29, 0xe3, 0x2f, 0x84],
        [0x53, 0xd1, 0x00, 0xed, 0x20, 0xfc, 0xb1, 0x5b, 0x6a, 0xcb, 0xbe, 0x39, 0x4a, 0x4c, 0x58, 0xcf],
        [0xd0, 0xef, 0xaa, 0xfb, 0x43, 0x4d, 0x33, 0x85, 0x45, 0xf9, 0x02, 0x7f, 0x50, 0x3c, 0x9f, 0xa8],
        [0x51, 0xa3, 0x40, 0x8f, 0x92, 0x9d, 0x38, 0xf5, 0xbc, 0xb6, 0xda, 0x21, 0x10, 0xff, 0xf3, 0xd2],
        [0xcd, 0x0c, 0x13, 0xec, 0x5f, 0x97, 0x44, 0x17, 0xc4, 0xa7, 0x7e, 0x3d, 0x64, 0x5d, 0x19, 0x73],
        [0x60, 0x81, 0x4f, 0xdc, 0x22, 0x2a, 0x90, 0x88, 0x46, 0xee, 0xb8, 0x14, 0xde, 0x5e, 0x0b, 0xdb],
        [0xe0, 0x32, 0x3a, 0x0a, 0x49, 0x06, 0x24, 0x5c, 0xc2, 0xd3, 0xac, 0x62, 0x91, 0x95, 0xe4, 0x79],
        [0xe7, 0xc8, 0x37, 0x6d, 0x8d, 0xd5, 0x4e, 0xa9, 0x6c, 0x56, 0xf4, 0xea, 0x65, 0x7a, 0xae, 0x08],
        [0xba, 0x78, 0x25, 0x2e, 0x1c, 0xa6, 0xb4, 0xc6, 0xe8, 0xdd, 0x74, 0x1f, 0x4b, 0xbd, 0x8b, 0x8a],
        [0x70, 0x3e, 0xb5, 0x66, 0x48, 0x03, 0xf6, 0x0e, 0x61, 0x35, 0x57, 0xb9, 0x86, 0xc1, 0x1d, 0x9e],
        [0xe1, 0xf8, 0x98, 0x11, 0x69, 0xd9, 0x8e, 0x94, 0x9b, 0x1e, 0x87, 0xe9, 0xce, 0x55, 0x28, 0xdf],
        [0x8c, 0xa1, 0x89, 0x0d, 0xbf, 0xe6, 0x42, 0x68, 0x41, 0x99, 0x2d, 0x0f, 0xb0, 0x54, 0xbb, 0x16]
]


SboxInv = [
        [0x52, 0x09, 0x6a, 0xd5, 0x30, 0x36, 0xa5, 0x38, 0xbf, 0x40, 0xa3, 0x9e, 0x81, 0xf3, 0xd7, 0xfb],
        [0x7c, 0xe3, 0x39, 0x82, 0x9b, 0x2f, 0xff, 0x87, 0x34, 0x8e, 0x43, 0x44, 0xc4, 0xde, 0xe9, 0xcb],
        [0x54, 0x7b, 0x94, 0x32, 0xa6, 0xc2, 0x23, 0x3d, 0xee, 0x4c, 0x95, 0x0b, 0x42, 0xfa, 0xc3, 0x4e],
        [0x08, 0x2e, 0xa1, 0x66, 0x28, 0xd9, 0x24, 0xb2, 0x76, 0x5b, 0xa2, 0x49, 0x6d, 0x8b, 0xd1, 0x25],
        [0x72, 0xf8, 0xf6, 0x64, 0x86, 0x68, 0x98, 0x16, 0xd4, 0xa4, 0x5c, 0xcc, 0x5d, 0x65, 0xb6, 0x92],
        [0x6c, 0x70, 0x48, 0x50, 0xfd, 0xed, 0xb9, 0xda, 0x5e, 0x15, 0x46, 0x57, 0xa7, 0x8d, 0x9d, 0x84],
        [0x90, 0xd8, 0xab, 0x00, 0x8c, 0xbc, 0xd3, 0x0a, 0xf7, 0xe4, 0x58, 0x05, 0xb8, 0xb3, 0x45, 0x06],
        
        [0xd0, 0x2c, 0x1e, 0x8f, 0xca, 0x3f, 0x0f, 0x02, 0xc1, 0xaf, 0xbd, 0x03, 0x01, 0x13, 0x8a, 0x6b],
        [0x3a, 0x91, 0x11, 0x41, 0x4f, 0x67, 0xdc, 0xea, 0x97, 0xf2, 0xcf, 0xce, 0xf0, 0xb4, 0xe6, 0x73],
        [0x96, 0xac, 0x74, 0x22, 0xe7, 0xad, 0x35, 0x85, 0xe2, 0xf9, 0x37, 0xe8, 0x1c, 0x75, 0xdf, 0x6e],
        [0x47, 0xf1, 0x1a, 0x71, 0x1d, 0x29, 0xc5, 0x89, 0x6f, 0xb7, 0x62, 0x0e, 0xaa, 0x18, 0xbe, 0x1b],
        [0xfc, 0x56, 0x3e, 0x4b, 0xc6, 0xd2, 0x79, 0x20, 0x9a, 0xdb, 0xc0, 0xfe, 0x78, 0xcd, 0x5a, 0xf4],
        [0x1f, 0xdd, 0xa8, 0x33, 0x88, 0x07, 0xc7, 0x31, 0xb1, 0x12, 0x10, 0x59, 0x27, 0x80, 0xec, 0x5f],
        [0x60, 0x51, 0x7f, 0xa9, 0x19, 0xb5, 0x4a, 0x0d, 0x2d, 0xe5, 0x7a, 0x9f, 0x93, 0xc9, 0x9c, 0xef],
        [0xa0, 0xe0, 0x3b, 0x4d, 0xae, 0x2a, 0xf5, 0xb0, 0xc8, 0xeb, 0xbb, 0x3c, 0x83, 0x53, 0x99, 0x61],
        [0x17, 0x2b, 0x04, 0x7e, 0xba, 0x77, 0xd6, 0x26, 0xe1, 0x69, 0x14, 0x63, 0x55, 0x21, 0x0c, 0x7d]
]


#################################################################################################
# AES256 

class AES256():
	
	def __init__(self,):
		
		self.PADD = "%"
		self.BYTES = 32 # 16 octets par bloc -> 128 bits
			        # 24 octets par bloc -> 192 bits
			        # 32 octets par bloc -> 256 bits
		self.R = 15 # 16 round keys -> AES-128
		            # 13 round keys -> AES-192
		            # 15 round keys -> AES-256


	def padding(self, plain:str)->str:
		"""
			Function to padd plaintext.
			Input:
				plain - plain text
				a - char to padd
			Output:
				plaintext (padded)
		"""          
		if len(plain) % self.BYTES != 0:
			plain += "".join([self.PADD for _ in range(self.BYTES - len(plain) % self.BYTES)])	
		return plain
	

	def keySchedule(self, key:str)->None:
		"""
			Function to expand key (key scheduling).
			Input:
				key - initial key
			Output:
				key expansion (for R rounds)
		"""
		def xor(x:str, y:str)->str:
			op = ""
			for i in range(len(x)):
				xi = x[i]#.encode('utf-8')
				yi = y[i]#.encode('utf-8')
				z = ord(xi) ^ ord(yi) # operator.xor(ord(x),ord(y))
				op += chr(z)
			return op
		
		def RoundConstant(n:int)->str:
			rci = [-1]
			for i in range(1,n+1): # Revoir index avec list rci.
				if i == 1:
					rci.append(1)
				elif i>1 and  rci[i-1] < int("0x80", 0):
					rci.append(2*rci[i-1])
				elif i>1 and  rci[i-1] >= int("0x80", 0):
					rci.append((2*rci[i-1])^0x11B)
				else:
					pass
			return "".join([chr(rci[-1]), chr(0x00), chr(0x00),chr(0x00)])
			
		def RotWord(x:str)->str:
			return x[1:]+x[0]
			
		def SubWord(x:str)->str:
			z = ""
			for y in x:
				if ord(y) < 16:
					i = 0
					j = int("0x{}".format(hex(ord(y))[2]),0)
				else:
					i = int("0x{}".format(hex(ord(y))[2]),0)
					j = int("0x{}".format(hex(ord(y))[3]),0)
				value = Sbox[i][j]
				z += chr(value)			
			return z
			  
		if len(key) != self.BYTES:
			raise Exception("\n\033[{}m[-]Error: Key size has to be {} bytes.".format("0;33", self.BYTES))
		
		N = self.BYTES*8 // 32 # length of the key in 32-bit words (4*8bits): 
				  	#4 words -> AES-128, 
				  	#6 words -> AES-192
				  	#8 words -> AES-256
		key32 = [copy.copy(key[i*4:(i+1)*4]) for i in range(N)] 
			
		W = []
		for i in range(N*self.R):
			if i < N:
				W.append(key32[i])
							
			elif i>=N and i%N == 0:
				wi = xor(xor(W[i-N],SubWord(RotWord(W[i-1]))), RoundConstant(int(i/N)))
				W.append(wi)
				
			elif i>=N and N>6 and i%N==4:
				wi = xor(W[i-N],SubWord(W[i-1]))
				W.append(wi)
			else:
				wi = xor(W[i-N], W[i-1])
				W.append(wi)	
		return W
	

	def blockencrypt(self, plain: str, keys: List[str])->str:
		"""
			Function to encrypt a block (of 128/192/256 bytes).
			Input:
				plain - plaintext (block to encrypt)
				keys - key expansion (from keyschedule)
			Output:
				block (encrypted)
		"""
		def AddRoundKey(x:str, y:str)->str: # -> XOR bit à bit
			op = ""
			for i in range(len(x)):
				xi = x[i]#.encode('utf-8')
				yi = y[i]#.encode('utf-8')
				z = ord(xi) ^ ord(yi) # operator.xor(ord(x),ord(y))
				op += chr(z)
			return op

		def SubBytes(x:str)->str:
			z = ""
			for y in x:
				if ord(y) < 16:
					i = 0
					j = int("0x{}".format(hex(ord(y))[2]),0)
				else:
					i = int("0x{}".format(hex(ord(y))[2]),0)
					j = int("0x{}".format(hex(ord(y))[3]),0)
				value = Sbox[i][j]
				z += chr(value)		
			return z
		

		def ShiftRows(x:str)->str:
			msg = copy.copy(x)
			columns = [1,2,3,4,6,7,8,5,11,12,9,10,16,13,14,15] # to change ! - for 16, 24, 32 bytes
			x1 = [msg[0:16][i-1] for i in columns]
			x2 = [msg[16:][i-1] for i in columns]
			return "".join(x1+x2)

		def MixColumns(x:str)->List[str]:
			mtx = [2,3,1,1,
		     	       1,2,3,1,
		     	       1,1,2,3,
		     	       3,1,1,2] # to change ! - for 16, 24, 32 bytes
			return galois(x[0:16], mtx) + galois(x[16:], mtx)

		N = self.BYTES//4

		cipher = AddRoundKey(plain, "".join(keys[0:0+N])) 
		
		for i in range(1,self.R-2+1): # -> R= 11 -2 = 9
			cipher = SubBytes(cipher) 
			cipher = ShiftRows(cipher) 
			cipher = MixColumns(cipher) 
			cipher = AddRoundKey(cipher, "".join(keys[i*N:i*N+N]))
		

		cipher = SubBytes(cipher) 
		cipher = ShiftRows(cipher)	
		cipher = AddRoundKey(cipher, "".join(keys[10*N:10*N+N]))
		return cipher
		
	
	def blockdecrypt(self, cipher: str, keys: List[str])->None:
		"""
			Function to decrypt a block (of 128/192/256 bytes).
			Input:
				cipher - cipher (block to decrypt)
				keys - key expansion (from keyschedule)
			Output:
				block (decrypted)
		"""
		def InvAddRoundKey(x:str, y:str)->str: # -> XOR bit à bit
			op = ""
			for i in range(len(x)):
				xi = x[i]#.encode('utf-8')
				yi = y[i]#.encode('utf-8')
				z = ord(xi) ^ ord(yi) # operator.xor(ord(x),ord(y))
				op += chr(z)
			return op

		def InvShiftRows(x:str)->str:
			msg = copy.copy(x)
			columns = [1,2,3,4,8,5,6,7,11,12,9,10,14,15,16,13]  # to change ! - for 16, 24, 32 bytes
			x1 = [msg[0:16][i-1] for i in columns]
			x2 = [msg[16:][i-1] for i in columns]
			return "".join(x1+x2)
			
		def InvSubBytes(x:str)->str:
			z = ""
			for y in x:
				if ord(y) < 16:
					i = 0
					j = int("0x{}".format(hex(ord(y))[2]),0)
				else:
					i = int("0x{}".format(hex(ord(y))[2]),0)
					j = int("0x{}".format(hex(ord(y))[3]),0)
				value = SboxInv[i][j]
				z += chr(value)		
			return z

		def InvMixColumns(x:str)->List[str]:
			mtx = [0x0E,0x0B,0x0D,0x09,
			       0x09,0x0E,0x0B,0x0D,
			       0x0D,0x09,0x0E,0x0B,
			       0x0B,0x0D,0x09,0x0E]  # to change ! - for 16, 24, 32 bytes
			return galois(x[0:16], mtx) + galois(x[16:], mtx)
		
		
		N = self.BYTES//4 #int(math.sqrt(BYTES))
		
		plain = InvAddRoundKey(cipher, "".join(keys[10*N:10*N+N]))	
		plain = InvShiftRows(plain) 
		plain = InvSubBytes(plain) 
		
		for i in range(self.R-2,0,-1): # -> R= 11 -2 = 9
			plain = InvAddRoundKey(plain, "".join(keys[i*N:i*N+N]))		
			plain = InvMixColumns(plain)		
			plain = InvShiftRows(plain)
			plain = InvSubBytes(plain) 
			
		plain = InvAddRoundKey(plain, "".join(keys[0:0+N])) 
		return plain
	
		
	def encrypt(self, plain: str, key:str)->None:
		"""
			Function to encrypt a message.
			Input:
				plain - plain text
				key - key (for encryption)
			Output:
				cipher text (encryption)
		"""
		plain = self.padding(plain)
		keys = self.keySchedule(key)	
		cipher = [self.blockencrypt(plain[i*self.BYTES:(i+1)*self.BYTES], keys) for i in range(len(plain)//self.BYTES)] 
		return "".join(cipher)
	

	def decrypt(self, cipher:str, key:str)->None:
		"""
			Function to decrypt a message.
			Input:
				plain - plain text
				key - key (for decryption)
			Output:
				plain text (decryption)
		"""
		keys = self.keySchedule(key)
		plain = [self.blockdecrypt(cipher[i*self.BYTES:(i+1)*self.BYTES], keys) for i in range(len(cipher)//self.BYTES)]
		return "".join(plain)
	
	
#################################################################################################
# main

"""
if __name__ == "__main__":
	
	plain = "helo,:(iamtired,iamexhausted"
	key = "helo:)iamyourkey+toencryptSecret" # clés de 256 bits -> 32 bytes
	
	aes256 = AES256()
	
	print("\n{} {}".format(plain, len(plain)))
	print("{}".format([hex(ord(i)) for i in plain]))
	
	cipher = aes256.encrypt(plain, key)
	
	print("\n{} {}".format(cipher, len(cipher)))
	print("{}".format([hex(ord(i)) for i in cipher]))
	
	plain = aes256.decrypt(cipher, key)
	
	print("\n{} {}".format(plain, len(plain)))
	print("{}".format([hex(ord(i)) for i in plain]))
"""

