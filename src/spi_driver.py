
import time
from pyftdi.spi import SpiController, SpiGpioPort
from pyftdi.gpio import  GpioController, GpioException



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
            self.ctrl = SpiController(cs_count=1)
            s = 'ftdi://0x0403:0x6011/2'
            self.ctrl.configure(s)

            self.slave = self.ctrl.get_port(cs=0, freq=10E6, mode=3)
            self.slave.set_frequency(8000000)

            self.gpio = self.ctrl.get_gpio()
            self.gpio.set_direction(0x10, 0x10) # direction for the fet controller is OUTPUT (1)
            self.gpio.write(0x10)
            time.sleep(0.1)
            # to account for using separate ports for power and comms:
            self.backup_ctrl = SpiController(cs_count=1)
            self.backup_gpio = None
            if not s == 'ftdi://0x0403:0x6011/1':
                backup_s = 'ftdi://0x0403:0x6011/1'
                self.backup_ctrl.configure(backup_s)
                self.backup_gpio = self.backup_ctrl.get_gpio()
                self.backup_gpio.set_direction(0x10, 0x10)
                self.backup_gpio.write(0x10)
                time.sleep(1)
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

    def set_power_on(self):
        self.gpio.write(0x10)
        if self.backup_gpio is not None:
            self.backup_gpio.write(0x10)

    def set_power_off(self):
        self.gpio.write(0x00)
        if self.backup_gpio is not None:
            self.backup_gpio.write(0x00)

    def terminate(self):
        self.ctrl.terminate()
        print('terminated')