"""
Author: Cristian Rosales Deloya

"""
import copy
import nltk
import string
from nltk.tokenize.casual import TweetTokenizer
from nltk.metrics.distance import edit_distance
from nltk.corpus import stopwords
import time 

stopwords =stopwords.words('spanish')

nombresVino = ["Reservado Cabernet Sauvignon",
    "Reservado Merlot", 
    "Reservado Carmenere",
    "Reservado Malbec",
    "Reservado Shiraz",
    "Reservado Rosé",
    "Reservado White Zinfandel",
    "Reservado Sauvignon Blanc",
    "Frontera Merlot",
    "Frontera Carmenere",
    "Frontera Cabernet Sauvignon",
    "Frontera Chardonnay",
    "Casillero del diablo Red Blend",
    "Casillero del diablo Cabernet Sauvignon",
    "Casillero del diablo Merlot",
    "Casillero del diablo Devil Collection Red",
    "Casillero del diablo Chardonnay",
    "Casillero del diablo Pinot Noir",
    "Casillero del diablo Carmenere",
    "Casillero del diablo Devil Collection White",
    "Casillero del diablo Malbec",
    "Marques de Casa Concha Merlot",
    "Marques de Casa Concha Carmenere",
    "Marques de Casa Concha Chardonnay",
    "Trio Merlot",
    "Trio Chardonnay",
    "Trio Cabernet Sauvignon",
    "Concha Y Toro Brut",
    "Diablo Dark Red",
    "Casillero Del Diablo Rosé",
    "Casillero Del Diablo Sauvignon Blanc",
    "Casillero Del Diablo Gran Reserva Cabernet Sauvignon",
    "Reservado Sweet Red",
    "L.A. Cetto  Cabernet Sauvignon",
    "L.A. Cetto  Merlot",
    "Condor Millaman  Carmenere",
    "L.A. Cetto - Petite Sirah",
    "La Redonda Rosado Semiseco",
    "L.A. Cetto  Blanc De Zinfandel",
    "L.A. Cetto - Fumé Blanc",
    "La Redonda - Nosotros Los Mexicanos",
    "L.A. Cetto - Invierno",
    "Domecq XA Cabernet Sauvignon",
    "L.A. Cetto - Chardonnay",
    "Orlandi - Cabernet Sauvignon - Malbec",
    "L.A. Cetto - Reserva Privada Cabernet Sauvignon",
    "Orlandi - Merlot - Cabernet Sauviginon",
    "El Cielo Eclipse - Mezcla De Tintos",
    "L.A. Cetto - Verano",
    "L.A. Cetto - Lyra",
    "L.A. Cetto - Reserva Privada Nebbiolo",
    "Sierra Blanca - Sauvignon Blanc",
    "Sierra Blanca - Tempranillo",
    "Sierra Blanca - Cabernet Sauvignon",
    "L.A. Cetto - Reserva Privada Petite Sirah",
    "Don Luis - Merlot",
    "Don Luis - Viognier",
    "Don Luis - Concordia",
    "Freixenet Viña Dolores - Brut",
    "L.A. Cetto - Espaldera",
    "Champbrulé - Brut",
    "Don Luis - Terra",
    "L.A. Cetto - Primavera",
    "Santa Digna - Carmenere",
    "Casa Madero - Cabernet Sauvignon",
    "Casa Madero - Merlot",
    "Viña Maipo Carmenere",
    "Casa Madero - Shiraz",
    "Finca Las Moras Rosado Dulce",
    "Gallo Family White Zinfandel",
    "Finca Las Moras Sauvignon Blanc",
    "Barefoot Cabernet Sauvignon",
    "Casa Madero - Chardonnay",
    "Santa Rita 120 Reserva Especial Cabernet Sauvignon",
    "Santa Rita 120 Reserva Especial Merlot",
    "Alma Mora Pinot Noir",
    "Santa Rita 120 Reserva Especial Sauvignon Blanc",
    "Trivento Malbec Reserve ",
    "Monte Xanic Chardonnay",
    "Finca Las Moras Reserva (Cabernet - Syrah)",
    "Vino Blanco André Brut California",
    "Santa Rita 120 Reserva Especial Rosé",
    "Casa Madero - Gran Reserva Cabernet Sauvignon",
    "Cousiño Macul Cabernet Sauvignon",
    "Monte Xanic Merlot",
    "Santa Elena Carmenere",
    "Las Moras Malbec",
    "Monte Xanic Syrah",
    "Sutter Home White Zinfandel",
    "Las Moras Black Label Cabernet",
    "Monte Xanic Cabernet Sauvignon",
    "Undurraga Merlot",
    "Los Haroldos Malbec",
    "Monte Xanic Calixa",
    "Palo Alto Reserva Cabernet Sauvignon",
    "Barefoot Merlot",
    "Altos Las Hormigas Malbec",
    "Yellow Tail Shiraz",
    "Barefoot White Zinfandel",
    "Beringer White Zinfandel",
    "Carnivor Cabernet Sauvignon",
    ]

