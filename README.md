# 3stools
python script mostly written by TVIndustries and then modified

usage:

place the 4 encrypted files in the same directory as the script sfiii3-simm1.0 sfiii3-simm1.1 sfiii3-simm1.2 sfiii3-simm1.3, then run combine-and-decrypt.py to get a single decrypted binary file ("sfiii3-binary-combined-and-decrypted") ready for hex editing and loading into ghidra

when you're ready to re-split and encrypt, run split-and-encrypt.py and the output will be the 4 original files

for the BIOS, you can dump decrypted from MAME debugger using "save filename,0,0x080000". then use the bios python script here to re-encrypt after modifying.

here's an example of how I use it:

`
python split-and-encrypt.py

7z a /roms/arcade/sfiii3nr1.zip sfiii3-simm1.?

rm /home/username/.mame/nvram/sfiii3nr1/*simm1*

rm *simm*

rm sfiii3-binary-combined-and-encrypted-sfiii3nr1

mame sfiii3nr1 -debug -sound none -nofilter -resolution0 768x448 -cheat -nokeepaspect
`
