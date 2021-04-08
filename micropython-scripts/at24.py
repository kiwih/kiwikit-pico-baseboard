from micropython import const

AT24_ROOT_ADDR = const(0xA)

class AT24Exception(Exception):
    pass

class AT24():
    """AT24 class. Manages read/write access to an AT24 EEPROM. 

    Example usage:
    # init i2c
    i2c = I2C(1, scl=Pin(19), sda=Pin(18), freq=100000)

    # init eeprom
    eeprom = AT24(A2_value=1, i2c=i2c)
    
    writebuf = bytearray(2)
    writebuf[0] = 0x01;
    writebuf[1] = 0x02;
    addr = 0x000;
    eeprom.write_bytes(addr, writebuf)
    memory = eeprom.read_bytes(addr, 2)
    print(memory)
    """
    
    def __init__(self, A2_value, i2c):
        """Set up an AT24 class. "A2_value" should be either '1' or '0' and represents the state of the A2 address pin on the AT24 chip. "i2c" is a pre-initialized i2c class."""
        self.A2_value = A2_value
        self.i2c = i2c
        
    def write_bytes(self, address, write_bytearray):
        """Writes up to 16 bytes starting at 10-bit address [address]. All bytes must be on the same page boundary (that is, A[9]-A[4] should be constant). "write_bytearray" is a bytearray."""
        i2c_addr = AT24_ROOT_ADDR << 3 | self.A2_value << 2 | (address & 0x300) >> 8
        mem_addr = address & 0xFF
        
        #The proper way to check if the AT24 chips are ready is to poll the write address and check the NACK.
        #Unfortunately, this isn't possible in the RP2040 port of MicroPython as the low-level I2C functions are not supported
        #Instead, we have to do this using exceptions (an OSError is thrown if the AT24 NACKS)
        #So, this works, but is less efficient than it could be
        attempts = 0
        while attempts < 50: 
            attempts = attempts + 1
            try:
                self.i2c.writeto_mem(i2c_addr, mem_addr, write_bytearray)
                break
            except OSError:
                pass
        
        if attempts >= 50:
            raise AT24Exception("AT24: Write operation timed out (check the address?)")
        
    def read_bytes(self, address, n):
        """Read up to n bytes starting at 10-bit address [address]. Returned as a bytes object."""
        i2c_addr = AT24_ROOT_ADDR << 3 | self.A2_value << 2 | (address & 0x300) >> 8
        mem_addr = address & 0xFF
        #The proper way to check if the AT24 chips are ready is to poll the write address and check the NACK.
        #Unfortunately, this isn't possible in the RP2040 port of MicroPython as the low-level I2C functions are not supported
        #Instead, we have to do this using exceptions (an OSError is thrown if the AT24 NACKS)
        #So, this works, but is less efficient than it could be
        attempts = 0
        while attempts < 50: 
            attempts = attempts + 1
            try:
                data = self.i2c.readfrom_mem(i2c_addr, mem_addr, n)
                break
            except OSError:
                pass
        
        if attempts >= 50:
            raise AT24Exception("AT24: Read operation timed out (check the address?)")
        
        return data
