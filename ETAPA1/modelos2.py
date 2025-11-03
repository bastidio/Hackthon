from faker import Faker
import random

def agregar_faker_equipo(arch, grupo, listaDNI, listaNombres, lenguajes, cantidad):
    fake = Faker("es_ES")

    for k in range(cantidad):
        nombre_fake = fake.name()
        dni_fake = str(random.randint(30000000, 50000000))
        while dni_fake in listaDNI:
            dni_fake = str(random.randint(30000000, 50000000))

        listaDNI.append(dni_fake)
        listaNombres.append(nombre_fake)

        niveles_posibles = ["Nulo", "Básico", "Intermedio", "Avanzado"]
        niveles = [random.choice(niveles_posibles) for _ in lenguajes]

        linea_fake = f"{grupo};{dni_fake};{nombre_fake};{niveles[0]};{niveles[1]};{niveles[2]};{niveles[3]};{niveles[4]};{niveles[5]}\n"
        arch.write(linea_fake)

        print(f"Integrante Faker #{k+1}: {nombre_fake} (DNI: {dni_fake})")
        for i, lang in enumerate(lenguajes):
            print(f"  - {lang}: {niveles[i]}")
        print()

    print(f"Se agregaron {cantidad} integrantes Faker al grupo {grupo}.\n")

def mensajeBienvenida():
    print(
        "=" * 80 + "\n" +
        "BIENVENIDO/A AL SISTEMA DE INSCRIPCIÓN DE SKILLMATCH".center(80) + "\n" +
        "=" * 80 + "\n" +
        "En este sistema vas a registrar tu participación en el proyecto.".center(80) + "\n" +
        "Los datos a solicitar serán:".center(80) + "\n" +
        "- Datos personales (nombre y DNI)".center(80) + "\n" +
        "- Selección de habilidades en distintos lenguajes".center(80) + "\n" +
        "- Breve cuestionario de validación de nivel".center(80) + "\n" +
        "- Años de experiencia en IT".center(80) + "\n" +
        "- Estado de equipo (si ya tenés o no)".center(80) + "\n\n" +
        "Con esta información se organizarán los equipos equilibradamente.".center(80) + "\n" +
        "=" * 80
    )


def validarDNI(texto,minimo,maximo):
    validar = lambda d: d == "" or (d.isdigit() and minimo <= len(d) <= maximo)
    dni = input(texto).strip()
    if not validar(dni):
        print(f"Error, ingrese un DNI con entre {minimo} y {maximo} dígitos.")
        return validarDNI(texto, minimo, maximo)
    return dni


def validarNombre(texto,minimo):
    while True:
        try:
            valor=input(texto).strip().title()
            if len(valor.replace(" ", "")) >= minimo and valor.replace(" ", "").isalpha():
                break
            else:
                raise ValueError
        except ValueError:
            print("Entrada invalida.")
    return valor


def validarNumero(texto, minimo, maximo):
    while True:
        try:
            valor = input(texto).strip()
            valorEntero = int(valor)
            if valorEntero >= minimo and valorEntero <= maximo:
                break
            else:
                raise ValueError
        except ValueError:
            print(f"Entrada inválida. Debe ser un número entero entre {minimo} y {maximo}.")
    return valorEntero


def generarArchivoUsuarios():
    try:
        arch = open("usuarios.csv", "rt")
    except IOError:
        try:
            arch = open("usuarios.csv", "wt")
        except IOError:
            print("Error al abrir el archivo de usuarios.")
        else:
            arch.write("usuario,nombre,dni,contraseña\n")
            arch.close()
    else:
        encabezado = arch.readline()
        arch.close()
        if not encabezado or "usuario,nombre,dni,contraseña" not in encabezado.strip().lower():
            try:
                arch = open("usuarios.csv", "wt")
            except IOError:
                print("Error al abrir el archivo de usuarios.")
            else:
                arch.write("usuario,nombre,dni,contraseña\n")
                arch.close()


def usuarioExistente(usuario):
    try:
        arch = open("usuarios.csv", "rt")
    except IOError:
        print("Error al abrir el archivo de usuarios.")
        return False
    else:
        encabezado = True
        usuarioExiste = False
        for linea in arch:
            if encabezado:
                encabezado = False
                continue
            partes = linea.strip("\n").split(",")
            if len(partes) != 4:
                continue
            u = partes[0].strip().lower()
            if u == usuario.strip().lower():
                usuarioExiste = True
                break
        arch.close()
        return usuarioExiste


