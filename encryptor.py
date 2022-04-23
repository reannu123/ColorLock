from time import sleep
class Encryptor:
	def __init__(self, grid,inputfile,outputfile,target_when_done):
		self.inputfile = inputfile
		self.outputfile = outputfile
		self.grid = grid
		self.key =""
		self.make_key()
		self.execute = target_when_done
		
	def make_key(self):
		init_key = ""
		for z in range(25):
			tilecolor=self.grid.get_tile(z)
			init_key += tilecolor
		overall = 0
		for character in range(25):
			if character%3 == 0:
				overall -= (ord(init_key[character])%25)^(character+26)
			else:
				overall += (ord(init_key[character])%25)^(character+26)
		overall = abs(overall)%256
		tile_shifts=[(ord(init_key[x])+ord(init_key[x+1])-x)^overall for x in range(23,-1,-1)]
		tile_shifts.append(overall^(ord(init_key[24])+ord(init_key[0])))
		for shift in tile_shifts:
			self.key += "".join([chr(ord(current_place)^shift) for current_place in init_key])
		self.key=self.key.encode()
		self.key_length = 625

	def extend(self):
		offset = self.key_length//5
		self.key =  self.key[4*offset:] + self.key[:4* offset] + self.key
		self.key_length = self.key_length * 2

	def truncate(self):
		self.key = self.key[:self.filesize]
		self.key_length = self.filesize

	def crypt(self):
		input = open(self.inputfile,"rb")
		self.filesize = input.seek(0,2)
		input.close()
		input = open(self.inputfile,"rb")
		while self.key_length < self.filesize:
			self.extend()
			sleep(0.000001)
		self.truncate()
		output = open(self.outputfile, "wb")
		for current_position in range(self.filesize):
			encrypted = int.from_bytes(input.read(1),"little") ^ self.key[current_position]
			output.write(encrypted.to_bytes(1,"little"))
			if current_position%16384==0:
				sleep(0.000001)
		input.close()
		output.close()
		self.execute()

	def large_crypt(self):
		for i in range(8):
			self.extend()
			sleep(0.000001)
		input = open(self.inputfile,"rb")
		self.filesize = input.seek(0,2)
		input.close()
		input = open(self.inputfile,"rb")
		output = open(self.outputfile, "wb")
		for current_position in range(self.filesize):
			encrypted = int.from_bytes(input.read(1),"little") ^ self.key[current_position%self.key_length]
			output.write(encrypted.to_bytes(1,"little"))
			if current_position%16384==0:
				sleep(0.000001)

		input.close()
		output.close()
		self.execute()
#Citations
#The syntax for sleeping was adapted from https://www.tutorialspoint.com/python/time_sleep.htm
#The syntax for setting file pointer positions was taken from https://www.tutorialsteacher.com/python/python-read-write-file
#The syntax for reading and writing binary files was taken from https://www.tutorialsteacher.com/python/python-read-write-file and the built-in help file for python's file objects.
#The syntax for XOR was taken from https://python-reference-readthedocs.io/en/latest/docs/operators/bitwise_XOR.html
#The syntax for encoding strings as bytes and converting integers to and from bytes was taken from https://docs.python.org/3/library/stdtypes.html		
