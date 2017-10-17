#!/usr/bin env python
#-*-coding:utf-8-*-

import math

'''
Thanks to superfranz's idea
	https://www.ccsinfo.com/forum/viewtopic.php?t=52861
code as follows:
	//DISPLAY[128*64] = {0};
	void OLED_pixel(long x,long y) { 
	   LONG nt; 
	   LONG pagina; 
	   LONG bit; 
	   pagina = y / 8; 
	   bit= y - (pagina * 8); 
	   nt= DISPLAY[pagina*128+x]; 
	   nt |= 1 << bit; 
	   DISPLAY[pagina*128+x] = nt; 
	} 
'''
class OLED:
	"""
	This moudle is a ssd1306 virtual device
	WIDTH: 128
	HIGHT: 64
	"""

	
	def __init__(self, wid=128, hig=64):
		self.WIDTH  = wid
		self.HEIGHT = hig

		self.BYTEMAP = [0] * ((self.WIDTH * self.HEIGHT) / 8)
		self.BITMAP = [0] * (self.WIDTH * self.HEIGHT)
		print '\nWidth:{0} Height:{1} DotMatricxSize:{2}\n'.format(self.WIDTH, self.HEIGHT, len(self.BITMAP))

	def setPixel(self, x, y, color=0):
		'''
			Draw a point on the screen
			color :
				1: Black, 0: White
		'''
		if(x >= self.WIDTH or y >= self.HEIGHT or x < 0 or y < 0): return

		dy = int(y) / 8
		# bit = y - (dy * 8)
		bitPos = int(y) % 8
		aByte = self.BYTEMAP[int(dy) * self.WIDTH + int(x)]

		if color:		
			aByte &= ~(1 << bitPos)
		else:
			aByte |= (1 << bitPos)

		self.BYTEMAP[dy * self.WIDTH + int(x)] = aByte

	def line(self, x1, y1, x2, y2, color=0):
		'''
			Draw a line
		'''
		if x2 == x1:
			startY = y1 if y1 <= y2 else y2
			endY   = y1 if y1 >= y2 else y2

			while startY <= endY:
				self.setPixel(x1, startY, color)
				startY += 1
		elif y2 == y1:
			startX = x1 if x1 <= x2 else x2
			endX   = x1 if x1 >= x2 else x2

			while startX <= endX:
				self.setPixel(startX, y1, color)
				startX += 1
		else:
			startX = x1 if x1 <= x2 else x2
			endX   = x1 if x1 >= x2 else x2

			while startX <= endX:
				leY = ((startX - x1) * (y2 - y1) / (x2 - x1)) + y1
				self.setPixel(startX, leY, color)
				startX += 1

	def rect(self, x, y, wid, hig, color=0):
		self.line(x, y, x + wid, y, color)
		self.line(x, y + hig, x + wid, y + hig, color)
		self.line(x, y, x, y + hig, color)
		self.line(x + wid, y, x + wid, y + hig, color)




	def circle(self, srcx, srcy, radius, startAngle=0.01, endAngle=2*math.pi, color=0):
		'''
			Draw a circle
		'''
		alpha = startAngle

		if radius < 2:
			self.setPixel(srcx, srcy, color)
			return

		while(alpha <= endAngle):
			x = srcx + radius * math.cos(alpha)
			y = srcy + radius * math.sin(alpha)
		
			self.setPixel(math.floor(x), math.floor(y), color)

			alpha += 0.01

	def mapping2bitmap(self):
		index = 0

		for col in range(self.HEIGHT/8):
			for row in range(self.WIDTH):
				byte = self.BYTEMAP[index]

				for bit in range(8):
					val = 0x01 & byte
					byte >>= 1

					self.BITMAP[(col*8 + bit)*self.WIDTH  + row] = val

				index += 1

	def display(self):
		self.mapping2bitmap()

		for i in range(len(self.BITMAP)):
			if(self.WIDTH > 80):
				print '\b{0}'.format(self.BITMAP[i]), 
			else:
				print '{0}'.format(self.BITMAP[i]), 
			if (i+1) % self.WIDTH == 0: print ''

	def showBytemap(self):
		index = 0

		print '\n::Byte Map of The Memory::\n'
		for col in range(self.HEIGHT/8):
			for row in range(self.WIDTH):
				print '\b{0:2x}'.format(self.BYTEMAP[index]),
				index += 1
			print ''




if __name__ == '__main__':  
	  
	old = OLED(56, 32)
	# old  = OLED()

	# old.setPixel(15, 12)
	# old.setPixel(15, 13, 1)

 	# old.setPixel(200,55)
	# old.circle(old.WIDTH/2, old.HEIGHT/2, 20)
	# old.circle(0, 0, 30)
	# old.line(5, 2, 5, 14)
	# old.line(15, 12, 30, 30)
	old.rect(5, 5, 15, 5)


	old.display()
	# old.showBytemap()



