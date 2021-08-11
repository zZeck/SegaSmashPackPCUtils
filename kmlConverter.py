from PIL import Image
import sys
import wave
import collections
from bitarray import bitarray
import os

ImageSectionMetadata = collections.namedtuple('ImageSectionMetadata', 'dimensions mode palette name')
AudioMetadata = collections.namedtuple('AudioSectionMetadata', 'sampleRate name')

def main():
	kmlArchivePath = sys.argv[1]
	kmlArchiveName = os.path.split(kmlArchivePath)[-1];
	
	kmlArchive = bytearray(open(kmlArchivePath, 'rb').read())
	sections = kmlArchiveToSections(kmlArchive)
	if kmlArchiveName == 'SoundBlk.kml':
		sectionsToWavFiles(sections)
	elif kmlArchiveName ==  'MainBlok.kml' and len(sys.argv) > 2:
		smashExePath = sys.argv[2]
		smashExeName = os.path.split(smashExePath)[-1];
		smashMetadata = None
		if smashExeName == 'Smash.exe':
			smashMetadata = smashMainBlokMetaData(smashExePath)
		elif smashExeName == 'Smash2.exe':
			smashMetadata = smash2MainBlokMetaData(smashExePath)	
		images = sectionsToImages(smashMetadata, sections)
		for image, sectionMetaData in zip(images, smashMetadata):
			image.save(f'{sectionMetaData.name}.png')
	else:
		index = 0
		while index < len(sections):
			open(f'section{index}.data', 'wb').write(sections[index])
			index += 1

def kmlArchiveToSections(kmlArchive):
	hasRunFlag = lambda byte: byte & 0b11000000 == 0b11000000
	byteToRunLength = lambda byte: byte & 0b00111111

	sections = []
	kmlIndex = 0
	while kmlIndex < len(kmlArchive):
		kmlSectionMagicString = kmlArchive[kmlIndex:kmlIndex+4].decode('ascii')
		kmlIndex += 4
		kmlSectionNumber = int.from_bytes((kmlArchive[kmlIndex:kmlIndex+4]), 'little')
		kmlIndex += 4
		kmlSectionSize = int.from_bytes((kmlArchive[kmlIndex:kmlIndex+4]), 'little')
		kmlIndex += 4
		kmlDecompressedSize = int.from_bytes((kmlArchive[kmlIndex:kmlIndex+4]), 'little')
		kmlIndex += 4
		outData = bytearray(kmlDecompressedSize)
		kmlSectionStartIndex = kmlIndex
		outDataIndex = 0
		while kmlIndex - kmlSectionStartIndex < kmlSectionSize:
			byte1 = kmlArchive[kmlIndex]
			kmlIndex += 1
			dataByte = byte1
			runLength = 1
			if hasRunFlag(byte1):
				runLength = byteToRunLength(byte1)
				dataByte = kmlArchive[kmlIndex]
				kmlIndex += 1
			runIndex = 0
			while runIndex < runLength:
				outData[outDataIndex] = dataByte
				outDataIndex += 1
				runIndex += 1
		sections.append(outData)
	return sections

def sectionsToWavFiles(sections):
	soundBlokMetadata = [
		AudioMetadata(44100, 'sega44'),
		AudioMetadata(22050, 'sega22'),
		AudioMetadata(11025, 'sega11'),
		AudioMetadata(44100, 'menu navigation44'),
		AudioMetadata(22050, 'menu navigation22'),
		AudioMetadata(11025, 'menu navigation11'),
		AudioMetadata(44100, 'menu selection44'),
		AudioMetadata(22050, 'menu selection22'),
		AudioMetadata(11025, 'menu selection11'),
	]
	for section, sectionMetadata in zip(sections, soundBlokMetadata):
		with wave.open(f'{sectionMetadata.name}.wav', 'wb') as wavfile:
			wavfile.setparams((1, 1, sectionMetadata.sampleRate, 0, 'NONE', 'NONE'))
			wavfile.writeframes(section)

