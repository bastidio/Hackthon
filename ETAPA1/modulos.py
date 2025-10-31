def mensaje_bienvenida():
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


def validar_nombre(nombre):
    while len(nombre) < 3 or not nombre.isalpha():
        print("El nombre es demasiado corto o tiene un número, ingrese nuevamente")
        nombre = input("Ingrese su nombre: ").title()
    return nombre


def validar_dni(dni, listaDNI):
    dni = dni.replace(".", "")
    while not dni.isdigit():
        print("El DNI debe estar compuesto solo de numeros. Ingrese nuevamente.")
        dni = input("Ingrese su DNI: ").replace(".", "")
    while len(dni) < 7 or len(dni) > 8:
        print("El DNI debe tener entre 7 y 8 caracteres. Ingrese nuevamente.")
        dni = input("Ingrese su DNI: ").replace(".", "")
    while dni in listaDNI:
        print("El DNI ya se encuentra registrado. Ingrese nuevamente.")
        dni = input("Ingrese su DNI: ").replace(".", "")
    return dni


def carga_participantes(listaNombre, listaDNI, equipo):
    nombre = input("Ingrese su nombre: ").title()
    nombre = validar_nombre(nombre)
    listaNombre.append(nombre)
    dni = input("Ingrese su DNI: ").replace(".", "")
    dni = validar_dni(dni, listaDNI)
    listaDNI.append(dni)
    equipo.append(dni)


def validar_numero(mensaje, minimo, maximo):
    num_str = input(mensaje)
    while not num_str.isdigit() or int(num_str) < minimo or int(num_str) > maximo:
        print(f"Tiene que ser un número entre {minimo} y {maximo}.")
        num_str = input(mensaje)
    return int(num_str)


def cargar_habilidades(matriz, lenguajes):

    niveles = ["Nulo"] * len(lenguajes)
    respuestas_correctas = [0] * len(lenguajes)

    print("\nLenguajes para evaluar:")
    for i in range(len(lenguajes)):
        print(f"{i+1}. {lenguajes[i]}")

    seleccion = validar_numero("¿En cuántos de estos lenguajes tenés conocimiento? (1-6): ", 1, 6)

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

    respuestas_correctas_lista = [
        ["B", "A", "B"],
        ["B", "C", "B"],
        ["B", "A", "B"],
        ["A", "B", "B"],
        ["A", "B", "A"],
        ["C", "B", "B"]
    ]

    elegidos = []

    while seleccion != 0:
        opcion = validar_numero("\nEligí del listado anterior el lenguaje que conocés. Te haremos unas preguntas sobre el mismo para evaluar tu nivel. Seleccioná uno del 1 al 6: ", 1, 6)
        lenguaje_indice = opcion - 1
        while lenguaje_indice in elegidos:
            print("Ya elegiste ese lenguaje. Elegí otro distinto.")
            opcion = validar_numero("\nEligí del listado anterior el lenguaje que conocés. Te haremos unas preguntas sobre el mismo para evaluar tu nivel. Seleccioná uno del 1 al 6: ", 1, 6)
            lenguaje_indice = opcion - 1

        seleccion -= 1

        elegidos.append(lenguaje_indice)

        print(f"\nPreguntas sobre {lenguajes[lenguaje_indice]}:")
        aciertos = 0

        for pregunta_num in range(3):
            pregunta = preguntas[lenguaje_indice][pregunta_num]
            correcta = respuestas_correctas_lista[lenguaje_indice][pregunta_num]
            respuesta = input(pregunta + "\nTu respuesta (A/B/C): ").replace(" ","").upper()
            while respuesta not in ["A", "B", "C"]:
                print("Opción inválida. Responda A, B o C.")
                respuesta = input("Tu respuesta (A/B/C): ").replace(" ","").upper()
            if respuesta == correcta:
                aciertos += 1

        respuestas_correctas[lenguaje_indice] = aciertos

        if aciertos == 3:
            niveles[lenguaje_indice] = "Avanzado"
        elif aciertos == 2:
            niveles[lenguaje_indice] = "Intermedio"
        elif aciertos == 1:
            niveles[lenguaje_indice] = "Básico"
        else:
            niveles[lenguaje_indice] = "Nulo"

        print(f"Resultado de {lenguajes[lenguaje_indice]}: {aciertos}/3 - Nivel: {niveles[lenguaje_indice]}")

    print("\nTus resultados finales:")
    for i in range(len(lenguajes)):
        if niveles[i] != "Nulo":
            print(f"{lenguajes[i]}: {niveles[i]} ({respuestas_correctas[i]}/3)")
    
    
    matriz.append(niveles)

def pregunta_equipos(contador, equipo, listaNombres, listaDNIs, niveles_matriz, lenguajes):
    preg = input("¿Tenés un equipo ya armado? (si o no)\n=> ").lower().strip()
    while preg not in ["si", "no"]:
        preg = input("Perdón, no entendí. ¿Tenés un equipo ya armado? (si o no)\n=> ").lower().strip()

    if preg == "si":
        total = validar_numero("¿Cuántos integrantes tiene tu equipo (incluyéndote)? (minimo 2 / maximo 5): ", 2, 5)
        faltan = total - contador
        print(f"Faltan cargar {faltan} integrante(s) de tu equipo.")

        for k in range(faltan):
            print(f"\n--- Ingresá la información del integrante #{k+2} ---")
            carga_participantes(listaNombres, listaDNIs, equipo)
            cargar_habilidades(niveles_matriz, lenguajes)

        print("\nTu equipo quedó conformado por los siguientes participantes:",end=" ")
        for i in range (len(equipo)):
            for j in range(len(listaDNIs)):
                if equipo[i] == listaDNIs[j]:
                    print(f"{listaNombres[j]}",end=", ")

    else:
        print("Te asignaremos con gente que le falte integrantes")


