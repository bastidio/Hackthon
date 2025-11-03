from faker import Faker
import random
import os

# --------------------------------------------------------------------------------
# Funciones de Validación
# --------------------------------------------------------------------------------

def validarDNI(texto, minimo, maximo, listaDNI_excluir=None):
    """
    Solicita y valida un DNI con longitud entre minimo y maximo.
    También verifica que no esté en la lista de DNI excluidos (opcional).
    """
    listaDNI_excluir = listaDNI_excluir if listaDNI_excluir is not None else []
    
    while True:
        dni = input(texto).strip()
        if dni == "":
            return dni # Permite vacío para terminar en generaArchivo
            
        if dni.isdigit() and minimo <= len(dni) <= maximo:
            if dni not in listaDNI_excluir:
                return dni
            else:
                print("Error: Este DNI ya está registrado. Ingrese uno nuevo.")
        else:
            print(f"Error: Ingrese un DNI con entre {minimo} y {maximo} dígitos, sin otros caracteres.")


def validarNombre(texto, minimo):
    """
    Solicita y valida un nombre y apellido con un mínimo de caracteres alfabéticos.
    Retorna el valor con la primera letra de cada palabra en mayúscula.
    """
    while True:
        try:
            valor = input(texto).strip().title()
            # Quitamos espacios para contar el mínimo de caracteres alfabéticos
            if len(valor.replace(" ", "")) >= minimo and valor.replace(" ", "").replace(".", "").isalpha():
                return valor
            else:
                raise ValueError
        except ValueError:
            print(f"Entrada inválida. Ingrese un nombre/apellido válido (mínimo {minimo} letras).")


def validarNumero(texto, minimo, maximo):
    """
    Solicita y valida un número entero dentro de un rango [minimo, maximo].
    """
    while True:
        try:
            valor = input(texto).strip()
            valorEntero = int(valor)
            if minimo <= valorEntero <= maximo:
                return valorEntero
            else:
                raise ValueError
        except ValueError:
            print(f"Entrada inválida. Debe ser un número entero entre {minimo} y {maximo}.")


# --------------------------------------------------------------------------------
# Funciones de Archivo y Usuario
# --------------------------------------------------------------------------------

def generarArchivoUsuarios():
    """ Asegura la existencia del archivo 'usuarios.csv' con el encabezado correcto. """
    encabezado_esperado = "usuario,nombre,dni,contraseña"
    try:
        with open("usuarios.csv", "rt") as arch:
            encabezado = arch.readline().strip().lower()
            if encabezado == encabezado_esperado:
                return
    except IOError:
        pass 
        
    try:
        with open("usuarios.csv", "wt") as arch:
            arch.write(f"{encabezado_esperado}\n")
            print("Archivo 'usuarios.csv' creado/actualizado con encabezado.")
    except IOError:
        print("Error crítico al crear el archivo 'usuarios.csv'.")


def usuarioExistente(usuario):
    """ Verifica si un nombre de usuario ya existe en 'usuarios.csv'. """
    try:
        with open("usuarios.csv", "rt") as arch:
            arch.readline() 
            for linea in arch:
                partes = linea.strip("\n").split(",")
                if len(partes) == 4 and partes[0].strip().lower() == usuario.strip().lower():
                    return True
    except IOError:
        print("Error al leer el archivo de usuarios.")
    return False


def controlCredenciales(usuario, clave):
    """ Verifica si el usuario y la clave son correctos en 'usuarios.csv'. """
    try:
        with open("usuarios.csv", "rt") as arch:
            arch.readline()
            for linea in arch:
                partes = linea.strip("\n").split(",")
                if len(partes) != 4:
                    continue
                u, n, d, c = [p.strip() for p in partes]
                if u.lower() == usuario.strip().lower() and c == clave:
                    return True, n, d
    except IOError:
        print("Error al abrir el archivo de usuarios.")
    return False, None, None