def sectionsToImages(sectionMetaDataList, sections):
	images = []
	for sectionMetadata, section in zip(sectionMetaDataList, sections):
		image = Image.new(sectionMetadata.mode, sectionMetadata.dimensions)
		if sectionMetadata.mode == '1':
			image.putdata(bitarray(''.join(format(byte, '08b') for byte in section)))
		else:
			image.putpalette(sectionMetadata.palette)
			image.putdata(section)
		images.append(image)
	return images

def smash2MainBlokMetaData(smashPack2ExePath):
	menuPalette = None
	otherPalette = None
	titleGraphicPalette = None
	cursorPalette = None
	menuBackgroundPalette = None
	comixZonePalette = None
	flickyPalette = None
	kidChameleonPalette = None
	shiningPalette = None
	sonic2Palette = None
	superHangOnPalette = None
	vectorman2Palette = None
	controllerPalette = None
	sonic2ModeSelectPalette = None
	segaLogoPalette = None
	cursorAndArrowPalette = None
	menuBackgroundPalette = None
	titleGraphicPalette = None
	controllerPalette = None
	
	with open(smashPack2ExePath, 'rb') as exeFile:
		exeFile.seek(0x8ca28)
		comixZonePalette = list(exeFile.read(0x123))
		exeFile.seek(0x8CB4B)
		flickyPalette = list(exeFile.read(0x123))
		exeFile.seek(0x8cc6E)
		kidChameleonPalette = list(exeFile.read(0x123))
		exeFile.seek(0x8cd91)
		shiningPalette = list(exeFile.read(0x123))
		exeFile.seek(0x8ceb4)
		sonic2Palette = list(exeFile.read(0x123))
		exeFile.seek(0x8cfd7)
		superHangOnPalette = list(exeFile.read(0x123))
		exeFile.seek(0x8D0Fa)
		vectorman2Palette = list(exeFile.read(0x123))
		exeFile.seek(0x8d21d)
		sonic2ModeSelectPalette = list(exeFile.read(0x123))
		exeFile.seek(0x8d340)
		sonic2ModeSelectPalette = list(exeFile.read(0x123))
		exeFile.seek(0x8d464)
		cursorAndArrowPalette = list(exeFile.read(0x18))
		exeFile.seek(0x8d47C)
		segaLogoPalette = list(exeFile.read(0x300))
		exeFile.seek(0x8d77c)
		menuBackgroundPalette = list(exeFile.read(0xA2))
		exeFile.seek(0x8D820)
		titleGraphicPalette = list(exeFile.read(0x240))
		exeFile.seek(0x8da60)
		controllerPalette = list(exeFile.read(0x120))

	return [
		ImageSectionMetadata((160, 112), 'P', comixZonePalette, 'comix zone'),
		ImageSectionMetadata((160, 112), 'P', flickyPalette, 'flicky'),
		ImageSectionMetadata((160, 112), 'P', kidChameleonPalette, 'kid chameleon'),
		ImageSectionMetadata((160, 112), 'P', shiningPalette, 'shining force'),
		ImageSectionMetadata((160, 112), 'P', sonic2Palette, 'sonic 2'),
		ImageSectionMetadata((160, 112), 'P', superHangOnPalette, 'super hang-on'),
		ImageSectionMetadata((160, 112), 'P', vectorman2Palette, 'vectorman 2'),
		ImageSectionMetadata((160, 112), 'P', sonic2ModeSelectPalette, 'sonic 2 arcade mode'),
		ImageSectionMetadata((160, 112), 'P', sonic2ModeSelectPalette, 'sonic 2 fullscreen mode'),
		ImageSectionMetadata((320, 240), 'P', segaLogoPalette, 'sega logo'),
		ImageSectionMetadata((12, 12), 'P', cursorAndArrowPalette, 'cursor'),
		ImageSectionMetadata((17, 136), 'P', cursorAndArrowPalette, 'navigation arrow sheet'),
		ImageSectionMetadata((256, 80), '1', None, 'bitmap font'),
		ImageSectionMetadata((320, 240), 'P', menuBackgroundPalette, 'menu background'),
		ImageSectionMetadata((256, 160), 'P', titleGraphicPalette, 'title graphic'),
		ImageSectionMetadata((64, 288), 'P', controllerPalette, 'controller sheet'),
		ImageSectionMetadata((8, 128), 'P', controllerPalette, 'controller button label sheet')
	]

