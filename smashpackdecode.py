import sys
import struct

inputFile = bytearray(open(sys.argv[3], 'rb').read())

outFile = None 

encodeStringPack1 = bytearray('Encoded for KGen Ultra / Sega Smash Pack / Snake KML 1999! ', 'ascii')
encodeStringPack2 = bytearray('Encoded for KGen Ultra / Sega Smash Pack II / Snake KML 1999! ', 'ascii')

encodeString = None

if sys.argv[2] == '-1':
	encodeString = encodeStringPack1
else:
	encodeString = encodeStringPack2

encodeStringOffset = 0
scramble = 6

if sys.argv[1] == '-d':
	romSize = len(inputFile)-8
	outFile = bytearray(romSize)
	for index in range(romSize):
		encodedByte = inputFile[8+index]
		encodeStringCharacter = encodeString[encodeStringOffset]
		decodedByte = ((encodedByte ^ encodeStringCharacter ^ 0x80) - scramble) & 0xFF
		outFile[index] = decodedByte
		scramble += 3
		if encodeStringOffset < len(encodeString) - 1:
			encodeStringOffset += 1
		else:
			encodeStringOffset = 0
else:
	romSize = len(inputFile)
	outFile = bytearray(romSize+8)
	check = 0
	for index in range(romSize):
		romByte = inputFile[index]
		encodeStringCharacter = encodeString[encodeStringOffset]
		encodedByte = ((romByte + scramble) & 0xFF) ^ 0x80 ^ encodeStringCharacter
		outFile[8+index] = encodedByte
		scramble += 3
		check = (check + encodedByte + romByte) & 0xFFFFFFFF
		if encodeStringOffset < len(encodeString) - 1:
			encodeStringOffset += 1
		else:
			encodeStringOffset = 0
	checkBytes1 = check.to_bytes(32, 'little')
	checkBytes2 = ((~check) & 0xFFFFFFFF).to_bytes(32, 'little')
	for index in range(4):
		outFile[index] = checkBytes1[index]
	for index in range(4):
		outFile[4+index] = checkBytes2[index]

open(sys.argv[4], 'wb').write(outFile)
