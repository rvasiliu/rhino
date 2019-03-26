import time
from pyftdi.spi import SpiController

ctrl = SpiController(silent_clock=False)
s = 'ftdi://0x0403:0x6011/1'
ctrl.configure(s)
slave = ctrl.get_port(cs=0, freq=6E6, mode=0)


#for k in range(100):
slave.set_frequency(6000000)

while(1):

    write_buf=b'\xC0\xC0\xFC\xFC\xFC\xFC\xC0\xC0\xC0\xC0\xC0\xC0\xC0\xC0\xC0\xC0\xC0\xC0\xC0\xC0\xC0\xC0\xC0\xC0'
    write_buf = write_buf * 82
   # slave.write(write_buf)
   # print(slave.read(82*24))
    read_buf = slave.exchange(write_buf, duplex = True).tobytes()
    print(read_buf)
    time.sleep(0.1)

    write_buf=bytearray(write_buf)  #b'\x88\x88\x88\x88\xEE\x88\x88\x88\x88\x88\x88\x88'
    write_buf.reverse() # = write_buf
    slave.write(write_buf)
    time.sleep(0.1)
