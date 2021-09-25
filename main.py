from PIL import Image
import ffmpeg
import argparse
from pixelight import Pixelight
import os
import shutil

'''
	Extract frames from a video file
'''

def extractFrames(input_path):
	ffmpeg.input(input_path).output('frames/out%d.png').run(quiet=True)
	
'''
	Compress frames into a video
'''

def compressFrames(fps, output_path):
	ffmpeg.input("render/out%d.png").filter('fps', fps=fps, round='up').output(output_path, pix_fmt='yuv420p').run(quiet=True, overwrite_output=True)
	

'''
	Remove cache files including extracted frames and rendered frames
'''

def resetCache():
	shutil.rmtree("frames", ignore_errors=True)
	os.mkdir("frames")
	shutil.rmtree("render", ignore_errors=True)
	os.mkdir("render")

parser = argparse.ArgumentParser()
parser.version = 'Pixelight v0.1.0 by Eduard Anton'
parser.add_argument('-v', '--version', action='version')
parser.add_argument('file',
					metavar='file',
					type=str,
					help='Source file (*.png, *.jpg, *.jfif, *.bmp, *.mp4, *.avi, *.mov, *.gif)')
parser.add_argument('-s',
					metavar='pixelation',
					action='store',
					type=float,
					default=10,
					help='Pixelation factor (default is 10)')
parser.add_argument('-p',
					metavar='palette',
					action='store',
					type=str,
					default='default',
					help='Palette (default is None) (default, auto, auto2, colorful, grey)')
parser.add_argument('-c',
					metavar='colors_count',
					action='store',
					type=int,
					default=10,
					help='Colors counts (default is 10)')
parser.add_argument('-o',
					metavar='output',
					action='store',
					type=str,
					default='output',
					help='Output file')
parser.add_argument('-f',
					metavar='framerate',
					action='store',
					type=int,
					default=10,
					help='Output framerate (default is 10)')

args = parser.parse_args()

# Check if the file exists
if os.path.exists(args.file):
	
	# Image file
	if args.file.endswith('.png') or args.file.endswith('.jpg') or args.file.endswith('.jfif') or  args.file.endswith('.bmp'):
		img = Image.open(args.file)
		if (args.p == 'auto'):
			palette = Pixelight.genPalette(img, args.c)
			img = Pixelight.pixelate(img, args.s, palette)
		elif (args.p == 'auto2'):
			palette = Pixelight.genPalette2(img, args.c)
			img = Pixelight.pixelate(img, args.s, palette)
		elif (args.p == 'default'):
			img = Pixelight.pixelate(img, args.s, None)
		else:
			img = Pixelight.pixelate(img, args.s, Pixelight.PALETTES[args.p])
		img.save(args.o + ".png" if args.o == "output" else args.o)

	# Video file
	elif args.file.endswith('.mp4') or args.file.endswith('.avi') or args.file.endswith('.mov') or args.file.endswith('.gif'):
		print("Cleaning the workspace.")
		resetCache()
		print("Extracting frames.")
		extractFrames(args.file)

		sample_img = Image.open("frames/" + os.listdir("frames/")[0])
		file_count = len(os.listdir("frames/"))
		rendering_prog = 1

		palette = None
		if (args.p == 'auto'):
			palette = Pixelight.genPalette(sample_img, args.c)
		elif (args.p == 'auto2'):
			palette = Pixelight.genPalette2(sample_img, args.c)
		elif (args.p == 'default'):
			palette = None
		else:
			palette = Pixelight.PALETTES[args.p]

		for file in os.listdir("frames/"):
			print(f"Rendering... ({rendering_prog} out of {file_count} done)")
			img = Image.open("frames/" + file)
			img = Pixelight.pixelate(img, args.s, palette)
			img.save("render/" + file)
			rendering_prog += 1

		print("Packaging the output.")
		compressFrames(args.f, args.o + ".mp4" if args.o == "output" else args.o)
		print("Done.")

	# Unknown file
	else:
		raise Exception("Error: Could not recognize the file format.")

else:
	raise Exception("Error: Could not find or access the file.")

# if __name__ == '__main__':
# 	img = Image.open("city.jfif").convert('RGBA')
# 	img = pixelate(img, 0.08)
# 	img.save("output.png")
	# resetCache()
	# extractFrames("boy.mp4")
	# palette = None
	# for file in os.listdir("frames/"):
		# img = Image.open("frames/" + file).convert('RGBA')
		# if palette == None:
			# genPalette(pixelate(img, 0.1), 10)
		# img = pixelate(img, 0.1, palette)
		# img.save("render/" + file)
	# compressFrames()