def controlCredenciales(usuario, clave):
    try:
        arch = open("usuarios.csv", "rt")
    except IOError:
        print("Error al abrir el archivo de usuarios.")
        return False
    else:
        encabezado = True
        ok = False
        for linea in arch:
            if encabezado:
                encabezado = False
                continue
            partes = linea.strip("\n").split(",")
            if len(partes) != 4:
                continue
            u, n, d, c = [p.strip() for p in partes]
            if u.lower() == usuario.strip().lower() and c == clave:
                ok = True
                break
        arch.close()
        return ok


def registrarUsuario():
    generarArchivoUsuarios()

    while True:
        usuario = input("Ingrese un nombre de usuario: ").strip().lower()
        if not usuario or "," in usuario:
            print("Usuario inválido (no vacío, sin comas).")
            continue
        if usuarioExistente(usuario):
            print("Ese usuario ya existe. Ingrese otro.")
            continue
        break


    while True:
        try:
            clave = input("Ingrese una contraseña (mín. 6 caracteres): ").strip()
            if len(clave) >= 6:
                break
            else:
                raise ValueError
        except ValueError:
            print("La contraseña debe tener al menos 6 caracteres.")

    try:
        arch = open("usuarios.csv", "at")
    except IOError:
        print("Error al abrir el archivo de usuarios para escribir.")
    else:
        arch.write(f"{usuario},{clave}\n")
        arch.close()
        print(f"Usuario '{usuario}' registrado correctamente.")


def iniciarSesion():
    usuario = input("Usuario: ").strip().lower()
    clave = input("Contraseña: ").strip()
    if controlCredenciales(usuario, clave):
        print(f"¡Bienvenido/a, {usuario}!")
        return True
    else:
        print("Usuario o contraseña incorrectos.")
        return False


def modificarUsuario():
    usuarioActual = input("Usuario actual: ").strip().lower()
    claveActual = input("Contraseña actual: ").strip()

    if not controlCredenciales(usuarioActual, claveActual):
        print("Usuario/clave incorrectos.")
        return

    while True:
        nuevoUsuario = input("Nuevo nombre de usuario: ").strip().lower()
        if not nuevoUsuario or "," in nuevoUsuario:
            print("Usuario inválido (no vacío, sin comas).")
            continue
        if usuarioExistente(nuevoUsuario):
            print("Ese usuario ya existe. Ingrese otro.")
            continue
        break

    try:
        arch = open("usuarios.csv", "rt")
    except IOError:
        print("Error al abrir el archivo de usuarios.")
    else:
        encabezado = arch.readline()
        filas = []
        for linea in arch:
            partes = linea.rstrip("\n").split(",")
            if len(partes) != 4:
                continue
            u, n, d, c = partes
            if u.strip().lower() == usuarioActual and c.strip() == claveActual:
                filas.append(f"{nuevoUsuario},{n},{d},{c}\n")
            else:
                filas.append(linea)
        arch.close()

        try:
            arch = open("usuarios.csv", "wt")
        except IOError:
            print("Error al reescribir el archivo de usuarios.")
        else:
            arch.write("usuario,nombre,dni,contraseña\n")
            for linea in filas:
                arch.write(linea)
            arch.close()
            print("Usuario modificado correctamente.")


def modificarClave():
    usuario = input("Usuario: ").strip().lower()
    clave = input("Contraseña actual: ").strip()

    if not controlCredenciales(usuario, clave):
        print("Usuario/clave incorrectos.")
        return

    while True:
        try:
            nueva = input("Nueva contraseña (mín. 6 caracteres): ").strip()
            if len(nueva) >= 6:
                break
            else:
                raise ValueError
        except ValueError:
            print("La contraseña debe tener al menos 6 caracteres.")

    try:
        arch = open("usuarios.csv", "rt")
    except IOError:
        print("Error al abrir el archivo de usuarios.")
    else:
        encabezado = arch.readline()
        filas = []
        for linea in arch:
            partes = linea.rstrip("\n").split(",")
            if len(partes) != 4:
                continue
            u, n, d, c = partes
            if u.strip().lower() == usuario and c.strip() == clave:
                filas.append(f"{u},{n},{d},{nueva}\n")
            else:
                filas.append(linea)
        arch.close()

        try:
            arch = open("usuarios.csv", "wt")
        except IOError:
            print("Error al reescribir el archivo de usuarios.")
        else:
            arch.write("usuario,nombre,dni,contraseña\n")
            for linea in filas:
                arch.write(linea)
            arch.close()
            print("Contraseña actualizada.")


