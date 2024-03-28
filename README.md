# Translate any conversation.

## Objetivo

Crear un traductor de voz que recibe video o audio y retorna el video con voz en el lenguaje requerido.

## Pasos

dado un grupo de archivos de video,  
 0. leer en lista todos los archivos y para cada uno: {

1.  Extraer audio del video.
2.  Limpiar el audio: ruido.
3.  Leer el audio y retornar un texto. Speech To Text.
4.  Traducir el texto al idioma requerido.
5.  Retornar un audio leyendo el texto traducido. Text to Speech.
6.  Ensamblar video y nuevo audio.
7.  Returnar video traducido y texto traducido.
    }
