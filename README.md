ALARMA VISUAL AVANZADA Con Raspberry Pi, SimpleCV y Dropbox
=================================

### Resumen:


El programa se activa cada cierto tiempo fijo (INTERVALO_MENOR_ACTIVACION_SENSOR) toma una foto
y mira si hay movimiento en ella comparandola con las anteriores segun el algoritmo running segmentation 
de simpleCV, si detecta movimiento lo guarda en la carpeta alertas.


Por otra parte, para ver como van las cosas en general, el programa va guardando imagenes en la carpeta fotos 
en un intervalo de tiempo mayor (INTERVALO_MAYOR_ACTIVACION_SENSOR).


Ademas el programa llama a un cliente dropbox que se encarga de ir subiendo las fotos de estas dos carpetas a la web.


### Implementacion:

Para el cliente Dropbox utiliza [el siguiente codigo][1]

[1]: https://github.com/vencejo/Cliente-Dropbox-para-Raspberry-Pi


