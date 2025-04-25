class TimeCounter:
	def __init__(self, t0):
		self.t = t0
		self.t0 = t0
	def update_time(self, dt):
		self.t += dt
	def print_time(self):
		print("current time: ", self.t)
	def reset(self):
		self.t = self.t0
		
class EventWatcher:
	def __init__(self):
		self.raisehead = False
		self.headsup = False
		self.wavetail = False
		self.lowerhead = False
		self.attack = False
		self.waitattack = False
		self.moving = False
