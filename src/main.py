import time
from spi_driver import SPIDriver

class LEDData:
    """
    Class to repseset the LED data for all the strip.
    Data is represented as one big array of defined length.
    Each pixel in the data array is one 3 element array, where each element is one byte (0-255).
    The processed_data array will be one big array of all the bytes that have to be sent out on the strip.
    """
    class pixel:

        def __init__(self, pixel_id=0, R_data=0, G_data=0, B_data=0):
            self.R = R_data
            self.G = G_data
            self.B = B_data
            self.pixel_id = pixel_id

        @property
        def data(self):
            return [self.R, self.G, self.B]


    def __init__(self, led_count):
        """ the LED strip has 82 LEDs"""
        self.virtual_data_array = [self.pixel(pixel_id=pixel_id) for pixel_id in range(led_count)]
        #self.make_colour()

    def make_colour(self):
        """
        This method makes the entire virtual data array be one colour only.
        """
        # use only one color for now
        for p in self.virtual_data_array:
            p.R = 0
            p.G = 255
            p.B = 0

    def slide_pixel(self, led_strip_handle):
        for k in range(len(self.virtual_data_array)-1):
            self.virtual_data_array[k].R = 0
            self.virtual_data_array[k+1].R = 255

            led_strip_handle.write_data_out(self.all_data)
            #time.sleep(1)
        self.virtual_data_array[-1].R = 0
        led_strip_handle.write_data_out(self.all_data)

        for k in range(len(self.virtual_data_array)-1, 0, -1):
            self.virtual_data_array[k].B = 0
            self.virtual_data_array[k-1].B = 255

            led_strip_handle.write_data_out(self.all_data)
            #time.sleep(1)
        self.virtual_data_array[0].B = 0
        led_strip_handle.write_data_out(self.all_data)

    def convert_virtual_pixel(self, virtual_pixel):
        """
        This methods convert the whole pixel array (of 3 elements) into the SPI type pixel
        """
        sequence = b''
        for colour in virtual_pixel:
            sequence += self.convert_single_byte_to_spi(color_byte=colour)
        return sequence

    def convert_single_byte_to_spi(self, color_byte):
        """
        This method takes in the byte representing the color
        and converts it to the 4 bytes that have to be shifted out of MOSI
        """
        if isinstance(color_byte, bytes):
            color_byte = int.from_bytes(color_byte, byteorder='big')
        in_bytes = 0
        for offset in range(7, -1, -1):
            bit = (color_byte >> offset) & 0b00000001
            if bit == 1:
                nibble = 0b1110
            elif bit == 0:
                nibble = 0b1000
            in_bytes = (in_bytes << 4) + nibble
        # convert in_bytes to bytes.
        return in_bytes.to_bytes(4, byteorder='big')

    def convert_to_spi_raw(self):
        """
        This method takes the LED data array (virtual one) and converts it to SPI data
        OUTPUT will be one big array of bytes
        """
        bytes_out = b''
        for pixel in self.virtual_data_array:
            bytes_out += self.convert_virtual_pixel([pixel.R, pixel.G, pixel.B])
        return bytes_out

    @property
    def all_data(self):
        return self.convert_to_spi_raw()


class WS2813_strip:
    """
    Class to represent the strip itself
    """
    def __init__(self, SPI_driver, LED_data):
        self._SPI_driver = SPI_driver() # this is the spi driver object, instantiated
        self._LED_data = LED_data(82) # have this be another object which represents the LED data

    def render(self):
        """
        This method, when called, renders the display set in LED data
        """
        buffer = self._LED_data.all_data
        self._SPI_driver.write_data_out(buffer=buffer)

    def render_slide(self):
        self._LED_data.slide_pixel(self._SPI_driver)


if __name__=='__main__':

    S = WS2813_strip(LED_data=LEDData, SPI_driver=SPIDriver)
    while 1:
        S.render_slide()
    #S._SPI_driver.terminate()

    print('done')