from pymodbus.client.sync import ModbusTcpClient
from pymodbus.exceptions import ModbusIOException

def read_all_registers(ip, port, start_address=0, count=125):
    """
    Reads all holding registers from a Modbus server.
    
    :param ip: IP address of the Modbus server
    :param port: Port number of the Modbus server
    :param start_address: Starting register address (default is 0)
    :param count: Number of registers to read in each batch (default is 125, max allowed per request)
    """
    try:
        client = ModbusTcpClient(ip, port)
        if not client.connect():
            print(f"Failed to connect to Modbus server at {ip}:{port}")
            return
        
        print(f"Connected to Modbus server at {ip}:{port}")
        register_values = []
        
        while True:
            # Read holding registers
            response = client.read_holding_registers(start_address, count)
            if isinstance(response, ModbusIOException) or not response.isError():
                # If we received valid data
                if response.registers:
                    register_values.extend(response.registers)
                    print(f"Read registers {start_address} to {start_address + len(response.registers) - 1}: {response.registers}")
                    start_address += len(response.registers)
                else:
                    print("No more data to read.")
                    break
            else:
                print(f"Error reading registers at address {start_address}")
                break
            
        print("All register values:", register_values)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        client.close()

# Example usage
if __name__ == "__main__":
    ip_address = "192.168.1.100"  # Replace with your Modbus server's IP
    port_number = 502            # Replace with your Modbus server's port
    read_all_registers(ip_address, port_number)
