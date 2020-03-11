import pytesseract
import PIL
import numpy as np
import cv2
from PIL import Image
import tempfile
import logging

IMAGE_SIZE = 1800
BINARY_THREHOLD = 180

size = None
#Funcion que aplica el OCR a la imagen en escala de grises
def ocr_function(imagen,i):
    text = pytesseract.image_to_string(imagen)
    #print(type(text))
    #print(text)
    text_file = open( "resultados/" + i + ".txt", "w")
    text_file.write(text)
    text_file.close()
    return text 

#Convertir imagen RGB a escala de grises 1er metodo
def gray_scale(imagen):
    row,col,canal = imagen.shape
    values_array = []
    print(row,col,canal)
    for i in range(row):
        for j in range(col):
            value = (imagen[i,j,0] * 0.07 + imagen[i,j,1] * 0.72 + imagen[i,j,2] * 0.21)
            values_array.append(value)
    image_gray = np.array(values_array)
    return image_gray
    #cv2.imwrite("tes2.png", image_gray.reshape(row,col))

#Convertir imagen RGB a escala de grises 2o metodo
def gray_scale_opencv(imagen, file):
    gray = cv2.cvtColor(imagen, cv2.COLOR_RGB2GRAY)
    cv2.imwrite("resultados/" + file, gray)
    #return gray



def get_size_of_scaled_image(im):
    global size
    if size is None:
        length_x, width_y = im.size
        factor = max(1, int(IMAGE_SIZE / length_x))
        size = factor * length_x, factor * width_y
    return size


def process_image_for_ocr(file_path):
    logging.info('Processing image for text Extraction')
    temp_filename = set_image_dpi(file_path)
    im_new = remove_noise_and_smooth(temp_filename)
    return im_new


def set_image_dpi(file_path):
    im = Image.open(file_path)
    # size = (1800, 1800)
    size = get_size_of_scaled_image(im)
    im_resized = im.resize(size, Image.ANTIALIAS)
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.jpg')
    temp_filename = temp_file.name
    im_resized.save(temp_filename, dpi=(300, 300))  # best for OCR
    return temp_filename


def image_smoothening(img):
    ret1, th1 = cv2.threshold(img, BINARY_THREHOLD, 255, cv2.THRESH_BINARY)
    ret2, th2 = cv2.threshold(th1, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    blur = cv2.GaussianBlur(th2, (1, 1), 0)
    ret3, th3 = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    return th3


def remove_noise_and_smooth(file_name):
    logging.info('Removing noise and smoothening image')
    img = cv2.imread(file_name, 0)
    filtered = cv2.adaptiveThreshold(img.astype(np.uint8), 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 41, 3)
    kernel = np.ones((1, 1), np.uint8)
    opening = cv2.morphologyEx(filtered, cv2.MORPH_OPEN, kernel)
    closing = cv2.morphologyEx(opening, cv2.MORPH_CLOSE, kernel)
    img = image_smoothening(img)
    or_image = cv2.bitwise_or(img, closing)
    return or_image

if __name__ == "__main__":
    print("Pre-procesamiento de imágenes")
    import os    
    files = []
    for file in os.listdir("menus"):
        if not file.startswith("."):
            files.append(file)
    
    for file in files:
        imagen  =  cv2.imread('menus/' + file)
        gray_scale_opencv(imagen,file)
        cadena = os.path.splitext(file)[0]
        text = ocr_function("resultados/"+file,cadena)
    print("Fin")

  # imagen = cv2.imread('menus/5-1.jpg')
   #imagen = reducir_tamano(imagen)
   #gray_scale_opencv(imagen)
   #Eliminar ruido
  # ocr_function("b5.png")
  # imagen = process_image_for_ocr('menus/5-1.jpg')
   #cv2.imwrite("b6.png", imagen)
  # text = ocr_function("a5.png")
   #print(type(imagen))