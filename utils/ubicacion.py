import requests

def obtener_ubicacion():
    try:
        respuesta = requests.get("https://solid-geolocation.vercel.app/location")
        if not respuesta.ok:
            raise ValueError("No se obtuvo respuesta de la api")
        data = respuesta.json()
        ciudad = data["city"]["name"] or "No disponible"
        pais = data["country"]["name"] or "No disponible"
        return ciudad, pais
    except Exception as e:
        print(f"Ocurrió un error: {e}")