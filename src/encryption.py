import string
import pymongo
from Crypto.Hash import SHA256
from Crypto.Cipher import AES
from Crypto import Random
from binascii import hexlify,a2b_uu
import pickle


def test():
	hash = SHA256.new()
	hash.update(b'message to hash')
	key = hash.digest()
	print("KEY: " + binConvert(key))

	iv = Random.new().read(16)
	print("IV: " + binConvert(iv))
	AES_encrypter = AES.new(key, AES.MODE_CBC, iv)

	message = b"Get wreked nerds"
	cypher = AES_encrypter.encrypt(message)
	print("Cypher: " + binConvert(cypher))

	AES_decrypter = AES.new(key, AES.MODE_CBC, iv)
	output = AES_decrypter.decrypt(cypher)
	print("Output: " + str(output,'ascii'))

def createUserSecurity(username, password):
	salt = binConvert(Random.new().read(16))
	keySalt = binConvert(Random.new().read(16))
	IV = Random.new().read(16)
	passwordHash = SHA256.new()
	passwordHash.update(bytes(password + salt, 'ascii'))
	t = {}
	t['username'] = username
	t['salt'] = salt
	t['password'] = binConvert(passwordHash.digest())
	t['keySalt'] = keySalt
	t['IV'] = IV

	print("Salt: " + salt)
	print("PasswordHash: " + binConvert(passwordHash.digest()))
	print("keySalt: " + keySalt)
	print("IV: " + binConvert(IV))
	return t

def encrypt(data, encryptionDict):
	hash = SHA256.new()
	key = hash.update(bytes(encryptionDict['password'] + encryptionDict['keySalt'], 'ascii'))
	bytes = bytes(data, 'ascii')
	AES_encrypter = AES.new(key, AES.MODE_CFB, encryptionDict['IV'])
	return AES_encrypter.encrypt(bytes)

def encryptDict(dict, encryptionDict):
	hash = SHA256.new()
	hash.update(bytes(encryptionDict['password'] + encryptionDict['keySalt'], 'ascii'))
	key = hash.digest()
	data = pickle.dumps(dict)
	AES_encrypter = AES.new(key, AES.MODE_CFB, encryptionDict['IV'])
	return binConvert(AES_encrypter.encrypt(data))


def binConvert(input):
	return str(hexlify(input),"ascii")
#Database:
#	userName
# 	passwordHash
#	passwordSalt
#	keySalt
#	IV
#
#	Rest of Data is Encrypted with AES
#
#
#
#
#
#
#
