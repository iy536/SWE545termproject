
import threading

class GameThread(threading.Thread)
	def __init__(self):
		threading.Thread(self)
	def run(self):
		pritnf("Threading...")