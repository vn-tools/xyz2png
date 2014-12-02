#!/usr/bin/python
import io
import struct
import sys
import zlib
from PIL import Image

if len(sys.argv) < 3:
	print >>sys.stderr, 'Usage: ' + sys.argv[0] + ' INPUT OUPTUT'
	sys.exit(1)

input_path = sys.argv[1]
output_path = sys.argv[2]

with open(input_path, 'rb') as input_fh:
	magic = input_fh.read(4)
	if magic != 'XYZ1':
		print >>sys.stderr, 'Unsupported file type: ' + magic
		sys.exit(1)
	width, height = struct.unpack('=HH', input_fh.read(4))
	rest = input_fh.read()
	rest = zlib.decompress(rest)
	rest = io.BytesIO(rest)
	palette = []
	for x in range(256):
		r, g, b = struct.unpack('=3B', rest.read(3))
		palette.append((r, g, b))

	output_image = Image.new('RGBA', (width, height))
	output_pixels = output_image.load()

	for y in range(height):
		for x in range(width):
			output_pixels[x,y] = palette[ord(rest.read(1))]

	output_image.save(output_path)
