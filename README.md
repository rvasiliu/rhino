# rhino
python FTDI driver for WS2813

##  Installing dependencies using pip

`$ pip install -r requirements.txt`

## Running demo procedure

`$ python main.py`

## Ftdi output port settings

Open `spi_driver.py`.

Alter line 23: `s = 'ftdi://0x0403:0x6011/[X]'` where [X] is the port number. E.g. if using port A, use X=1, if port B, X=2 and so on. 