def registrarUsuario():
    """ Permite registrar un nuevo usuario, nombre, DNI y contraseña. """
    generarArchivoUsuarios()

    # 1. Validar Usuario
    while True:
        usuario = input("Ingrese un nombre de usuario: ").strip().lower()
        if not usuario or "," in usuario:
            print("Usuario inválido (no vacío, sin comas).")
            continue
        if usuarioExistente(usuario):
            print("Ese usuario ya existe. Ingrese otro.")
            continue
        break
    
    # 2. Validar Nombre y DNI
    nombre = validarNombre("Ingrese su nombre y apellido: ", 3)
    dni = validarDNI("Ingrese su DNI (entre 7 y 8 caracteres): ", 7, 8)
    
    # 3. Validar Contraseña
    while True:
        try:
            clave = input("Ingrese una contraseña (mín. 6 caracteres): ").strip()
            if len(clave) >= 6:
                break
            else:
                raise ValueError
        except ValueError:
            print("La contraseña debe tener al menos 6 caracteres.")

    # 4. Escribir en el archivo
    try:
        with open("usuarios.csv", "at") as arch:
            arch.write(f"{usuario},{nombre},{dni},{clave}\n") 
        print(f"Usuario '{usuario}' registrado correctamente.")
    except IOError:
        print("Error al abrir el archivo de usuarios para escribir.")


def iniciarSesion():
    """ Solicita credenciales e inicia sesión. """
    usuario = input("Usuario: ").strip().lower()
    clave = input("Contraseña: ").strip()
    
    ok, nombre, dni = controlCredenciales(usuario, clave)
    
    if ok:
        print(f"¡Bienvenido/a, {nombre}!")
        return True
    else:
        print("Usuario o contraseña incorrectos.")
        return False


def modificarUsuario():
    """ Permite modificar el nombre de usuario de una cuenta existente. """
    usuarioActual = input("Usuario actual: ").strip().lower()
    claveActual = input("Contraseña actual: ").strip()

    ok, _, _ = controlCredenciales(usuarioActual, claveActual)

    if not ok:
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
        with open("usuarios.csv", "rt") as arch:
            arch.readline()
            filas = []
            for linea in arch:
                partes = linea.rstrip("\n").split(",")
                if len(partes) != 4:
                    filas.append(linea)
                    continue
                u, n, d, c = partes
                if u.strip().lower() == usuarioActual and c.strip() == claveActual:
                    filas.append(f"{nuevoUsuario},{n},{d},{c}\n") 
                else:
                    filas.append(linea)
    except IOError:
        print("Error al abrir el archivo de usuarios.")
        return

    try:
        with open("usuarios.csv", "wt") as arch:
            arch.write("usuario,nombre,dni,contraseña\n")
            arch.writelines(filas)
        print("Usuario modificado correctamente.")
    except IOError:
        print("Error al reescribir el archivo de usuarios.")


def modificarClave():
    """ Permite modificar la contraseña de una cuenta existente. """
    usuario = input("Usuario: ").strip().lower()
    clave = input("Contraseña actual: ").strip()

    ok, _, _ = controlCredenciales(usuario, clave)

    if not ok:
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
        with open("usuarios.csv", "rt") as arch:
            arch.readline()
            filas = []
            for linea in arch:
                partes = linea.rstrip("\n").split(",")
                if len(partes) != 4:
                    filas.append(linea)
                    continue
                u, n, d, c = partes
                if u.strip().lower() == usuario and c.strip() == clave:
                    filas.append(f"{u},{n},{d},{nueva}\n") 
                else:
                    filas.append(linea)
    except IOError:
        print("Error al abrir el archivo de usuarios.")
        return

    try:
        with open("usuarios.csv", "wt") as arch:
            arch.write("usuario,nombre,dni,contraseña\n")
            arch.writelines(filas)
        print("Contraseña actualizada.")
    except IOError:
        print("Error al reescribir el archivo de usuarios.")


def eliminarUsuario():
    """ Permite eliminar un usuario del sistema, pidiendo confirmación. """
    usuario = input("Usuario a eliminar: ").strip().lower()
    clave = input("Contraseña: ").strip()

    ok, _, _ = controlCredenciales(usuario, clave)
    if not ok:
        print("Usuario/clave incorrectos.")
        return

    conf = input(f"¿Seguro que querés eliminar '{usuario}'? (si/no): ").strip().lower()
    if conf != "si":
        print("Operación cancelada.")
        return

    try:
        with open("usuarios.csv", "rt") as arch:
            arch.readline()
            filas = []
            eliminado = False
            for linea in arch:
                partes = linea.rstrip("\n").split(",")
                if len(partes) != 4:
                    filas.append(linea)
                    continue
                u, n, d, c = partes
                if u.strip().lower() == usuario and c.strip() == clave:
                    eliminado = True
                else:
                    filas.append(linea)
    except IOError:
        print("Error al abrir el archivo de usuarios.")
        return

    try:
        with open("usuarios.csv", "wt") as arch:
            arch.write("usuario,nombre,dni,contraseña\n")
            arch.writelines(filas)
            
        if eliminado:
            print("Usuario eliminado correctamente.")
        else:
            print("Error: No se encontró el usuario para eliminar.")
    except IOError:
        print("Error al reescribir el archivo de usuarios.")


