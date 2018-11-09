
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

    def render_animation(self, animation_procedure): # renders frame by frame
        self.cleanup()
        self._LED_data
        self._SPI_driver.write_data_out(self._LED_data.all_data)

    def cleanup(self):
        """
        this method turns all LEDs of. Does not turn power off.
        """
        self._LED_data.make_colour(red=0, green=0, blue=0)
        self.render()