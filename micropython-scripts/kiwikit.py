from machine import Pin, Timer, I2C
from ssd1306 import SSD1306_I2C
from at24 import AT24

import framebuf

# the rpi logo
buffer=bytearray(b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00|?\x00\x01\x86@\x80\x01\x01\x80\x80\x01\x11\x88\x80\x01\x05\xa0\x80\x00\x83\xc1\x00\x00C\xe3\x00\x00~\xfc\x00\x00L'\x00\x00\x9c\x11\x00\x00\xbf\xfd\x00\x00\xe1\x87\x00\x01\xc1\x83\x80\x02A\x82@\x02A\x82@\x02\xc1\xc2@\x02\xf6>\xc0\x01\xfc=\x80\x01\x18\x18\x80\x01\x88\x10\x80\x00\x8c!\x00\x00\x87\xf1\x00\x00\x7f\xf6\x00\x008\x1c\x00\x00\x0c\x00\x00\x03\xc0\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00")

# init screen
i2c = I2C(1, scl=Pin(19), sda=Pin(18), freq=100000)
oled = SSD1306_I2C(128, 64, i2c)

# copy over logo
fb = framebuf.FrameBuffer(buffer, 32, 32, framebuf.MONO_HLSB)
oled.fill(0)
oled.blit(fb, 48, 16)

# write some text
oled.text('Hello PICO!', 0, 0)
oled.text('     Kiwikit', 32, 56)
oled.show()

# init eeprom
eeprom = AT24(A2_value=1, i2c=i2c)

writebuf = bytearray(2)
writebuf[0] = 0x01;
writebuf[1] = 0x02;
addr = 0x000;
eeprom.write_bytes(addr, writebuf)
memory = eeprom.read_bytes(addr, 2)
print(memory)

greenLed = Pin(17, Pin.OUT)
redLed = Pin(22, Pin.OUT)

tim = Timer()
def tick(timer):
    greenLed.toggle()
    redLed.toggle()
    
tim.init(freq=1, mode=Timer.PERIODIC, callback=tick)