def eliminarUsuario():
    usuario = input("Usuario a eliminar: ").strip().lower()
    clave = input("Contraseña: ").strip()

    conf = input(f"¿Seguro que querés eliminar '{usuario}'? (si/no): ").strip().lower()
    if conf != "si":
        print("Operación cancelada.")
        return

    try:
        arch = open("usuarios.csv", "rt")
    except IOError:
        print("Error al abrir el archivo de usuarios.")
    else:
        encabezado = arch.readline()
        filas = []
        eliminado = False
        for linea in arch:
            partes = linea.rstrip("\n").split(",")
            if len(partes) != 4:
                continue
            u, n, d, c = partes
            if u.strip().lower() == usuario and c.strip() == clave:
                eliminado = True
            else:
                filas.append(linea)
        arch.close()

        try:
            arch = open("usuarios.csv", "wt")
        except IOError:
            print("Error al reescribir el archivo de usuarios.")
        else:
            arch.write("usuario,nombre,dni,contraseña\n")
            for linea in filas:
                arch.write(linea)
            arch.close()
            if eliminado:
                print("Usuario eliminado correctamente.")
            else:
                print("Usuario/clave incorrectos.")


def mostrarEquipos():
    try:
        arch = open("hackaton.csv", "rt")
    except IOError:
        print("Aún no existe hackaton.csv. Generá el archivo primero.")
    else:
        encabezado = True
        grupos = {}
        for linea in arch:
            if encabezado:
                encabezado = False
                continue
            partes = linea.strip().split(";")
            if len(partes) != 9:
                continue
            grupo, dni, nombre = partes[0], partes[1], partes[2]
            if grupo not in grupos:
                grupos[grupo] = []
            grupos[grupo].append((dni, nombre))
        arch.close()

        if not grupos:
            print("\nNo hay equipos registrados aún.")
            return

        print("\n=== Equipos cargados ===")
        claves = list(grupos.keys())
        try:
            claves.sort(key=lambda x: int(x))
        except:
            claves.sort()

        for g in claves:
            print(f"\nGrupo {g}:")
            for dni, nombre in grupos[g]:
                print(f"  - {nombre} ({dni})")


def generaArchivo():
    try:
        arch=open("hackaton.csv","wt")
    except IOError:
        print("Error al abrir el archivo")
    else:
        arch.write("GRUPO;DNI;NOMBRE;PYTHON;JAVA;C++;JAVASCRIPT;PHP;C#\n")
        listaDNI=[]
        listaNombres=[]
        lenguajes=["Python", "Java", "C++", "JavaScript", "PHP", "C#"]
        grupo=1
        while True:
            dni=validarDNI("Ingrese su DNI (entre 7 y 8 caracteres)(Vacio para terminar): ",7,8)
            if dni=="":
                break
            if dni in listaDNI:
                print("Este DNI ya ha sido registrado. Vuelva a intentar")
                continue
            else:
                nombre=validarNombre("Ingrese su nombre y apellido: ",3)
                print (nombre)
                niveles=[]
                niveles=cargarHabilidades()
                linea=f"{grupo};{dni};{nombre};{niveles[0]};{niveles[1]};{niveles[2]};{niveles[3]};{niveles[4]};{niveles[5]}\n"
                arch.write(linea)
                listaDNI.append(dni)
                seguirMismo = input("¿Agregar otro participante a ESTE grupo? (si/no): ").strip().lower()
                while seguirMismo not in ("si", "no"):
                    agregar_faker_equipo(arch, grupo, listaDNI, listaNombres, lenguajes, 4)
                    
        arch.close()
        print("Archivo generado con exito.")


def generaDiccionario(dicc):
    try:
        arch = open("hackaton.csv", "rt")
    except IOError:
        print("Error al abrir el archivo.")
    else:
        encabezado = True
        for linea in arch:
            if encabezado:
                encabezado = False
                continue

            grupo,dni,nombre,py,java,c,js,php,cs = linea.strip().split(";")
            if grupo not in dicc:
                dicc[grupo] = {}
            if dni not in dicc[grupo]:
                dicc[grupo][dni] = {}
            dicc[grupo][dni]["python"] = py
            dicc[grupo][dni]["java"] = java
            dicc[grupo][dni]["c++"] = c
            dicc[grupo][dni]["js"] = js
            dicc[grupo][dni]["php"] = php
            dicc[grupo][dni]["c#"] = cs
        arch.close()
        return dicc