def smashMainBlokMetaData(smashExePath):
	alteredBeastPalette = None
	columnsPalette = None
	goldenAxePalette = None
	outrunPalette = None
	phantasyStartIIPalette = None
	superShinobiPalette = None
	sonicSpinballPalette = None
	vectormanPalette = None
	segaLogoPalette = None
	cursorAndArrowPalette = None
	menuBackgroundPalette = None
	titleGraphicPalette = None
	controllerPalette = None
	
	with open(smashExePath, 'rb') as exeFile:
		exeFile.seek(0x7F994)
		alteredBeastPalette = list(exeFile.read(0x123))
		exeFile.seek(0x7FAB7)
		columnsPalette = list(exeFile.read(0x123))
		exeFile.seek(0x7FBDA)
		goldenAxePalette = list(exeFile.read(0x123))
		exeFile.seek(0x7FCFD)
		outrunPalette = list(exeFile.read(0x123))
		exeFile.seek(0x7FE20)
		phantasyStartIIPalette = list(exeFile.read(0x123))
		exeFile.seek(0x7FF43)
		superShinobiPalette = list(exeFile.read(0x123))
		exeFile.seek(0x80066)
		sonicSpinballPalette = list(exeFile.read(0x123))
		exeFile.seek(0x80189)
		vectormanPalette = list(exeFile.read(0x123))
		exeFile.seek(0x802AC)
		cursorAndArrowPalette = list(exeFile.read(0x18))
		exeFile.seek(0x802C4)
		segaLogoPalette = list(exeFile.read(0x6c))
		exeFile.seek(0x80330)
		menuBackgroundPalette = list(exeFile.read(0xA2))
		exeFile.seek(0x803D4)
		titleGraphicPalette = list(exeFile.read(0x240))
		exeFile.seek(0x80614)
		controllerPalette = list(exeFile.read(0x120))

	return [
		ImageSectionMetadata((160, 112), 'P', alteredBeastPalette, 'altered beast'),
		ImageSectionMetadata((160, 112), 'P', columnsPalette, 'columns'),
		ImageSectionMetadata((160, 112), 'P', goldenAxePalette, 'golden axe'),
		ImageSectionMetadata((160, 112), 'P', outrunPalette, 'outrun'),
		ImageSectionMetadata((160, 112), 'P', phantasyStartIIPalette, 'phantasy start II'),
		ImageSectionMetadata((160, 112), 'P', superShinobiPalette, 'super shinobi'),
		ImageSectionMetadata((160, 112), 'P', sonicSpinballPalette, 'sonic spinball'),
		ImageSectionMetadata((160, 112), 'P', vectormanPalette, 'vectorman'),
		ImageSectionMetadata((320, 240), 'P', segaLogoPalette, 'sega logo'),
		ImageSectionMetadata((12, 12), 'P', cursorAndArrowPalette, 'cursor'),
		ImageSectionMetadata((17, 136), 'P', cursorAndArrowPalette, 'navigation arrow sheet'),
		ImageSectionMetadata((256, 80), '1', None, 'bitmap font'),
		ImageSectionMetadata((320, 240), 'P', menuBackgroundPalette, 'menu background'),
		ImageSectionMetadata((256, 160), 'P', titleGraphicPalette, 'title graphic'),
		ImageSectionMetadata((64, 288), 'P', controllerPalette, 'controller sheet'),
		ImageSectionMetadata((8, 128), 'P', controllerPalette, 'controller button label sheet')
	]

if __name__=="__main__":
	main()
