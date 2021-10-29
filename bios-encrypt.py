import os


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


input_simm1_0 = 0
input_simm1_1 = 0
input_simm1_2 = 0
input_simm1_3 = 0
output_simm1_0 = 0
output_simm1_1 = 0
output_simm1_2 = 0
output_simm1_3 = 0
in_file = 0
in_file += 0
outFile = 0

sfiii3s_keys = 0xA55432B4, 0x0C129981
baseOffset = 0x0000000

simm_input = False
simm_output = False
simm2_processing = False

if simm_input:
    input_simm1_0 = open('sfiii3n-simm1.0', 'rb')
    input_simm1_1 = open('sfiii3n-simm1.1', 'rb')
    input_simm1_2 = open('sfiii3n-simm1.2', 'rb')
    input_simm1_3 = open('sfiii3n-simm1.3', 'rb')
    file_size = os.path.getsize('sfiii3n-simm1.0')
else:
    single_filename = 'sfiii3_japan_nocd.29f400.u2'
    in_file = open('3rdstrikebios-decrypted.bin', 'rb')
    file_size = os.path.getsize('3rdstrikebios-decrypted.bin') >> 2

if simm_output:
    output_simm1_0 = open('sfiii3n-simm1.0', 'wb+')
    output_simm1_1 = open('sfiii3n-simm1.1', 'wb+')
    output_simm1_2 = open('sfiii3n-simm1.2', 'wb+')
    output_simm1_3 = open('sfiii3n-simm1.3', 'wb+')
else:
    outFile = open('3rdstrikebios-encrypted.bin', 'wb+')

if simm2_processing:
    baseOffset += 0x800000

for i in range(0, file_size):
    if simm_input:
        simm1_0_data = int.from_bytes(input_simm1_0.read(1), 'little')
        simm1_1_data = int.from_bytes(input_simm1_1.read(1), 'little')
        simm1_2_data = int.from_bytes(input_simm1_2.read(1), 'little')
        simm1_3_data = int.from_bytes(input_simm1_3.read(1), 'little')
        curData = ((simm1_0_data << 24) | (simm1_1_data << 16) | (simm1_2_data << 8) | (simm1_3_data << 0))
    else:
        curData = int.from_bytes(in_file.read(4), 'big')

    newData = curData ^ (cps3_mask(baseOffset + (i * 4), 0xA55432B4, 0x0C129981))
    if simm_output:
        simm1_0_data = (newData & 0xFF000000) >> 24
        simm1_1_data = (newData & 0x00FF0000) >> 16
        simm1_2_data = (newData & 0x0000FF00) >> 8
        simm1_3_data = (newData & 0x000000FF)
        output_simm1_0.write(simm1_0_data.to_bytes(1, 'little', signed=False))
        output_simm1_1.write(simm1_1_data.to_bytes(1, 'little', signed=False))
        output_simm1_2.write(simm1_2_data.to_bytes(1, 'little', signed=False))
        output_simm1_3.write(simm1_3_data.to_bytes(1, 'little', signed=False))
    else:
        outFile.write(newData.to_bytes(4, 'big', signed=False))

if simm_output:
    output_simm1_0.close()
    output_simm1_1.close()
    output_simm1_2.close()
    output_simm1_3.close()
else:
    outFile.close()

if simm_input:
    input_simm1_0.close()
    input_simm1_1.close()
    input_simm1_2.close()
    input_simm1_3.close()
else:
    in_file.close()
