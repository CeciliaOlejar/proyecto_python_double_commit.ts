import requests

def obtener_ubicacion():
    respuesta = requests.get("https://solid-geolocation.vercel.app/location")
    data = respuesta.json()
    ciudad = data["city"]["name"]
    pais = data["country"]["name"]
    return ciudad, pais