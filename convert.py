import pprint
import sys

if len(sys.argv) < 1:
	print('Usage: python convert.py <filename>')
	sys.exit(1)

with open(sys.argv[1], mode='rb') as f:
	data = bytearray(f.read())

if data[0] == 0xc0 and data[1] == 0x5b:
	line_length = 80
elif data[0] == 0x98 and data[1] == 0x4c:
	line_length = 40
else:
	print('Unknown file format: ' + sys.argv[1])
	sys.exit(1)

data = data[2:]

while len(data):
	line = data[:line_length]
	data = data[line_length:]

	if line[0] == 0x7a: # command line
		command = ''
		while True:
			line = line[1:]
			if len(line) == 0:
				break
			c = line[0]
			if c == 0x1f:
				break
			if c < 0x20:
				command += chr(c + 0x60)
			else:
				command += chr(c)
		if command.startswith('ln'):
			for i in range(0, int(command[2])):
				sys.stdout.write('\n')
		else:
			sys.stdout.write('\u001b[7m' + command + '\u001b[0m\n')
	else: # text line
		while True:
			c = line[0]
			if c == 0x1f:
				sys.stdout.write('\n')
				break
			if c == 0x6d: # bold on
				sys.stdout.write('\u001b[1m')
			elif c == 0x7d: # bold off
				sys.stdout.write('\u001b[0m')
			elif c == 0x7c: # underline on
				sys.stdout.write('\u001b[4m')
			elif c == 0x7e: # underline off
				sys.stdout.write('\u001b[0m')
			elif c < 0x20:
				sys.stdout.write(chr(c + 0x60))
			elif c == 0x6f: # leading space
				sys.stdout.write(' ')
			else:
				sys.stdout.write(chr(c))
			line = line[1:]
			if len(line) == 0:
				break

#pprint.pprint(data)
