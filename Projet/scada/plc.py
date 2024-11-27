from pymodbus.server import StartTcpServer
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext
from pymodbus.datastore import ModbusSequentialDataBlock

# Configuration des registres Modbus (ici Holding Registers)
store = ModbusSlaveContext(
    co=ModbusSequentialDataBlock(0, [True] * 10)  # 10 registres, initialisés à 0
)
context = ModbusServerContext(slaves=store, single=True)

# Identification du dispositif simulé
identity = ModbusDeviceIdentification()
identity.VendorName = 'Python-PLC'
identity.ProductCode = 'PLC001'
identity.VendorUrl = 'https://example.com'
identity.ProductName = 'Python Modbus PLC'
identity.ModelName = 'PLC Simulator'
identity.MajorMinorRevision = '1.0'

# Fonction principale pour lancer le serveur
def run_server():
    print("Starting Modbus server...")
    StartTcpServer(context=context, identity=identity, address=("0.0.0.0", 502))

if __name__ == "__main__":
    run_server()
