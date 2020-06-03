import Data
import zlib
import crypting
import keys
import rabinMiller
import fileOperations

IDAT = '49444154'
IEND = '49454e44'

filename = '3x2.png'
publicKey, privateKey = keys.generateKey(1024)
'''
def test(file, public, private):
    _, compress, decompress, _, _ = Data.getIDAT(file)
    en = []
    de = []
    k=0
    block_size = 256
    if len(compress)%8 != 0:
        for add in range(len(compress)%8):
            compress+= bytes(0)
    while k < len(compress):
        if k+block_size<len(compress):
            block = compress[k:k+block_size]
        else:
            block = compress[k:len(compress)]
        encryp = crypting.encrypting(int.from_bytes(block, byteorder='big'),public)
        foo = (encryp.to_bytes((encryp.bit_length() // 8) + 1, byteorder='big')).hex()
        en.append(bytes.fromhex(foo))
        k+=block_size
    return b''.join(en)

def test_dec(file, public, private):
    encoded = test(file,public,private)
    decrypt = []
    k = 0
    block_size = 256
    enc = encoded
    if len(encoded) % 8 != 0:
        for add in range(len(encoded) % 8):
            encoded += bytes(0)
    while k < len(encoded):
        if k + block_size < len(encoded):
            block = encoded[k:k + block_size]
        else:
            block = encoded[k:len(encoded)]
        decryp = crypting.decrypting(int.from_bytes(block, byteorder='big'),private)
        foo = (decryp.to_bytes((decryp.bit_length() // 8) + 1, byteorder='big')).hex()
        decrypt.append(bytes.fromhex(foo))
        k += block_size
        k+=block_size
    print(b''.join(decrypt))
'''
def test(file, public, private):
    _, compress, decompress, _, _ = Data.getIDAT(file)
    k=0
    block_size = 256
    block = decompress[0:k+block_size]
    encryp = crypting.encrypting(int.from_bytes(block, byteorder='big'),public)
    foo = (encryp.to_bytes((encryp.bit_length() // 8) + 1, byteorder='big'))
    en=foo
    decryp = crypting.decrypting(int.from_bytes(block, byteorder='big'),private)
    foo = (decryp.to_bytes((decryp.bit_length() // 8) + 1, byteorder='big'))
    de=foo
    print(block==de)

def encrypt_compressed(file,public):
    _, compress, decompress, _, _ = Data.getIDAT(file)
    block_size = 64
    encrypt_compress = []
    compress= compress.hex()
    k=0
    if len(compress)%8 != 0:
        for add in range(len(compress)%8):
            compress+='0'
    while k < len(compress):
        if k+block_size<len(compress):
            block = compress[k:k+block_size]
        else:
            block = compress[k:len(compress)]
        print(int(block,16))
        encrypy_block=crypting.encrypting(int(block,16),public)
        encrypt_compress.append(encrypy_block)
        k+=block_size
    print(encrypt_compress)
    print(crypting.decrypting(encrypt_compress[0],privateKey))


def encrypt_decompressed(filename,public):
    _, comp, decompress, _, _ = Data.getIDAT(filename)
    encrypt_decompress = []
    #size = len(decompress)
    block_size = 64
    foo = []
    #foo1=[]
    decompress = decompress.hex()
    k = 0
    if len(decompress) % 8 != 0:
        for add in range(len(decompress) % 8):
            decompress += '00'
    while k < len(decompress):
        if k + block_size < len(decompress):
            block = decompress[k:k + block_size]
        else:
            block = decompress[k:len(decompress)]
        foo.append(int(block, 16))
        encrypy_block = crypting.encrypting(int(block, 16), public)
        print(bytes(encrypy_block))
        encrypt_decompress.append(bytes(encrypy_block))
        k += block_size

    #print(encrypt_decompress)
    #for i in range(len(encrypt_decompress)):
    #   foo1.append(crypting.decrypting(encrypt_decompress[i], privateKey))
    #print(foo==foo1)

def decrypt_compressed(filename,private):
    _,compress,decompress,_,_ = Data.getIDAT(filename)
    decrypt_compress = []
    for j in range(len(compress)):
        decrypt_compress.append(crypting.decrypting(compress[j],private))
   # print(decrypt_compress)
def decrypt_decompressed(filename,private):
    _, comp, decompress, _, _ = Data.getIDAT(filename)
    decrypt_dec = []
    for j in range(len(decompress)):
        decrypt_dec.append(crypting.decrypting(decompress[j], private))
   # print(decrypt_dec)

def savePNG_decompress(OGfile,newfile):
    file = open(OGfile, 'rb')
    fileInHex = file.read().hex()
    posIDAT = fileInHex.find(IDAT)
    posIEND = fileInHex.find(IEND)
    text_file = open(newfile, 'wb')
    #print(fileInHex[:(posIDAT + 8)].encode('utf-8'))  wrong way
    #print(bytes.fromhex(fileInHex[:(posIDAT + 8)]))   corect way
    n = text_file.write(bytes.fromhex(fileInHex[:(posIDAT + 8)]))
    idata = test(OGfile,publicKey,privateKey)
    print(idata)
    n=text_file.write(idata)
    n = text_file.write(bytes.fromhex(fileInHex[posIEND:]))
    text_file.close()
    print("Hex version of this file has been saved to given file")
    file.close()
    text_file.close()


test('3x2.png',publicKey,privateKey)
#test_dec('3x2.png',publicKey,privateKey)
#encrypt_compressed(filename,publicKey)
#encrypt_decompressed(filename,publicKey)
#fileOperations.displayImage('test.png')
#savePNG_decompress('3x2.png','test.txt')


