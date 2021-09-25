from PIL import Image
import math
import numpy as np
import scipy
import scipy.misc
import scipy.cluster

class Pixelight:
	
	'''
		Palettes
	'''
	PALETTES = {
		'colorful': [
			(140, 143, 174, 255),
			(88, 69, 99, 255),
			(62, 33, 55, 255),
			(154, 99, 72, 255),
			(215, 155, 125, 255),
			(245, 237, 186, 255),
			(192, 199, 65, 255),
			(100, 125, 52, 255),
			(228, 148, 58, 255),
			(157, 48, 59, 255),
			(210, 100, 113, 255),
			(112, 55, 127, 255),
			(126, 196, 193, 255),
			(52, 133, 157, 255),
			(23, 67, 75, 255),
			(31, 14, 28, 255)
		],
		'grey': [
			(255, 255, 255, 255),
			(229, 228, 219, 255),
			(206, 205, 197, 255),
			(183, 182, 175, 255),
			(160, 160, 153, 255),
			(137, 137, 131, 255),
			(115, 114, 110, 255),
			(92, 91, 88, 255),
			(69, 68, 66, 255),
			(46, 46, 44, 255),
			(23, 23, 22, 255),
			(0, 0, 0, 255)
		]
	}
		
	'''
		Compute the similarity between colors
		source_color = [int, int, int]
		compare_color = [int, int, int]
	'''
	
	@staticmethod
	def getColorSimilarity(source_color, compare_color):
		return math.sqrt(pow(source_color[0] - compare_color[0], 2) + pow(source_color[1] - compare_color[1], 2) + pow(source_color[2] - compare_color[2], 2))
		
	
	'''
		Automatically generate a color palette from an image
	'''
	
	@staticmethod
	def genPalette(img, size):
		paletted = img.convert('P', palette=Image.ADAPTIVE, colors=size)
		
		palette = paletted.getpalette()
		color_counts = sorted(paletted.getcolors(), reverse=True)
		colors = []
		
		for i in range(size if len(color_counts) >= size else len(color_counts)):
			palette_index = color_counts[i][1]
			dominant_color = palette[palette_index*3:palette_index*3+3]
			colors.append(tuple(dominant_color))
			
		return colors

	
	'''
		Automatically generate a color palette from an image
	'''
	
	@staticmethod
	def genPalette2(img, size):
		
		ar = np.asarray(img)
		shape = ar.shape
		ar = ar.reshape(np.product(shape[:2]), shape[2]).astype(float)

		codes, dist = scipy.cluster.vq.kmeans(ar, size+1)
		vecs, dist = scipy.cluster.vq.vq(ar, codes)
		counts, bins = np.histogram(vecs, len(codes))

		most_frequent = np.argpartition(-counts, kth=size)[:size]
		colors = []
		
		for i in most_frequent:
			r = int(codes[i][0])
			g = int(codes[i][1])
			b = int(codes[i][2])
			colors.append((r, g, b, 255))
			
		return colors
	

	'''
		From a palette, determine the closest color to the source color
		source_color = [int, int, int]
	'''
	
	@staticmethod
	def simplifyColor(source_color, palette):
		best_color = (0, 0, 0)
		best_score = math.inf
		
		for palette_color in palette:

			score = Pixelight.getColorSimilarity(source_color, palette_color)
			if (score <= best_score):
				best_score = score
				best_color = palette_color
		
		return best_color
		
	
	'''
		Apply color palette to an image
	'''

	@staticmethod
	def applyPalette(image, palette):
		width, height = image.size
		
		for x in range(0, width):
			for y in range(0, height):
				r, g, b, a = image.getpixel((x, y))
				
				if (a == 0):
					image.putpixel((x, y), (0, 0, 0, 0))
				else:
					new_color = Pixelight.simplifyColor((r, g, b, a), palette)
					image.putpixel((x,y), new_color)
				
		return image
	
		
	'''
	Resize image and apply color palette
	'''
	
	@staticmethod
	def pixelate(image, factor, palette = PALETTES['colorful']):
		width, height = image.size
		
		if factor < 1: raise Exception("Invalid pixelation factor. A mimimum value of 1 is required")
		
		resizeFactor = 1 / factor
		
		# Convert to RGBA color format
		image = image.convert('RGBA')
		
		# Create a pixelated version of the image
		pixelated = image.resize((int(resizeFactor * width),int(resizeFactor * height)), Image.NEAREST)
		
		if (palette == None):
			# Pixelate with no palettes
			colored = pixelated.resize((width, height), Image.NEAREST)
			return colored
		else:
			# Pixelate with a palette
			colored = Pixelight.applyPalette(pixelated, palette).resize((width, height), Image.NEAREST)
			return colored