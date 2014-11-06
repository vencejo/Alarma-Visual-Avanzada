from SimpleCV import Image , Display, Color, ColorCurve
from SimpleCV.Shell import plot
import time
import os
import picamera

def pausa():
	while True:
		print ""
		tecla = raw_input("Pulse cualquier tecla para continuar ")
		if tecla or tecla == "\n":
			break
			
def tomaFoto(filename, brillo=50,resolucion=(1024,768),preview=None,modoExposicion='auto',altaVelocidad = False):
	""" Toma una foto con los ajustes que se le pasan como parametros ,
	la guarda en el archivo filename y devuelve un objeto Image de la foto """
	print "capturing image"
	

	with picamera.PiCamera() as picam:
		
		#if preview is not None:
			#start = time.time()
			#picam.start_preview()
			#time.sleep(1)
				
		picam.resolution = resolucion
		picam.brightness = brillo
		picam.exposure_mode = modoExposicion
		picam.rotation = 180
		if altaVelocidad:
			picam.framerate = 30
			picam.capture(filename, use_video_port = True)
		else:
			picam.capture(filename)
		
		#if preview  is not None:
			#picam.stop_preview()
			#end = time.time()
			#print "captured image in " + str(end-start) + " seconds"
			
	return Image(filename)

def ajusteFoto(filename,brillo=50,resolucion=(1024,768),modoExposicion='auto'):
	""" Va tomando fotos en un proceso de ensayo y error supervisado por el 
	usuario , hasta que se toma la adecuada y el metodo 
	devuelve el objeto imagen """
	
	disp = Display(resolucion)
	
	try:
		while not disp.isDone():
			
				img = tomaFoto(filename,brillo,resolucion,modoExposicion,altaVelocidad=False)
				img.save(disp)
	except:
		pass
		
	return img
	
def eliminaReflejos(img):
	# El canal del reflejo que tengo que disminuir es el L , 
	# de la luminosidad
	hCurve = ColorCurve([[0,0],[64,64],[128,128],[256,256]])
	lCurve = ColorCurve([[0,0],[64,30],[128,30],[256,20]])
	sCurve = ColorCurve([[0,0],[64,64],[128,128],[256,256]])

	coloredImg = img.applyHLSCurve(hCurve, lCurve, sCurve)
	erodedImg = coloredImg.erode()

	#histogram2 = erodedImg.histogram(256) 
	#plot(histogram2)	

	return erodedImg

if __name__ == "__main__":
	img = ajusteFoto('foto1.jpg',resolucion=(1024,768))
	img.live()
