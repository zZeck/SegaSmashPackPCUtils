encode with pack 2 encoding

.\smashpackkvqutil.py -e -2 '.\Ristar (UE) (Aug 1994) [!].bin' 'Shining Force.kvq'

decode with pack 1 encoding

.\smashpackkvqutil.py -d -1 '.\Phantasy Star II.kvq' ps2.bin

decode with puzzle pack encoding

.\smashpackkvqutil.py -d -p '.\Phantasy Star II.kvq' ps2.bin

convert save file

.\kmlConverter.py 'GameSav3.KML'

png images

.\kmlConverter.py 'MainBlok.kml' 'Smash2.exe'

wav files

.\kmlConverter.py 'SoundBlk.kml'


kml script uses Pillow and bitarray.


If you want to save games, you must replace a game in the collection that had saving.
Comix Zone has a patch applied by smash pack 2 after it is decoded into RAM.
This patch will be applied to any ROM you replace comix zone with, which will likely crash that rom.
