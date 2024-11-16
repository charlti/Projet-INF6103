import time
from pymodbus.client import ModbusTcpClient

client = ModbusTcpClient('0.0.0.0', port=502)

read_before = client.read_coils(0, 8)   # start reading from address 1
print(read_before.bits)
client.write_coil(0, False)
time.sleep(5)
reading_coil = client.read_coils(0, 8)   # start reading from address 1
print(reading_coil.bits)
