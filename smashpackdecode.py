import sys

def main():
	encodeString = None
	match sys.argv[2]:
		case '-1':
			encodeString = bytearray('Encoded for KGen Ultra / Sega Smash Pack / Snake KML 1999! ', 'ascii')
		case '-2':
			encodeString = bytearray('Encoded for KGen Ultra / Sega Smash Pack II / Snake KML 1999! ', 'ascii')
		case '-p':
			encodeString = bytearray('Encoded for KGen Ultra / Sega Puzzle Pack / Snake KML 1999! ', 'ascii')
		case _:
			raise Exception('Invalid pack')

	outBytes = None
	with open(sys.argv[3], 'rb') as inputFile:
		inBytes = inputFile.read()
		match sys.argv[1]:
			case '-d':
				outBytes = decode(inBytes, encodeString)
			case '-e':
				outBytes = encode(inBytes, encodeString)
			case _:
				raise Exception('Invalid action')

	with open(sys.argv[4], 'wb') as outFile:
		outFile.write(outBytes)

def decode(inBytes, encodeString):
	scramble = 6
	outFile = bytearray()
	for index, encodedByte in enumerate(inBytes[8:]):
		encodeStringCharacter = encodeString[index % len(encodeString)]
		decodedByte = ((encodedByte ^ encodeStringCharacter ^ 0x80) - scramble) & 0xFF
		outFile.append(decodedByte)
		scramble += 3
	return outFile

def encode(inBytes,encodeString):
	scramble = 6
	outFile = bytearray()
	check = 0
	for index, romByte in enumerate(inBytes):
		encodeStringCharacter = encodeString[index % len(encodeString)]
		encodedByte = ((romByte + scramble) & 0xFF) ^ 0x80 ^ encodeStringCharacter
		outFile.append(encodedByte)
		scramble += 3
		check = (check + encodedByte + romByte) & 0xFFFFFFFF
	checkBytes1 = check.to_bytes(4, 'little')
	checkBytes2 = ((~check) & 0xFFFFFFFF).to_bytes(4, 'little')
	outFile = checkBytes1 + checkBytes2 + outFile
	return outFile

if __name__=="__main__":
    main()