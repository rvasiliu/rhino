
from data import LEDData
from WS2813 import WS2813_strip

class StripAnimation:
    """
    This class will perform actions onto the LEDData instance and it will yield out renders
    """

    def __init__(self): # feed in the strip object
        pass

    def cleanup(self):
        """
        Need this method to clear up all other actions before starting animation
        """
        pass

    def bargraph_one_way(self):
        """
        Method renders a bargraph like display, going fro DIN to DOUT
        """
        pass
