from SimpleCV import Image , Display, Color, ColorCurve,DrawingLayer
import picamera
import utilidades as util
#import numpy as np

ALTURA_OBJETO = 85 #mm
DISTANCIA_FOCAL = 3.6 #mm
FACTOR_CONVERSION_PIXEL_A_MM = 295

img = util.tomaFoto("objeto.jpg", brillo = 55)
#img = Image("lineaDe4.jpg")
#img.live()

# El truco esta en buscar el color azul del tablero en lugar de ir directamente a por las fichas
img_tratada = img.binarize() 
#img_tratada.live()

blobGrande = img_tratada.findBlobs().sortArea()[-1]

if blobGrande:
	
	i_prima = blobGrande.length() / FACTOR_CONVERSION_PIXEL_A_MM
	d = (ALTURA_OBJETO * DISTANCIA_FOCAL / i_prima) / 10
	
	textLayer = DrawingLayer((img.width,img.height))
	textLayer.setFontSize(36)
	textLayer.text("Distancia = " + str(d) + " centimetros", (10,10), color=Color.RED)
	
	blobGrande.draw(width = 5, color = Color.RED)	
	img.addDrawingLayer(img_tratada.dl())
	img.addDrawingLayer(textLayer)

	img.show()
	util.pausa()
else:
	print "No se han encontrado Blobs"



