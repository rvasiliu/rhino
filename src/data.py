

class LEDData:
    """
    Class to represent the LED data for all the strip.
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
            return [self.G, self.R, self.B]


    def __init__(self, led_count):
        """ the LED strip has 82 LEDs"""
        self.virtual_data_array = [self.pixel(pixel_id=pixel_id) for pixel_id in range(led_count)]

    def make_colour(self, red, green, blue):
        """
        This method makes the entire virtual data array be one colour only.
        """
        for p in self.virtual_data_array:
            p.R = red
            p.G = green
            p.B = blue

    def make_pixel_colour(self, pixel=pixel, red=0, green=0, blue=0):
        """
        Method sets pixel colour.
        """
        pixel.R = red
        pixel.G = green
        pixel.B = blue

    def make_pixel_colour_by_id(self, pixel_id=0, red=0, green=0, blue=0):
        """
        Method set pixel colour.
        """
        self.virtual_data_array[pixel_id].R = red
        self.virtual_data_array[pixel_id].G = green
        self.virtual_data_array[pixel_id].B = blue

    def slide_pixel(self, led_strip_handle):
        """
        This is a test method to slide a pixel across the stip.
        """
        for k in range(len(self.virtual_data_array)-1):
            self.make_pixel_colour_by_id(pixel_id=k,
                                         red=0,
                                         green=0,
                                         blue=0)
            self.make_pixel_colour_by_id(pixel_id=k+1,
                                         red=0,
                                         green=0,
                                         blue=255)
            led_strip_handle.write_data_out(self.all_data)
        self.make_pixel_colour_by_id(pixel_id=-1,
                                     red=0,
                                     green=0,
                                     blue=0)
        led_strip_handle.write_data_out(self.all_data)
        for k in range(len(self.virtual_data_array)-1, 0, -1):
            self.make_pixel_colour_by_id(pixel_id=k,
                                         red=0,
                                         green=0,
                                         blue=0)
            self.make_pixel_colour_by_id(pixel_id=k-1,
                                         red=255,
                                         green=0,
                                         blue=0)
            led_strip_handle.write_data_out(self.all_data)
        self.make_pixel_colour_by_id(pixel_id=0,
                                     red=0,
                                     green=0,
                                     blue=0)
        led_strip_handle.write_data_out(self.all_data)

    def slide_pixel_smooth(self, led_strip_handle):
        """
                This is a test method to slide a pixel across the strip.
                Smooth version
                """
        for k in range(len(self.virtual_data_array) - 4):
            self.make_pixel_colour_by_id(pixel_id=k,
                                         red=0,
                                         green=0,
                                         blue=0)
            self.make_pixel_colour_by_id(pixel_id=k + 1,
                                         red=0,
                                         green=0,
                                         blue=64)
            self.make_pixel_colour_by_id(pixel_id=k + 2,
                                         red=0,
                                         green=0,
                                         blue=128)
            self.make_pixel_colour_by_id(pixel_id=k + 3,
                                         red=0,
                                         green=0,
                                         blue=255)
            self.make_pixel_colour_by_id(pixel_id=k + 4,
                                         red=0,
                                         green=0,
                                         blue=128)
            led_strip_handle.write_data_out(self.all_data)
        self.make_pixel_colour_by_id(pixel_id=-1,
                                     red=0,
                                     green=0,
                                     blue=0)
        led_strip_handle.write_data_out(self.all_data)
        for k in range(len(self.virtual_data_array) - 1, 0, -1):
            self.make_pixel_colour_by_id(pixel_id=k,
                                         red=0,
                                         green=0,
                                         blue=0)
            self.make_pixel_colour_by_id(pixel_id=k - 1,
                                         red=255,
                                         green=0,
                                         blue=0)
            led_strip_handle.write_data_out(self.all_data)
        self.make_pixel_colour_by_id(pixel_id=0,
                                     red=0,
                                     green=0,
                                     blue=0)
        led_strip_handle.write_data_out(self.all_data)

    def convert_virtual_pixel(self, virtual_pixel):
        """
        This methods convert the whole pixel array (of 3 elements) into the SPI type pixel
        """
        sequence = b''
        for colour in virtual_pixel:
            sequence += self.convert_single_byte_to_spi(color_byte=colour)
        return sequence

    def convert_single_byte_to_spi_4mhz(self, color_byte):
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

    def convert_single_byte_to_spi(self, color_byte):
        """This method is identical to convert_single_byte_to_spi but it converts each bit to one byte. For running at 6Mhz."""
        if isinstance(color_byte, bytes):
            color_byte = int.from_bytes(color_byte, byteorder='big')
        in_bytes = 0
        for offset in range(7, -1, -1):
            bit = (color_byte >> offset) & 0b00000001
            if bit == 1:
                byte = 0b11111100
            elif bit == 0:
                byte = 0b11000000
            in_bytes = (in_bytes << 8) + byte
        # convert in_bytes to bytes.
        return in_bytes.to_bytes(8, byteorder='big')

    def convert_to_spi_raw(self):
        """
        This method takes the LED data array (virtual one) and converts it to SPI data
        OUTPUT will be one big array of bytes
        """
        bytes_out = b''
        for pixel in self.virtual_data_array:
            bytes_out += self.convert_virtual_pixel([pixel.G, pixel.R, pixel.B])
        return bytes_out

    @property
    def all_data(self):
        return self.convert_to_spi_raw()
