class LineProcessor(object):

	def __init__(self, centr):
		self.centr = centr

	def leftLine(self, lines):
		temp = []
		for line in lines:
			if line[2] < self.centr:
				temp.append(line)
		if len(temp) > 0:
			left = temp[0]
			for line in temp[1:]:
				if line[2] > left[2]:
					left = line
			return left
		return None

	def rightLine(self, lines):
		temp = []
		for line in lines:
			if line[2] > self.centr:
				temp.append(line)
		if len(temp) > 0:
			right = temp[0]
			for line in temp[1:]:
				if line[2] < right[2]:
					right = line
			return right
		return None