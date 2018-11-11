'''
Created on 31 oct. 2018

@author: apavond
'''

from bs4 import BeautifulSoup
import requests

#FormData con idcircuito por defecto , en nuestro caso la temporada 2018
def obtenerCarreras (formData={'idcircuito':'52CC7BE8-3D55-4E07-A8A1-5F3C71B446C9'}, url = 'https://imd.sevilla.org/app/carreras/cargar_carreras.php'):
    #Creación de la llamada para obtener el HTML
    headers={}
    headers['Content-Type']='application/x-www-form-urlencoded'
    headers['Origin']='https://imd.sevilla.org'
    response=requests.post(url, data = formData, headers = headers)
    soup=BeautifulSoup(response.text,'html.parser')
    #Busca de los identificadores de las carreras
    listado=soup.findAll('a', alt='Consulta de Clasificaciones')
    nombresCarreras=[]
    for element in listado:
        href=element.get('href')
        hrefSplit=href.split('=')
        nombresCarreras.append(hrefSplit[1])
    return nombresCarreras