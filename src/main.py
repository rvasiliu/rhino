import time
from spi_driver import SPIDriver
from data import LEDData
from WS2813 import WS2813_strip
from animation import StripAnimation


if __name__=='__main__':

    S = WS2813_strip(LED_data=LEDData, SPI_driver=SPIDriver)
    S.cleanup()
    S._LED_data.make_colour(red=100, green=0, blue=0)
    S.render_slide()
    while True:
        for k in range(127):
            S._LED_data.make_colour(red=2*k, green=0, blue=0)
            S.render()

            #time.sleep(1)
        S.render_slide()
    S.cleanup()
    print('done')