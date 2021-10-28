import os

simm1_0 = open('sfiii3-simm1.0-unencrypted', 'wb+')
simm1_1 = open('sfiii3-simm1.1-unencrypted', 'wb+')
simm1_2 = open('sfiii3-simm1.2-unencrypted', 'wb+')
simm1_3 = open('sfiii3-simm1.3-unencrypted', 'wb+')

file_10 = open('sfiii3-binary-combined-and-decrypted', 'rb')

fileSize = os.path.getsize('sfiii3-binary-combined-and-decrypted')
for i in range(0, fileSize, 4):
    data = int.from_bytes(file_10.read(1), 'little')
    simm1_0.write(data.to_bytes(1, 'little', signed=False))
    data = int.from_bytes(file_10.read(1), 'little')
    simm1_1.write(data.to_bytes(1, 'little', signed=False))
    data = int.from_bytes(file_10.read(1), 'little')
    simm1_2.write(data.to_bytes(1, 'little', signed=False))
    data = int.from_bytes(file_10.read(1), 'little')
    simm1_3.write(data.to_bytes(1, 'little', signed=False))

file_10.close()
simm1_0.close()
simm1_1.close()
simm1_2.close()
simm1_3.close()


def rotate_left(value, n):
    value &= 0xFFFF
    aux = (value >> (16 - n))
    return ((value << n) | aux) % 0x10000


def rotxor(val, xorval):
    val &= 0xFFFF
    xorval &= 0xFFFF
    res = val + rotate_left(val, 2)
    res = rotate_left(res, 4) ^ (res & (val ^ xorval))
    return res


def cps3_mask(address, key1, key2):
    address ^= key1
    val = ((address & 0xFFFF) ^ 0xFFFF)
    val = rotxor(val, key2 & 0xFFFF)
    val ^= (address >> 16) ^ 0xFFFF
    val = rotxor(val, key2 >> 16)
    val ^= (address & 0xFFFF) ^ (key2 & 0xFFFF)
    rel = (val | (val << 16))
    return rel


simm1_0 = open('sfiii3-simm1.0-unencrypted', 'rb')
simm1_1 = open('sfiii3-simm1.1-unencrypted', 'rb')
simm1_2 = open('sfiii3-simm1.2-unencrypted', 'rb')
simm1_3 = open('sfiii3-simm1.3-unencrypted', 'rb')

sfiii3s_keys = 0xA55432B4, 0x0C129981

simmProc = True
which = 0
allData = []
real_offset = 0
baseOffset = 0x6000000
simmFilesize = os.path.getsize('sfiii3-simm1.0-unencrypted')
outFile = open('sfiii3-binary-combined-and-encrypted', 'wb+')
target = 0x604A50, 0x604ADC
if which == 1:
    baseOffset += 0x800000
for i in range(0, simmFilesize):

    if simmProc:
        simm1_0_data = int.from_bytes(simm1_0.read(1), 'little')
        simm1_1_data = int.from_bytes(simm1_1.read(1), 'little')
        simm1_2_data = int.from_bytes(simm1_2.read(1), 'little')
        simm1_3_data = int.from_bytes(simm1_3.read(1), 'little')
        curData = ((simm1_0_data << 24) | (simm1_1_data << 16) | (simm1_2_data << 8) | (simm1_3_data << 0))

    newData = curData ^ (cps3_mask(baseOffset + (i * 4), 0xA55432B4, 0x0C129981))
    outFile.write(newData.to_bytes(4, 'big', signed=False))

simm1_0.close()
simm1_1.close()
simm1_2.close()
simm1_3.close()

outFile.close()

simm1_0 = open('sfiii3-simm1.0', 'wb+')
simm1_1 = open('sfiii3-simm1.1', 'wb+')
simm1_2 = open('sfiii3-simm1.2', 'wb+')
simm1_3 = open('sfiii3-simm1.3', 'wb+')

file_10 = open('sfiii3-binary-combined-and-encrypted', 'rb')

fileSize = os.path.getsize('sfiii3-binary-combined-and-encrypted')
for i in range(0, fileSize, 4):
    data = int.from_bytes(file_10.read(1), 'little')
    simm1_0.write(data.to_bytes(1, 'little', signed=False))
    data = int.from_bytes(file_10.read(1), 'little')
    simm1_1.write(data.to_bytes(1, 'little', signed=False))
    data = int.from_bytes(file_10.read(1), 'little')
    simm1_2.write(data.to_bytes(1, 'little', signed=False))
    data = int.from_bytes(file_10.read(1), 'little')
    simm1_3.write(data.to_bytes(1, 'little', signed=False))

file_10.close()
simm1_0.close()
simm1_1.close()
simm1_2.close()
simm1_3.close()