#!/usr/bin/env python
#Jonathon Lefler
#

import sys
from SX127x.LoRa import *
from time import sleep
from SX127x.board_config import BOARD
from SX127x.LoRaArgumentParser import LoRaArgumentParser

parser = LoRaArgumentParser("A simple LoRa beacon")
parser.add_argument('--single', '-S', dest='single', default=False, action="store_true", help="Single transmission")
parser.add_argument('--wait', '-w', dest='wait', default=1, action="store", type=float, help="Waiting time between transmissions (default is 0s)")

class Node(LoRa):

	#Override
	def __init__(self, verbose=False): #
		super(Node, self).__init__(verbose)
		# setup registers etc.
		self.set_mode(MODE.SLEEP) #ONLY CHANGE REGS WHEN MODE = SLEEP
		self.set_dio_mapping([1,0,0,0,0,0])
		self.set_freq(915.0)

	#Override
	def on_rx_done(self): # When reading is done?
		payload = self.read_payload(nocheck=True)
		# etc.

	#Override
	def on_tx_done(self): # When Transmitting is done?
		global args
		self.set_mode(MODE.STDBY)
		self.clear_irq_flags(TxDone=1)
		if args.single:
			print("args exit")
			sys.exit(0)
		BOARD.led_off()
		print("Ending Transmission")
		BOARD.teardown()
		sys.exit(0)

	#Override
	def on_cad_done(self): #
		pass

	#Override
	def on_rx_timeout(self): # Recieving time out
		pass

	#Override
	def on_valid_header(self): #
		pass

	#Override
	def on_payload_crc_error(self): #
		pass

	#Override
	def on_fhss_change_channel(self): #
		pass

	def start(self, payload):
		global args
		print(self.get_freq())
		print("Starting Transmission")
		BOARD.led_on()
		self.write_payload(payload)
		self.set_mode(MODE.TX)
		while True:
			sleep(1)

if __name__ == '__main__':
	BOARD.setup()
	lora_n = Node()
	lora_n.set_mode(MODE.SLEEP)
	lora_n.set_freq(915.0)
	args = parser.parse_args(lora_n)
	payload = 1
	#payload = bytearray(payload, 'utf-8')
	#payload = payload.encode('utf-8')
	lora_n.start([payload])
