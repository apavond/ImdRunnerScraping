'''
Created on 26 oct. 2018

@author: apavond
'''

import os
import requests
import csv
from bs4 import BeautifulSoup
from imd.nombreCarreras import obtenerCarreras


def consultaClasificacion(formData, listaCorredores, url = 'https://imd.sevilla.org/app/carreras/clasificaciones_carrera.php'):
    #Creamos la llamada
    headers={}
    headers['Content-Type']='application/x-www-form-urlencoded'
    headers['Origin']='https://imd.sevilla.org'
    
    response=requests.post(url, data = formData, headers = headers)
    soup=BeautifulSoup(response.text, 'html.parser')
    nombreCarrera=soup.find('h2').find(text=True)
    #Busqueda de la clasificacion
    listado=soup.find('table')
    #obtenemos los registros
    listResponse=listado.findAll('tr')
    
    esCabecera=True
    for corredor in listResponse:
        #La primera vez obtenemos la cabecera por la etiqueta th
        if(esCabecera):
            camposCabecera=corredor.findAll('th')
            cabecera=[camposCabecera[0].find(text=True),camposCabecera[1].find(text=True),camposCabecera[2].find(text=True),camposCabecera[3].find(text=True),camposCabecera[4].find(text=True),camposCabecera[5].find(text=True),camposCabecera[6].find(text=True),camposCabecera[7].find(text=True)]
            listaCorredores.append(cabecera)
            esCabecera=False
        else:
            #Posteriormente obtenemos los registros de los corredores
            camposCorredor=corredor.findAll('td')
            if len(camposCorredor)==8:
                corredorAdd=[camposCorredor[0].find(text=True),camposCorredor[1].find(text=True),camposCorredor[2].find(text=True),camposCorredor[3].find(text=True),camposCorredor[4].find(text=True),camposCorredor[5].find(text=True),camposCorredor[6].find(text=True),camposCorredor[7].find(text=True)]
                listaCorredores.append(corredorAdd)
    return nombreCarrera

def generacionCSV(nombresCarreras, tipoClasificacion='general'):
    #generacion de la llamada
    formData={}
    
    formData['id']=tipoClasificacion
    
    #Vamos a recorrer las carreras
    for carrera in nombresCarreras:
        response=[]
        formData['idcarrera']=carrera
        
        nombreArchivo=consultaClasificacion(formData, response)+'.csv'
        
        #Proceso de escribir el CSV en nuestro ordenador
        currentDir = os.path.dirname(__file__)
        filePath = os.path.join(currentDir, nombreArchivo)

        with open(filePath, 'w+', newline='') as csvFile:
            writer = csv.writer(csvFile)
            for corredor in response:
                writer.writerow(corredor)
    return

def obtencionImagen(url='https://imd.sevilla.org/programas-deportivos/carreras-populares-sevilla10'):
    #Proceso de obtener la imagen
    response = requests.get(url, None)
    soup=BeautifulSoup(response.text, 'html.parser')
    imagenes=soup.findAll('img', alt='Carreras_Populares_2018_OK')
    href=imagenes[0].get('src')
    
    nombreArchivo=href.split('/')[len(href.split('/'))-1]
    
    #Proceso de escribir nuestra imagen en nuestro ordenador
    currentDir=os.path.dirname(__file__)
    ruta=os.path.join(currentDir,nombreArchivo)
    salida = open(ruta,'wb')
    for element in requests.get(href, stream = True):
        salida.write(element)
    salida.close()
    
    return

def ejercicio():
    #Generamos la imagen
    obtencionImagen()
    #Generamos los CSV de las carreras
    generacionCSV(obtenerCarreras())