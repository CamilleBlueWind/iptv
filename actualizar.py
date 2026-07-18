import urllib.request
import re

def obtener_link_dailymotion():
    try:
        # 1. Entramos a la web de Color Visión
        url_canal = "https://www.colorvision.com.do/"
        req = urllib.request.Request(url_canal, headers={'User-Agent': 'Mozilla/5.0'})
        html = urllib.request.urlopen(req).read().decode('utf-8')
        
        # 2. Buscamos el ID del video en vivo de Dailymotion en el código de la página
        match = re.search(r'dailymotion\.com/embed/video/([a-zA-Z0-9]+)', html)
        if match:
            video_id = match.group(1)
            # Retornamos la URL con el formato m3u8 que los reproductores necesitan
            return f"https://www.dailymotion.com/cdn/live/video/{video_id}.m3u8"
    except Exception as e:
        print(f"Error al extraer el enlace: {e}")
    return None

def actualizar_lista():
    nuevo_link = obtener_link_dailymotion()
    if not nuevo_link:
        print("No se pudo obtener el nuevo enlace de Color Visión.")
        return

    # Leer la lista actual
    with open("Canales RD.m3u", "r", encoding="utf-8") as f:
        lineas = f.readlines()

    # Buscar la línea de Color Vision y reemplazar la siguiente
    for i, linea in enumerate(lineas):
        if 'tvg-id="ColorVision.do"' in linea:
            # Reemplazamos la línea de abajo con el enlace dinámico fresco
            lineas[i+1] = nuevo_link + "\n"
            break

    # Guardar los cambios en el archivo
    with open("Canales RD.m3u", "w", encoding="utf-8") as f:
        f.writelines(lineas)
    print("¡Lista M3U actualizada con éxito con el token del día!")

if __name__ == "__main__":
    actualizar_lista()