def cargarHabilidades():

    lenguajes=["Python", "Java", "C++", "JavaScript", "PHP", "C#"]

    niveles = ["Nulo"] * len(lenguajes)
    respuestasCorrectas = [0] * len(lenguajes)

    print("\nLenguajes para evaluar:")
    for i in range(len(lenguajes)):
        print(f"{i+1}. {lenguajes[i]}")

    seleccion = validarNumero("¿En cuántos de estos lenguajes tenés conocimiento? (1-6): ", 1, 6)

    preguntas = [
        ["(Python) ¿Qué imprime print(len([1,2,3]))?\nA) 2\nB) 3\nC) 4",
         "(Python) ¿Qué palabra clave define una función?\nA) def\nB) fun\nC) lambda",
         "(Python) ¿Qué estructura recorre una lista?\nA) while\nB) for\nC) switch"],

        ["(Java) ¿Tipo primitivo entero?\nA) String\nB) int\nC) Integer",
         "(Java) ¿Palabra clave para herencia?\nA) implements\nB) inherits\nC) extends",
         "(Java) ¿Método de entrada estándar?\nA) System.console\nB) System.in\nC) System.input"],

        ["(C++) ¿Biblioteca de E/S básica?\nA) <stdio.h>\nB) <iostream>\nC) <string>",
         "(C++) ¿Operador de inserción en stream?\nA) <<\nB) >>\nC) <--",
         "(C++) ¿Estructura condicional?\nA) when\nB) if\nC) guard"],

        ["(JS) ¿Palabra para variable mutable?\nA) let\nB) const\nC) var",
         "(JS) ¿Tipo de dato para 'true'?\nA) string\nB) boolean\nC) number",
         "(JS) ¿Método para longitud de string?\nA) .size()\nB) .length\nC) .count()"],

        ["(PHP) ¿Variables comienzan con?\nA) $\nB) #\nC) @",
         "(PHP) ¿Concatenación de strings?\nA) +\nB) .\nC) &",
         "(PHP) ¿Impresión estándar?\nA) echo\nB) printLine\nC) out"],

        ["(C#) ¿Palabra para propiedades automáticas?\nA) prop\nB) getset\nC) get; set;",
         "(C#) ¿Método de entrada de consola?\nA) Console.In()\nB) Console.ReadLine()\nC) Console.Read()",
         "(C#) ¿Estructura de selección múltiple?\nA) match\nB) switch\nC) choose"]
    ]

    respuestasCorrectas_lista = [
        ["B", "A", "B"],
        ["B", "C", "B"],
        ["B", "A", "B"],
        ["A", "B", "B"],
        ["A", "B", "A"],
        ["C", "B", "B"]
    ]

    elegidos = []

    while seleccion != 0:
        opcion = validarNumero("\nEligí del listado anterior el lenguaje que conocés. Te haremos unas preguntas sobre el mismo para evaluar tu nivel. Seleccioná uno del 1 al 6: ", 1, 6)
        lenguajeIndice = opcion - 1
        while lenguajeIndice in elegidos:
            print("Ya elegiste ese lenguaje. Elegí otro distinto.")
            opcion = validarNumero("\nEligí del listado anterior el lenguaje que conocés. Te haremos unas preguntas sobre el mismo para evaluar tu nivel. Seleccioná uno del 1 al 6: ", 1, 6)
            lenguajeIndice = opcion - 1

        seleccion -= 1

        elegidos.append(lenguajeIndice)

        print(f"\nPreguntas sobre {lenguajes[lenguajeIndice]}:")
        aciertos = 0

        for preguntaNum in range(3):
            pregunta = preguntas[lenguajeIndice][preguntaNum]
            correcta = respuestasCorrectas_lista[lenguajeIndice][preguntaNum]
            respuesta = input(pregunta + "\nTu respuesta (A/B/C): ").replace(" ","").upper()
            while respuesta not in ["A", "B", "C"]:
                print("Opción inválida. Responda A, B o C.")
                respuesta = input("Tu respuesta (A/B/C): ").replace(" ","").upper()
            if respuesta == correcta:
                aciertos += 1

        respuestasCorrectas[lenguajeIndice] = aciertos

        if aciertos == 3:
            niveles[lenguajeIndice] = "Avanzado"
        elif aciertos == 2:
            niveles[lenguajeIndice] = "Intermedio"
        elif aciertos == 1:
            niveles[lenguajeIndice] = "Básico"
        else:
            niveles[lenguajeIndice] = "Nulo"

        print(f"Resultado de {lenguajes[lenguajeIndice]}: {aciertos}/3 - Nivel: {niveles[lenguajeIndice]}")

    print("\nTus resultados finales:")
    for i in range(len(lenguajes)):
        if niveles[i] != "Nulo":
            print(f"{lenguajes[i]}: {niveles[i]} ({respuestasCorrectas[i]}/3)")
    
    return niveles