def mostrarEquipos():
    """ Lee 'hackaton.csv' y muestra los participantes agrupados por equipo. """
    try:
        with open("hackaton.csv", "rt") as arch:
            grupos = {}
            arch.readline() 
            
            for linea in arch:
                partes = linea.strip().split(";")
                if len(partes) != 9:
                    continue
                
                grupo, dni, nombre = partes[0], partes[1], partes[2]
                
                if grupo not in grupos:
                    grupos[grupo] = []
                grupos[grupo].append((dni, nombre))
    except IOError:
        print("Aún no existe hackaton.csv. Generá el archivo primero (opción 6).")
        return

    if not grupos:
        print("\nNo hay equipos registrados aún.")
        return

    print("\n=== Equipos cargados ===")
    claves = list(grupos.keys())
    try:
        claves.sort(key=lambda x: int(x))
    except ValueError:
        claves.sort()

    for g in claves:
        print(f"\nGrupo {g} (Integrantes: {len(grupos[g])}):")
        for dni, nombre in grupos[g]:
            print(f"  - {nombre} (DNI: {dni})")


def generaDiccionario(dicc):
    """
    Lee los datos del archivo 'hackaton.csv' y los carga en un diccionario
    con la estructura: {grupo: {dni: {lenguaje: nivel, ...}, ...}, ...}
    """
    dicc.clear() 
    try:
        with open("hackaton.csv", "rt") as arch:
            encabezado = arch.readline().strip().split(";")
            lenguajes = [l.lower() for l in encabezado[3:]]
            
            for linea in arch:
                partes = linea.strip().split(";")
                if len(partes) != 9: 
                    continue
                
                grupo, dni, nombre = partes[0], partes[1], partes[2]
                niveles_raw = partes[3:]
                
                if grupo not in dicc:
                    dicc[grupo] = {}
                
                dicc[grupo][dni] = {}
                for i, nivel in enumerate(niveles_raw):
                    dicc[grupo][dni][lenguajes[i]] = nivel.strip()
                    
    except IOError:
        print("Error: No se puede leer el archivo 'hackaton.csv'.")
    except Exception as e:
        print(f"Error procesando el archivo de participantes: {e}")
        
    return dicc


def cargarHabilidades():
    """ Guía al usuario a través del cuestionario de habilidades y retorna 
    una lista con los niveles obtenidos. """
    lenguajes = ["Python", "Java", "C++", "JavaScript", "PHP", "C#"]
    niveles = ["Nulo"] * len(lenguajes)
    
    # ... (Resto de la lógica de cargarHabilidades es correcta y se mantiene)
    
    print("\nLenguajes para evaluar:")
    for i, lang in enumerate(lenguajes):
        print(f"{i+1}. {lang}")

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

    for _ in range(seleccion):
        opcion = validarNumero("\nEligí del listado anterior el lenguaje que conocés (1-6): ", 1, 6)
        lenguajeIndice = opcion - 1
        
        while lenguajeIndice in elegidos:
            print("Ya elegiste ese lenguaje. Elegí otro distinto.")
            opcion = validarNumero("Eligí del listado anterior el lenguaje que conocés (1-6): ", 1, 6)
            lenguajeIndice = opcion - 1

        elegidos.append(lenguajeIndice)

        print(f"\nPreguntas sobre {lenguajes[lenguajeIndice]}:")
        aciertos = 0

        for preguntaNum in range(3):
            pregunta = preguntas[lenguajeIndice][preguntaNum]
            correcta = respuestasCorrectas_lista[lenguajeIndice][preguntaNum]
            
            while True:
                respuesta = input(pregunta + "\nTu respuesta (A/B/C): ").replace(" ","").upper()
                if respuesta in ["A", "B", "C"]:
                    break
                print("Opción inválida. Responda A, B o C.")
                
            if respuesta == correcta:
                aciertos += 1

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
            print(f"{lenguajes[i]}: {niveles[i]}")
            
    return niveles


