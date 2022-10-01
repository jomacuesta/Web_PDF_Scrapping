# -*- coding: utf-8 -*-

##--------------------------Librerias----------------------------------------------

import requests as req
from bs4 import BeautifulSoup
import re
from xlwt import Workbook
import pandas as pd
import time
import sys
import ssl


##------------------------Environment---------------------------------------------


ssl._create_default_https_context = ssl._create_unverified_context
import warnings
warnings.filterwarnings("ignore")


##---------------------------------------------------------------------------------

class Web:
    
    """Esta clase permite crear conexion con Web, es necesario pasar un String como Input"""
    
    
    def __init__(self, path):
        
        if type(path) is not str:
            
            print("ERROR - INPUT ---> La clase Web necesita una ruta URL con formato String")

        else:
            self.url = path
            self.page = req.get(self.url,verify=False)
            self.status = self.page.status_code
            self.available = self.isAvailable()
            time.sleep(0.1) #Damos un margen por si realizamos varias construcciones seguidas

            
    def isAvailable(self):
        
        if self.status in range(200,300):
            return 'OK'
        else:
            return 'KO'
        
    def getURL(self):
        """ Esta funcion devolvera la URL que está empleando """
        
        print("La URL actual es : " + self.url)
        
        return self.url
    
    def setURL(self, postText):
        """ Esta funcion modificara la URL, con un String que se entregue """
            
        self.url = self.url + postText
        
    def getHTMLWeb(self):
        """ Esta función devolvera el codigo HTML de la pagina web """
        
        if self.status == 200 or self.status == 201:
            soup = BeautifulSoup(self.page.content, 'html.parser')
            
        else:
            print("ERROR - WEB NOT FOUND ---> No es posible acceder a la web, respuesta : {}".format(self.status))
            
        return soup.prettify()
        

        
##--------------------------------------------------------------------------------
            
class WebScrapping_Regex(Web):  
    
    """Esta clase permite extraer informacion a traves de patrones establecidos como parametros"""

    segmentos = None

    def __init__(self, web):
        
        if type(web) is not  Web:
            
            print("ERROR - INPUT ---> La clase RegexHTML necesita una Web como input")

        else:
            self.html = web.getHTMLWeb()
            self.segmentos = None
            self.url = web.url
            
  
            
    def set_HTML_For_Regex(self):
        """Esta funcion eliminara espacios en blanco y convertira a minusculas, facilitando la aplicacion de regex"""
        
        self.html = self.html.replace(' ','').lower()
            
    def splitHTML(self, pattern):
        """ Esta función generara los posibles segmentos del codigo html de la web inicial """
        
        self.segmentos = self.html.split(pattern)

        #return self.segmentos
    
    def getDict_nextPage(self,pattern_key, pattern_value):
        """ Esta funcion es necesaria cuando necesitamos progresar en la web "clicks", hacia páginas mas "profundas" para extraer la informacion """
        
        segs = self.segmentos
        dict_page = {}
        check_key = pattern_key.split('(.*)')[0]
        check_value = pattern_value.split('(.*)')[0]
        print(check_key)
        contador = 0
        
        for seg in segs:
            
            if check_key in seg and check_value in seg:
                key = self.extractInfo(pattern_key, seg)
                value = self.extractInfo(pattern_value, seg)
                dict_page[key] = value
                
            else:
                print("El segmento {} no posee la estructura esperada".format(contador))
            
            contador += 1
            
            
        return dict_page
            
    def extractInfo(self,pattern,segmento):
        """ Esta funcion extrae mediante patterns con formato : ""textodeejemplo(.*)"" donde la parte variable es la info que queremos extraer"""
        regex = re.compile(pattern)
        lista_match = regex.findall(segmento)
        return lista_match[0]
    
    def getTable(self,indice_tabla):#En este ejemplo será 2
        
        dfs = pd.read_html(self.url)
        df = dfs[indice_tabla]
        
        return df
    
##---------------------------------------------------------------------------------    


if __name__ == "__main__":
    
    web = Web('https://www.marca.com/')
    html = web.getHTMLWeb()
