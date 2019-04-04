import pprint
import sys

with open('files/chapter 1-a', mode='rb') as f:
	data = bytearray(f.read())[2:]

for i in range(0, int(len(data)/80)):
	line = data[i * 80 : (i + 1) * 80]

	if line[0] == 0x7a:
		sys.stdout.write('\u001b[7m')
		for c in line[1:-1]:
			if c < 0x20:
				sys.stdout.write(chr(c + 0x60))
			else:
				sys.stdout.write(chr(c))
		sys.stdout.write('\u001b[0m')
		sys.stdout.write('\n')
		continue

	j = 0
	while j < 80:
		c = line[j]
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
		else:
			sys.stdout.write(chr(c))
		j += 1
	sys.stdout.write('\n')

#pprint.pprint(data)
