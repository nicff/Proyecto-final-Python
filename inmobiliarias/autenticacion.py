def registro_usuario():
    usuarios = {}
    
    try:
        base_de_datos = open("basededatos.txt", "r")
        for linea in base_de_datos:
            usuario, contraseña = linea.strip().split(", ")
            usuarios[usuario] = contraseña
        base_de_datos.close()
    except FileNotFoundError:
        pass

    usuario = input("Ingrese su usuario:\n")

    while usuario in usuarios:
        usuario = input("El usuario elegido ya existe en la base de datos, elija un nuevo usuario:\n")

    contraseña = input("Ingrese su contraseña:\n")
    contraseña_confirm = input("Por seguridad, vuelva a ingresar su contraseña:\n")

    while contraseña_confirm != contraseña:
        contraseña = input("Las contraseñas no coinciden. Ingrese nuevamente su contraseña:\n")
        contraseña_confirm = input("Vuelva a ingresar su contraseña:\n")

    base_de_datos = open("basededatos.txt", "a+")
    base_de_datos.write(f"{usuario}, {contraseña}\n")
    base_de_datos.close()

    print("¡Registro exitoso!\n")

def login_usuario():
    usuarios = {}
    
    try:
        base_de_datos = open("basededatos.txt", "r")
        for linea in base_de_datos:
            usuario, contraseña = linea.strip().split(", ")
            usuarios[usuario] = contraseña
        base_de_datos.close()
    except FileNotFoundError:
        print("La base de datos está vacía.")

    intentos = 6
    while intentos > 0:
        usuario = input("Ingrese su usuario:\n")
        contraseña = input("Ingrese su contraseña:\n")

        if usuario in usuarios and usuarios[usuario] == contraseña:
            print("Inicio de sesión exitoso.")
        else:
            intentos -= 1
            if intentos > 0:
                print(f"Usuario o contraseña incorrectos. Quedan {intentos} intentos restantes.\n")
    print("\nNo quedan intentos.\n")
    

def leer_bdd():
    usuarios = {}
    
    try:
        base_de_datos = open("basededatos.txt", "r")
        for linea in base_de_datos:
            usuario, contraseña = linea.strip().split(", ")
            usuarios[usuario] = contraseña
        if len(usuarios) >= 1:
            print(f"{usuarios}\n")
        else:
            print("La base de datos está vacía.\n")
        base_de_datos.close()
    except FileNotFoundError:
        input("La base de datos está vacía.\n")

if __name__ == "__main__":
    print("¡BIENVENIDO A MI TRABAJO ENTREGABLE N° 1!\n")
    while True:
        intencion = input("- Si quiere registrarse, escriba 'R'\n- Si ya posee una cuenta, escriba 'L' para loguearse\n- Para leer la base de datos escriba 'B'\nPresione ENTER o escriba cualquier otra cosa para cerrar el programa\n")
        if intencion == "L" or intencion == "l":
            login_usuario()
        elif intencion == "R" or intencion == "r":
            registro_usuario()
        elif intencion == "B" or intencion == "b":
            leer_bdd()
        else:
            break