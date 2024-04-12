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
         \               J3 10 9 8 7 6 5 4 3 2 1 |
          \______________________________________|


| J3 | JTAG | SPI  | UART |
|----|------|------|------|
| 10 | TCK  | CLK  |      |
| 9  | TDI  | MOSI |      |
| 8  | TDO  | MISO |      |
| 7  | TMS  | CS   |      |
| 6  | RST  |      |      |
| 5  |      |      | TX   |
| 4  |      |      | RX   |
| 3  |      |      |      |
| 2  |        GND         |
| 1  |        3V3         |


## Usage
### openFPGALoader
[openFPGALoader](https://github.com/trabucayre/openFPGALoader) can be used to configure and flash FPGAs with option `-c ft2232_b`

```bash
openFPGALoader -c ft2232_b <other options>
```


### FlashROM
[FlashROM](https://wiki.flashrom.org/FT2232SPI_Programmer) can be used to read / program SPI FLASH chips. Here is how to use it with icetag:

```bash
flashrom -p ft2232_spi:type=2232H,port=B,divisor=8
```
you might want to try different `divisor` value depending on your board.


## (optional) Enabling the UART
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