def nueva_carga(listaNombres, listaDNIs, niveles_matriz, equipos_declarados, lenguajes):
    preg = input("\n¿Querés cargar un nuevo participante o equipo? (si/no): ").lower()
    while preg not in ["si", "no"]:
        preg = input("Responda si/no: ").lower()

    while preg == "si":
        equipo = []
        carga_participantes(listaNombres, listaDNIs, equipo)
        print("\n=== Evaluación de habilidades ===")
        cargar_habilidades(niveles_matriz, lenguajes)
        pregunta_equipos(1, equipo, listaNombres, listaDNIs, niveles_matriz, lenguajes)

        agregar_equipo(equipo, equipos_declarados)

        preg = input("\n¿Querés cargar un nuevo participante? (si/no): ").lower()
        while preg not in ["si", "no"]:
            preg = input("Responda si/no: ").lower()


def recorrer_matriz_equipos(mensaje, matriz):
    print("=" * 110)
    print(mensaje.center(110))
    print("=" * 110)

    # encabezado
    print("N° Equipo"," " * (1), end="")
    for i in range(5):
        print(f"Integrante {i+1}".center(15), end="")
    print()
    print()
    # filas
    for i in range(len(matriz)):
        print(f"Equipo {i+1}".ljust(10), end="")
        for j in range(len(matriz[i])):
            print(f"{matriz[i][j]}".center(15), end="")
        print()


def recorrer_matriz_nivel(mensaje,matriz,fila,lenguajes):
    print("=" * 110)
    print(mensaje.center(110))
    print("=" * 110)

    # encabezado
    print("DNI"," " * (len(fila)-1), end="")
    for i in range(len(lenguajes)):
        print(f"{lenguajes[i]}".center(15), end="")
    print()
    print()
    # filas
    for i in range(len(matriz)):
        print(f"{fila[i]}".ljust(len(fila) + 3), end="")
        for j in range(len(matriz[i])):
            print(f"{matriz[i][j]}".center(15), end="")
        print()


def porcentaje_avanzados_python(niveles_matriz):
    total = len(niveles_matriz)
    avanzados = 0
    for i in range(len(niveles_matriz)):
        if niveles_matriz[i][0] == "Avanzado":  # columna 0 es Python
            avanzados += 1
    porcentaje = lambda parte, total: (parte / total) * 100
    porcentaje_python = porcentaje(avanzados, total)
    print(f"\nPorcentaje de participantes con nivel Avanzado en Python: {porcentaje_python:.2f}%\n")


def contador_basico_dos_lenguajes(niveles_matriz):
    contador = 0
    for fila in niveles_matriz: # recorre la matriz por filas
        basicos = fila.count("Básico")
        if basicos > 2:
            contador += 1
    print(f"\nCantidad de participantes con nivel Básico en más de 2 lenguajes: {contador}\n")


def porcentaje_equipos_java(equipos_declarados, listaDNIs, niveles_matriz):
    total_equipos = len(equipos_declarados)  # cantidad total de equipos cargados
    contador_si_cumplen = 0
    for equipo in equipos_declarados:
        suma_integrante_si_cumple = 0
        for dni in equipo:
            for i in range(len(listaDNIs)):
                if listaDNIs[i] == dni:
                    if niveles_matriz[i][1] in ("Intermedio", "Avanzado"):  # columna 1 = Java
                        suma_integrante_si_cumple += 1
        if suma_integrante_si_cumple > 2:
            contador_si_cumplen += 1
    porcentaje = (contador_si_cumplen / total_equipos) * 100
    print(f"El {porcentaje:.2f}% de equipos cuentan con más de 2 integrantes con un nivel Intermedio o Avanzado en Java.") 


def agregar_equipo(equipo, equipos_declarados):
    if len(equipo) > 0:
        equipos_declarados.append(equipo[:])


def main():
    #LISTAS
    lenguajes = ["Python", "Java", "C++", "JavaScript", "PHP", "C#"]
    listaDNIs = []
    listaNombres = []
    equipo = []
    #MATRICES
    niveles_matriz = []
    equipos_declarados = []
    #MENSAJE DE BIENVENIDA
    mensaje_bienvenida()
    #CARGA DE PARTICIPANTES Y EQUIPOS
    carga_participantes(listaNombres, listaDNIs, equipo)
    print("\n=== Evaluación de habilidades ===")
    cargar_habilidades(niveles_matriz, lenguajes)
    #PERTENECE A UN EQUIPO?
    pregunta_equipos(1, equipo, listaNombres, listaDNIs, niveles_matriz, lenguajes)

    agregar_equipo(equipo, equipos_declarados)

    #CARGA DE NUEVOS PARTICIPANTES Y/O EQUIPOS
    nueva_carga(listaNombres, listaDNIs, niveles_matriz, equipos_declarados, lenguajes)

    #REPORTES
    print("\n=== Fin de inscripción ===")
    print("Participantes cargados:", len(listaDNIs))
    recorrer_matriz_equipos("MATRIZ DE EQUIPOS", equipos_declarados)
    recorrer_matriz_nivel("MATRIZ DE HABILIDADES", niveles_matriz, listaDNIs, lenguajes)
    porcentaje_avanzados_python(niveles_matriz)
    porcentaje_equipos_java(equipos_declarados, listaDNIs, niveles_matriz)
    contador_basico_dos_lenguajes(niveles_matriz)

    print("¡Gracias por usar el sistema de inscripción de SkillMatch!. Éxitos en el hackathon!")
