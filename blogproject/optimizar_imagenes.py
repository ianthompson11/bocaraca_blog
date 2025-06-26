from PIL import Image
import os

# Directorio base (ajustado correctamente)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

imagenes = [
    {
        "entrada": os.path.join(BASE_DIR, "staticfiles/blogapp/images/fondo.8874588f1432.png"),
        "salida": os.path.join(BASE_DIR, "staticfiles/blogapp/images/fondo_optimizado.webp")
    },
    {
        "entrada": os.path.join(BASE_DIR, "staticfiles/blogapp/images/fondo_dark2.jpg"),
        "salida": os.path.join(BASE_DIR, "staticfiles/blogapp/images/fondo_dark2_optimizado.webp")
    }
]

for imagen in imagenes:
    try:
        img = Image.open(imagen["entrada"])
        img.save(imagen["salida"], "WEBP", quality=80)

        size_mb = os.path.getsize(imagen["salida"]) / (1024 * 1024)
        print(f"✅ {imagen['salida']} optimizada ({size_mb:.2f} MB)")

    except Exception as e:
        print(f"❌ Error procesando {imagen['entrada']}: {e}")
