"""
ALARMA VISUAL Con Raspberry Pi, SimpleCV y Dropbox

El programa se activa cada cierto tiempo fijo (INTERVALO_MENOR_ACTIVACION_SENSOR) toma una foto
y mira si hay movimiento en ella comparandola con las anteriores segun el algoritmo running segmentation 
de simpleCV, si detecta movimiento lo guarda en la carpeta alertas.
Por otra parte, para ver como van las cosas en general, el programa va guardando imagenes en la carpeta fotos 
en un intervalo de tiempo mayor (INTERVALO_MAYOR_ACTIVACION_SENSOR).

Ademas el programa llama a un cliente dropbox que se encarga de ir subiendo las fotos de estas dos carpetas a la web.

"""

import os
import time
from threading import Timer
import datetime
import time
import utilidades as camara
from SimpleCV import Image , Display, DrawingLayer, Color
import numpy as np
import  xmpp
from clienteDropbox import ClienteDropbox
from SimpleCV import Image , Display, Color, RunningSegmentation
import utilidades as util


# Constantes Camara

brillo=50
resolucion=(640,480)
modoExposicion='auto'
filename='temp.jpg'

INTERVALO_MENOR_ACTIVACION_SENSOR = 5 #segundos
INTERVALO_MAYOR_ACTIVACION_SENSOR = 1 #minuto

# Constantes Dropbox
RUTA_BASE_LOCAL = "/home/pi/Desktop/Alarma/Fotos"
RUTA_BASE_REMOTA = "/Guhorus/Alarma/Fotos"
RUTA_BASE_LOCAL_ALERTAS = "/home/pi/Desktop/Alarma/Fotos/Alertas"
COPIA_LOCAL_INFO_LOCAL = "/home/pi/Desktop/Alarma/copiaLocalInfoLocal.json"
COPIA_LOCAL_INFO_REMOTA = "/home/pi/Desktop/Alarma/copiaLocalInfoRemota.json"

clienteDropbox = ClienteDropbox(RUTA_BASE_LOCAL= "/home/pi/Desktop/Alarma/Fotos",
						RUTA_BASE_REMOTA = "/Guhorus/Alarma/Fotos")

# Codigo de la camara
periodo = datetime.timedelta(minutes=INTERVALO_MAYOR_ACTIVACION_SENSOR)
proximo = datetime.datetime.now() + periodo

# Algoritmo de deteccion del movimiento
rs = RunningSegmentation(alpha=0.75)

def mandaMensaje(mensaje, destinatarios):
	""" Manda mensaje al google Talk """
	jid = xmpp.protocol.JID('guhorus@gmail.com')
	cl=xmpp.Client(jid.getDomain(),debug=[])
	cl.connect(server=('talk.google.com', 5223))
	cl.auth(jid.getNode(),'viendolarealidad')

	for destinatario in destinatarios:
		cl.send(xmpp.protocol.Message(destinatario,mensaje, typ='chat'))
		
				
def activaCamara():
	""" Se activa la camara para detectar movimiento 
	utilizando el algormitmo running segmentation de SimpleCV"""
	global proximo
	screenLength = resolucion[0] 
	min_blob_size = screenLength * 0.15
	max_blob_size = screenLength * 0.75
	ahora = datetime.datetime.now()
	
	img = util.tomaFoto(filename,brillo,resolucion,modoExposicion)
	rs.addImage(img)
	diffImg = rs.getSegmentedImage(False)
	
	if diffImg is not None:
		
		blobs = diffImg.dilate(3).findBlobs()
		
		if blobs is not None   :
			print screenLength, min_blob_size, blobs[-1].length(),  max_blob_size	
			
			if blobs[-1].length() > min_blob_size and blobs[-1].length() < max_blob_size :
				print "El sensor ha detectado algo relevante"
				mensaje = 'Alerta ' + str(ahora) + ".jpg"
				
				imagen = Image (filename)
				
				os.chdir(RUTA_BASE_LOCAL_ALERTAS)
				blobs.image = imagen
				blobs[-1].draw(width=5, color=Color.GREEN)
				imagen.drawText(str(ahora), x= 20, y =10, fontsize=25)
				imagen.save(str(ahora)+'.jpg')
				os.chdir(RUTA_BASE_LOCAL)
				
				destinatarios = ['guadalinfopulpi@gmail.com', 'apussapus@gmail.com'] 
				mensaje = 'Alerta de la alarma, visita https://www.dropbox.com para ver las fotos'
				mandaMensaje(mensaje, destinatarios)

	# ---------------------------------------------
	# Foto a intervalos regulares
	# ---------------------------------------------
	if ahora > proximo :
		print "tomada foto de cada hora"
		camara.tomaFoto(str(ahora) + ".jpg", brillo=50,resolucion=(640,480),preview=False,modoExposicion='auto')
		proximo = datetime.datetime.now() + periodo
	

		
class Vigila:
	""" Esta clase se encarga de la activacion periodica de la camara 
		y de la subida  de las imagenes a Dropbox"""
	def __init__(self, cadaCuantoTiempo):
		self.cadaCuantoTiempo = cadaCuantoTiempo # Son segundos
		self.last_updated = None
		self.update()
		
	def update(self):
		activaCamara()
		print "Vigilando directorios locales ..."
		clienteDropbox.vigilaArbol(donde = 'local')
		self.last_updated = datetime.datetime.now()
		self.schedule()
		
	def schedule(self):
		self.timer = Timer(self.cadaCuantoTiempo, self.update)
		#self.timer.setDaemon(True)
		self.timer.start()
		
                          
if __name__ == "__main__":
	
	
	vigilancia = Vigila(INTERVALO_MENOR_ACTIVACION_SENSOR)
	
	
	
		



