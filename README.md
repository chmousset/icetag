# ICETAG - using icestick as JTAG adapter

## Goal
The icestick is a simple, inexpensive FPGA dev board with an onboard FT2232H.
The FT2232H has two MPSSE ports that can act as UART, JTAG, FIFO or SPI interfaces.
This project allows to use an icestick as an JTAG+UART interface.

## Pinout

           ______________________________________
          /                  o o o o o o o o o o |
       __/           _________    | 3V3 | 3V3 |  |
     _____          |         |   | GND | GND |  |
    |     |         |         |   |  7  |  3  |  |
    | USB |         |  ICE40  |   |  6  |  2  |  |
    |_____|         |         |   |  5  |  1  |  |
       __           |_________|   |  4  |  0  |  |
         \               J3  o o o o o o o o o o |
          \______________________________________|
                             T T T T R n n n G 3
                             C D D M S c c c N V
                             K I O S T       D 3


## Enabling the UART
The FT2232 has an EEPROM attached which stores some configuration parameters.
By default, the MPSSE port A is configured as a FIFO which can apparently prevents Linux from using is correctly as an UART.

Unfortunately, the only fix for this issue it to re-program the EEPROM with FTDI-s FT-PROG tool, which is windows-only :(
Or remove the EEPROM :)


2 configurations are provided in `ftprog/` directory:
 * `icestick_default_ftdi_config.xml` : the default configuration
 * `icestick_2uart_ftdi_config.xml` : dual UART-capable configuration

ftdlib also has a `ftdi_eeprom` utility that seems to be able to read/write the EEPROM, altough it was not verified to be functional. You can try this:
```
cd ftprog
git clone https://github.com/nblock/libftdi.git
cd libftdi
cmake .
make
cd ..
./libftdi/ftdi_eeprom/ftdi_eeprom --write-eeprom ftdi_eeprom_2uart.conf
```