def agregar_faker_equipo(arch, grupo, listaDNI, listaNombres, lenguajes):
    """
    Agrega de 1 a 4 participantes de relleno (Faker) a un equipo.
    Actualiza la lista de DNI y Nombres.
    """
    fake = Faker("es_ES")
    # Genera entre 1 y 4 participantes adicionales
    faltan = random.randint(1, 4)

    print(f"\nGenerando {faltan} integrantes Faker para el Grupo {grupo}...")
    
    for k in range(faltan):
        nombre_fake = fake.name()
        # Generamos DNI que no esté en la lista de DNI ya registrados
        dni_fake = str(random.randint(30000000, 50000000))
        while dni_fake in listaDNI:
            dni_fake = str(random.randint(30000000, 50000000))

        listaDNI.append(dni_fake)
        listaNombres.append(nombre_fake)

        niveles_posibles = ["Nulo", "Básico", "Intermedio", "Avanzado"]
        # Asignamos niveles aleatorios a los 6 lenguajes
        niveles = [random.choice(niveles_posibles) for _ in lenguajes]

        # Generamos la línea para el archivo hackaton.csv
        linea_fake = f"{grupo};{dni_fake};{nombre_fake};{niveles[0]};{niveles[1]};{niveles[2]};{niveles[3]};{niveles[4]};{niveles[5]}\n"
        arch.write(linea_fake)

        print(f"Integrante Faker #{k+1}: {nombre_fake} (DNI: {dni_fake})")

    print(f"Se agregaron {faltan} integrantes Faker al grupo {grupo}.\n")


def generaArchivo():
    """ Permite al usuario inscribir participantes y equipos, generando 
    el archivo 'hackaton.csv'. """
    try:
        # Abrimos en modo append para agregar nuevos registros
        arch = open("hackaton.csv", "at") 
        # Si es un archivo nuevo, escribimos el encabezado. 
        if os.path.getsize("hackaton.csv") == 0:
             arch.write("GRUPO;DNI;NOMBRE;PYTHON;JAVA;C++;JAVASCRIPT;PHP;C#\n")
        
        listaDNI = []
        # Leemos DNI existentes para evitar duplicados
        try:
             with open("hackaton.csv", "rt") as read_arch:
                read_arch.readline() 
                for linea in read_arch:
                    if len(linea.split(";")) >= 2:
                        listaDNI.append(linea.split(";")[1].strip())
        except IOError:
             pass 
        
        listaNombres = []
        lenguajes = ["Python", "Java", "C++", "JavaScript", "PHP", "C#"]
        
        # Lógica para determinar el número de grupo
        grupo_base = 1
        if listaDNI:
            try:
                with open("hackaton.csv", "rt") as read_arch:
                    last_group = 0
                    for linea in read_arch:
                        partes = linea.split(";")
                        if len(partes) > 0 and partes[0].isdigit():
                            last_group = int(partes[0])
                    grupo_base = last_group + 1
            except:
                pass 

    except IOError:
        print("Error al abrir el archivo 'hackaton.csv'.")
        return
    else:
        grupo = grupo_base
        print(f"\nInscripción de participantes. Nuevo grupo a asignar: {grupo}")

        while True:
            # Validamos DNI contra los DNI ya registrados
            dni = validarDNI("Ingrese su DNI (7-8 dígitos) (Vacío para terminar): ", 7, 8, listaDNI_excluir=listaDNI)
            
            if dni == "":
                break
            
            nombre = validarNombre("Ingrese su nombre y apellido: ", 3).title()
            listaDNI.append(dni)
            listaNombres.append(nombre)

            niveles_lista = cargarHabilidades() 

            linea = f"{grupo};{dni};{nombre};{niveles_lista[0]};{niveles_lista[1]};{niveles_lista[2]};{niveles_lista[3]};{niveles_lista[4]};{niveles_lista[5]}\n"
            arch.write(linea)
            print(f"{nombre} agregado al grupo {grupo}.\n")
            
            # Pregunta si desea completar el equipo con Faker
            completar = input("¿Desea completar su equipo automáticamente con Faker? (si/no): ").strip().lower()
            while completar not in ("si", "no"):
                completar = input("Responda si/no: ").strip().lower()

            if completar == "si":
                # La función Faker ya se encarga de escribir en el archivo y actualizar listaDNI/listaNombres
                agregar_faker_equipo(arch, grupo, listaDNI, listaNombres, lenguajes)
            
            # Incrementamos el grupo para el próximo participante/equipo
            grupo += 1 

        arch.close()
        print("\nArchivo de participantes 'hackaton.csv' generado/actualizado con éxito.")


# --------------------------------------------------------------------------------
# Funciones de Reporte (Generan archivos CSV)
# --------------------------------------------------------------------------------

