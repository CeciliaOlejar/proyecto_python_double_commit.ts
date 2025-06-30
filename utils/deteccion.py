def detectar_rol(rol: int | str):
    if rol == 1:
        return "admin"
    elif rol == 2:
        return "Usuario"
    else:
        return "No asignado"