def clean_string(text):
    text = ''.join([word for word in text if word not in string.punctuation])
    text = text.lower()
    text = ' '.join([word for word in text.split() if word not in stopwords])
    return text

def formar_oraciones(texto_ocr,ventana):
    ventana_real = ventana - 1
    oracion = []
    oraciones = []
    for i in range(len(texto_ocr)- ventana_real):
        oracion = []
        oracion.append(texto_ocr[i:i+ ventana])
        oraciones.append(oracion)

    return oraciones

def similitud_Levenshtein_prueba(oracion,nombreVino):
    scores = []
    l = [ item for elem in oracion for item in elem]
    for i in range(len(nombreVino)):
        for j in range(len(l)):
            distancia = edit_distance(nombreVino[i], l[j])
            score = 1 - (distancia/max(len(l[j]),len(nombreVino[i])))
            if(score > 0.8):
                scores.append(score)
    return sum(scores)/len(nombreVino)
 

def similitud_Levenshtein(oracion,nombreVino):
    scores = []
    distancias = []
    #ponderacion_palabra = 1 / len(nombreVino)
    l = [ item for elem in oracion for item in elem]
    if(len(l) == len(nombreVino)):
        for i in range(len(l)):
            #Calcular la distancia palabra a 
            #print("Compara:", l[i], " y ", nombreVino[i])
            distancia = edit_distance(l[i],nombreVino[i])
            score = 1 - (distancia/max(len(l[i]),len(nombreVino[i])))
            #score  = score * ponderacion_palabra
            scores.append(score)
            distancias.append(distancia)
       # print(sum(scores) * 100)
        return sum(scores)/len(l)
       # if(sum(scores)/len(l) > 0.8):
        #    print(nombreVino)
         #   print(l)
          #  print(sum(scores)/len(l))
           # return sum(scores)/len(l)
            #print(distancias)

def encontrarVinos(texto_ocr):
    #Lista para los datos de los vinos limpios
    clean_data = []
    #Limpiar el texto que se obtuvo del OCR (quitar stopwords, puntuación, y mayúsculas)
    lista_texto_OCR = clean_string(texto_ocr).split()
    #Limpiar todos los elementos de la lista de vinos
    for vino in nombresVino:
        clean_data.append(clean_string(vino))
    #Crear una lista para almecenar los identificadores de los vinos encontrados en la lista
    list_results = []
    for ventana in range(2,7):
        oraciones = formar_oraciones(lista_texto_OCR,ventana)
        for i in range(len(clean_data)):
            if(len(clean_data[i].split()) == ventana):
                for oracion in oraciones:
                    score = similitud_Levenshtein(oracion,clean_data[i].split())
                    if(score > 0.80):
                        list_results.append(i+1)
    return list_results


def funcion_principal():      
    #texto_ocr es el texto que obtuvo el OCR Tesseract
    texto_ocr = open("resultados/ART5.txt").read()
    #Lista para los datos de los vinos limpios
    clean_data = []
    #Limpiar el texto que se obtuvo del OCR (quitar stopwords, puntuación, y mayúsculas)
    lista_texto_OCR = clean_string(texto_ocr).split()
    #Limpiar todos los elementos de la lista de vinos
    for vino in nombresVino:
        clean_data.append(clean_string(vino))

    #print(lista_texto_OCR)
    #print(len(clean_data[0].split()))
    #lista_prueba = ["cab","cetto","reseruad","sauignon","blamc","egrr","weee","ssss","ddd","ssss"]
    dict_results = {}
    for ventana in range(2,7):
    # print("Ventana de ",ventana)
        oraciones = formar_oraciones(lista_texto_OCR,ventana)
        for i in range(len(clean_data)):
            if(len(clean_data[i].split()) == ventana):
                for oracion in oraciones:
                    score = similitud_Levenshtein(oracion,clean_data[i].split())
                    if(score > 0.80):
                        dict_results[i + 1] = clean_data[i]
                        #print(oracion)
                        #print(clean_data[i])
                        #print(score)
    #print(dict_results)     


#tiempo_inicial = time() 

#tiempo_final = time() 
#tiempo_ejecucion = tiempo_final - tiempo_inicial
#print ('El tiempo de ejecucion fue:',tiempo_ejecucion) #En segundos
#start_time = time.time()
#funcion_principal()
#print("--- %s seconds ---" % (time.time() - start_time))
#Prueba de edit distance
#s1 = ["reservado", "merlot"]
#s2 = ["reseuado", "merlott"]
#ponderacion_palabra = 1 / len(s1)
#scores = []
#print(ponderacion_palabra)
#for i in range(len(s1)):
#    distancia =  edit_distance(s1[i], s2[i])
    #print(distancia)
 #   score = 1 - (distancia/max(len(s1[i]),len(s2[i]))) ;
  #  score  = score * ponderacion_palabra
   # scores.append(score)

#print(sum(scores) * 100)