def generaReportePorcentaje(dicc):
    """
    [Reporte 1] Genera 'porcentaje_avanzados_python.csv' con el total de participantes,
    avanzados en Python, y el porcentaje.
    """
    try:
        arch = open("porcentaje_avanzados_python.csv", "wt")
    except IOError:
        print("Error al crear el archivo porcentaje_avanzados_python.csv")
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
        print("  [✓] Reporte 'porcentaje_avanzados_python.csv' generado.")


def generaReportePromedio(dicc):
    """
    [Reporte 2] Genera 'promedio_java.csv' con una etiqueta (BÁSICO, INTERMEDIO, AVANZADO)
    basada en el promedio del nivel de Java (1=Básico, 2=Intermedio, 3=Avanzado).
    """
    puntaje = {"Básico": 1, "Intermedio": 2, "Avanzado": 3} 
    try:
        arch = open("promedio_java.csv", "wt")
    except IOError:
        print("Error al crear el archivo promedio_java.csv")
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
        print("  [✓] Reporte 'promedio_java.csv' generado.")


def generaReporteCantidadIntegrantes(dicc):
    """
    [Reporte 3] Genera 'cantidad_integrantes.csv' con el grupo/s con la máxima y mínima
    cantidad de integrantes.
    """
    try:
        arch = open("cantidad_integrantes.csv", "wt")
    except IOError:
        print("Error al crear el archivo cantidad_integrantes.csv")
    else:
        if not dicc:
            arch.write(f"MAX;0;N/A\n")
            arch.write(f"MIN;0;N/A\n")
            arch.close()
            print("  [✓] Reporte 'cantidad_integrantes.csv' generado (Diccionario vacío).")
            return
            
        ks = list(dicc.keys())
        
        maxC = minC = len(dicc[ks[0]])
        gMax = [ks[0]]
        gMin = [ks[0]]
        
        for i in range(1, len(ks)):
            g = ks[i]
            c = len(dicc[g])
            
            if c > maxC:
                maxC, gMax = c, [g]
            elif c == maxC:
                gMax.append(g)
                
            if c < minC:
                minC, gMin = c, [g]
            elif c == minC:
                gMin.append(g)
                
        arch.write(f"MAX;{maxC};{'|'.join(gMax)}\n")
        arch.write(f"MIN;{minC};{'|'.join(gMin)}\n")
        arch.close()
        print("  [✓] Reporte 'cantidad_integrantes.csv' generado.")


# --------------------------------------------------------------------------------
# Función Principal
# --------------------------------------------------------------------------------

def mensajeBienvenida():
    """ Muestra un mensaje de bienvenida formateado. """
    print(
        "=" * 80 + "\n" +
        "BIENVENIDO/A AL SISTEMA DE INSCRIPCIÓN DE SKILLMATCH".center(80) + "\n" +
        "=" * 80 + "\n" +
        "En este sistema vas a registrar tu participación en el proyecto.".center(80) + "\n" +
        "Con esta información se organizarán los equipos equilibradamente.".center(80) + "\n" +
        "=" * 80
    )


def main():
    mensajeBienvenida()
    diccionario = {}
    generarArchivoUsuarios() 
    
    # Intentamos cargar el diccionario al inicio
    diccionario = generaDiccionario(diccionario)

    while True:
        print("\n=== MENÚ PRINCIPAL ===")
        print("1. Registrarse")
        print("2. Iniciar sesión")
        print("3. Mostrar equipos")
        print("4. Modificar usuario o contraseña")
        print("5. Eliminar usuario")
        print("6. Cargar participantes (Genera/Actualiza reportes)")
        print("7. Salir")

        op = input("Elegí una opción (1-7): ").strip()
        
        # Ejecución de opciones de menú
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
            # 1. El usuario carga/actualiza hackaton.csv
            generaArchivo()
            # 2. Leemos hackaton.csv y populamos el diccionario para los reportes
            diccionario = generaDiccionario({})
        
        # Generación de reportes: se ejecuta al final de cada iteración si hay datos
        if diccionario:
            print("\n--- Generando reportes automáticos ---")
            generaReportePorcentaje(diccionario)
            generaReportePromedio(diccionario)
            generaReporteCantidadIntegrantes(diccionario)
            print("--------------------------------------")
            
        # Opción Salir (7)
        if op == "7":
            print("\n¡Gracias por usar el sistema de inscripción de SkillMatch! Éxitos en el hackathon.")
            break
        # Manejo de opciones inválidas
        elif op not in "123456":
            print("Opción inválida. Probá de nuevo.")


if __name__ == "__main__":
    main()

