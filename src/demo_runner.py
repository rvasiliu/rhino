import time
from pyftdi.spi import SpiController

ctrl = SpiController(silent_clock=False)
s = 'ftdi://0x0403:0x6011/1'
ctrl.configure(s)
slave = ctrl.get_port(cs=0, freq=3E6, mode=3)


for k in range(100):
    slave.set_frequency(4000000)

    write_buf=b'\xEE\x88\xEE\x88\x88\x88\x88\x88\x88\x88\x88\x88'
    write_buf = write_buf * 100
    slave.write(write_buf)
    time.sleep(1)

    write_buf=b'\x88\x88\x88\x88\xEE\x88\x88\x88\x88\x88\x88\x88'
    write_buf = write_buf * 100
    slave.write(write_buf)
    time.sleep(1)
