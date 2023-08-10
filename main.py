import requests
import os
import pandas as pd
import mimetypes
from urllib.parse import urlparse, unquote

def obtener_extension(url):
    """
    Intenta obtener la extensión de la URL.
    Si no es posible, devuelve None.
    """
    try:
        # Decodificar URL para manejar URLs codificadas (%20 para espacio, etc.)
        path = unquote(urlparse(url).path)
        extension = os.path.splitext(path)[1]
        if extension:  # Si hay una extensión en la URL
            return extension
    except:
        pass
    return None

def descargar_imagen(url, ruta_guardado, nombre_archivo):
    respuesta = requests.get(url)
    
    try:
        if respuesta.status_code == 200:
            extension = obtener_extension(url) or mimetypes.guess_extension(respuesta.headers.get('content-type')) or '.jpg'
            
            ruta_completa = os.path.join(ruta_guardado, nombre_archivo + extension)
            
            carpeta_destino = os.path.dirname(ruta_completa)
            
            if not os.path.exists(carpeta_destino):
                os.makedirs(carpeta_destino)
            
            with open(ruta_completa, 'wb') as archivo:
                archivo.write(respuesta.content)
            print(f"La imagen de {url} se ha descargado exitosamente.")
        else:
            print(f"No se pudo descargar la imagen de {url}.")
    except:
        pass
    


def main():
    archivo_excel = 'productos.xlsx'
    df = pd.read_excel(archivo_excel)

    ruta_guardado = "final/"

    for valor, row in df.iterrows():
        id_producto = row['id']
        codigo = str(row['codigo'])
        url_img_1 = row["media"]
        # url_img_2 = row["img_2"]
        # print(url_img_1)
        descargar_imagen(url_img_1, ruta_guardado, codigo)

if __name__ == "__main__":
    main()
