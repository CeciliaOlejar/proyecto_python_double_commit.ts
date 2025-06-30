import httpx

async def api_cliente():
    try:
        async with httpx.AsyncClient() as client:
            respuesta = await client.get("https://solid-geolocation.vercel.app/location")
            if not respuesta:
                raise ValueError("No se obtuvo respuesta de la api")
            data = respuesta.json()
            ciudad = data["city"]["name"] or "No disponible"
            pais = data["country"]["name"] or "No disponible"
            return ciudad, pais
    except Exception as e:
        print(f"Ocurrió un error: {e}")

async def obtener_ubicacion():
    data = await api_cliente()
    return data
