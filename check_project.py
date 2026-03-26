import os
import py_compile
import sys

# Ruta predeterminada donde buscar los archivos
RUTA = "/storage/emulated/0/00 Root/02 Programming/2026/Monetizar_Cliente/gpt_test"  # cámbiala según tu entorno

def obtener_ultimo_archivo(ruta):
    archivos = [
        os.path.join(ruta, f) for f in os.listdir(ruta)
        if os.path.isfile(os.path.join(ruta, f)) and f.endswith(".py")
    ]
    if not archivos:
        return None
    # Ordenar por fecha de modificación
    archivos.sort(key=lambda x: os.path.getmtime(x), reverse=True)
    return archivos[0]

def revisar_sintaxis(ruta_archivo):
    try:
        py_compile.compile(ruta_archivo, doraise=True)
        print(f"✅ El archivo '{ruta_archivo}' no tiene errores de sintaxis.")
    except py_compile.PyCompileError as e:
        print(f"❌ Error de sintaxis en '{ruta_archivo}':")
        print(e)

if __name__ == "__main__":
    archivo = obtener_ultimo_archivo(RUTA)
    if archivo:
        revisar_sintaxis(archivo)
    else:
        print("⚠️ No se encontraron archivos .py en la ruta especificada.")