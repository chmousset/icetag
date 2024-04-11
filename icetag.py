from migen import *
from migen.build.platforms.icestick import Platform, _connectors
from migen.build.generic_platform import Pins, IOStandard, Subsignal

gpio0_ios = _connectors[0][1].split()
# gpio1_ios = _connectors[1][1].split()
io = [
    ("jtag", 0,
        Subsignal("tck", Pins(gpio0_ios[0])),
        Subsignal("tdi", Pins(gpio0_ios[1])),
        Subsignal("tdo", Pins(gpio0_ios[2])),
        Subsignal("tms", Pins(gpio0_ios[3])),
        Subsignal("rst", Pins(gpio0_ios[4])),
        IOStandard("LVTTL"),
    ),
    ("uart", 0,
        Subsignal("tx", Pins(gpio0_ios[5])),
        Subsignal("rx", Pins(gpio0_ios[6])),
        IOStandard("LVTTL"),
    ),
]

class icetag(Module):
	"""Simple JTAG and UART pass-through for icestick"""
	def __init__(self, plat):
		plat.add_extension(io)

		# Connect the FTDI port A (spiflash) as UART
		# Connect the FTDI port B (serial) as JTAG
		# Only port B can be used as JTAG since the A port lacks the TMS
		# connection
		jtag = plat.request("jtag")
		ft2232 = plat.request("serial")
		spiflash = plat.request("spiflash")
		uart = plat.request("uart")

		self.comb += [
			# JTAG
			jtag.tck.eq(ft2232.rx),
			jtag.tdi.eq(ft2232.tx),
			ft2232.rts.eq(jtag.tdo),
			jtag.tms.eq(ft2232.cts),
			jtag.rst.eq(ft2232.dtr),

			# UART
			spiflash.mosi.eq(uart.rx),
			uart.tx.eq(spiflash.clk),
		]

		# LED5 slowly blinks to indicate icestick is correctly flashed
		counter = Signal(max=int(12e6))
		self.sync += counter.eq(counter + 1)
		led = plat.request("user_led", 4)
		self.comb += led.eq(counter[-1])

		# LED1 and 2 blink each time some data goes on the UART lines
		led_cnt = Signal(max=int(12e6/10))
		led_tx = plat.request("user_led", 0)
		led_rx = plat.request("user_led", 1)
		self.sync += [
			led_cnt.eq(led_cnt+1),
			If(led_cnt == 0,
				led_tx.eq(0),
				led_rx.eq(0),
			).Else(
				If(uart.tx == 0,
					led_tx.eq(1)
				),
				If(uart.rx == 0,
					led_rx.eq(1)
				),
			)
		]

plat = Platform()
top = icetag(plat)
plat.build(top)
plat.create_programmer().flash(0, "build/top.bin")
