
import time
from pyftdi.spi import SpiController



class SPIDriver:
    """
    Class that contains the driver for the FTDI SPI + GPIO.
    """

    def __init__(self):
        self.ctrl = None
        self.slave = None
        print('Starting driver ...')
        self.begin()


    def begin(self):
        try:
            self.ctrl = SpiController(silent_clock=False)
            s = 'ftdi://0x0403:0x6011/2'
            self.ctrl.configure(s)
            self.slave = self.ctrl.get_port(cs=0, freq=10E6, mode=3)
            self.slave.set_frequency(4000000)
        except Exception as err:
            print('Error in initialising the FTDI driver ...:', err)

    def write_data_out(self, buffer):
        if not isinstance(buffer, bytes):
            raise Exception # TODO define exception
        try:
            self.slave.write(buffer)
            return True
        except Exception as err:
            #TODO convert to Logging
            print('Error in writing data out to FTDI SPI...:', err)
            return False

    def terminate(self):
        self.ctrl.terminate()
        print('terminated')