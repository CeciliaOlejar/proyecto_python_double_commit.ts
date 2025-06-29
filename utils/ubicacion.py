import requests

def obtener_ubicacion():
    try:
        respuesta = requests.get("https://solid-geolocation.vercel.app/location")
        data = respuesta.json()
        ciudad = data["city"]["name"]
        pais = data["country"]["name"]
        return ciudad, pais
    except Exception as e:
        print(f"Ocurrió un error al relizar el fetch de datos {e}")