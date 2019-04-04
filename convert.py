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

i = 0
while i < len(data):
#	sys.stdout.write(str(i) + ": ")

	c = data[i]
	if c == 0x7a: # command line
		i += 1
		if i >= len(data):
			break
		sys.stdout.write('\u001b[7m')
		while c != 0x1f:
			if c < 0x20:
				sys.stdout.write(chr(c + 0x60))
			else:
				sys.stdout.write(chr(c))
			i += 1
			if i >= len(data):
				break
			c = data[i]
		sys.stdout.write('\u001b[0m')
		sys.stdout.write('\n')
	else: # text line
		while c != 0x1f:
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
			elif c == 0x6f: # space?
				sys.stdout.write('_')
			else:
				sys.stdout.write(chr(c))
			i += 1
			if i >= len(data):
				break
			c = data[i]
		sys.stdout.write('\n')
	i = int((i + line_length) / line_length) * line_length

#pprint.pprint(data)