def generaReportePorcentaje(dicc):
    try:
        arch = open("porcentaje_avanzados_python.csv", "wt")
    except IOError:
        print("Error al crear el archivo")
    else:
        arch.write(f"TOTAL INTEGRANTES;TOTAL AVANZADOS;PORCENTAJE\n")
        totalGeneral = 0
        avanzadosGeneral = 0
        for grupo, participantes in dicc.items():
            for dni, niveles in participantes.items():
                totalGeneral += 1
                if "python" in niveles:
                    if str(niveles["python"]).strip().capitalize() == "Avanzado":
                        avanzadosGeneral += 1
        porcentajeGeneral = (avanzadosGeneral / totalGeneral * 100) if totalGeneral > 0 else 0.0
        arch.write(f"{totalGeneral};{avanzadosGeneral};{porcentajeGeneral:.2f}%\n")
        arch.close()


def generaReportePromedio(dicc):
    puntaje = {"Básico": 1, "Intermedio": 2, "Avanzado": 3}
    try:
        arch = open("promedio_java.csv", "wt")
    except IOError:
        print("Error al crear el archivo")
    else:
        arch.write("PROMEDIO NIVEL JAVA\n")
        sumaTotal = 0
        contTotal = 0
        for grupo, participantes in dicc.items():
            for dni, niveles in participantes.items():
                if "java" in niveles:
                    nivel = str(niveles["java"]).strip().capitalize()
                    if nivel in puntaje:
                        sumaTotal += puntaje[nivel]
                        contTotal += 1

        if contTotal == 0:
            etiqueta = "NULO"
        else:
            promedio = sumaTotal / contTotal
            if promedio < 1.5:
                etiqueta = "BÁSICO"
            elif promedio < 2.5:
                etiqueta = "INTERMEDIO"
            else:
                etiqueta = "AVANZADO"

        arch.write(f"{etiqueta}\n")
        arch.close()


def generaReporteCantidadIntegrantes(dicc):
    try:
        arch = open("cantidad_integrantes.csv", "wt")
    except IOError:
        print("Error al crear el archivo")
    else:
        ks = list(dicc)
        maxC = minC = len(dicc[ks[0]])
        gMax = [ks[0]]
        gMin = [ks[0]]
        for i in range(1, len(ks)):
            g = ks[i]; c = len(dicc[g])
            if c > maxC: maxC, gMax = c, [g]
            elif c == maxC: gMax.append(g)
            if c < minC: minC, gMin = c, [g]
            elif c == minC: gMin.append(g)
        arch.write(f"MAX;{maxC};{'|'.join(gMax)}\n")
        arch.write(f"MIN;{minC};{'|'.join(gMin)}\n")
        arch.close()


def main():
    mensajeBienvenida()
    generarArchivoUsuarios()  # asegura usuarios.csv con encabezado

    while True:
        print("\n=== MENÚ PRINCIPAL ===")
        print("1. Registrarse")
        print("2. Iniciar sesión")
        print("3. Mostrar equipos")
        print("4. Modificar usuario o contraseña")
        print("5. Eliminar usuario")
        print("6. Cargar participantes")
        print("7. Salir")

        op = input("Elegí una opción (1-7): ").strip()
        if op == "1":
            registrarUsuario()
        elif op == "2":
            iniciarSesion()
        elif op == "3":
            mostrarEquipos()
        elif op == "4":
            print("\n1) Modificar usuario\n2) Modificar contraseña")
            sub = input("Elegí (1/2): ").strip()
            if sub == "1":
                modificarUsuario()
            elif sub == "2":
                modificarClave()
            else:
                print("Opción inválida.")
        elif op == "5":
            eliminarUsuario()
        elif op == "6":
            generaArchivo()
        elif op == "7":
            print("\n¡Gracias por usar el sistema de inscripción de SkillMatch! Éxitos en el hackathon.")
            break
        else:
            print("Opción inválida. Probá de nuevo.")


if __name__ == "__main__":

    main()
