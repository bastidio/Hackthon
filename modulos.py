def mensajeBienvenida(ancho):#hola
    print(
        "=" * ancho + "\n" +
        "BIENVENIDO/A AL SISTEMA DE INSCRIPCIÓN DE SKILLMATCH".center(ancho) + "\n" +
        "=" * ancho + "\n" +
        "En este sistema vas a registrar tu participación en el proyecto.".center(ancho) + "\n" +
        "Los datos a solicitar serán:".center(ancho) + "\n" +
        "- Datos personales (nombre y DNI)".center(ancho) + "\n" +
        "- Selección de habilidades en distintos lenguajes".center(ancho) + "\n" +
        "- Breve cuestionario de validación de nivel".center(ancho) + "\n" +
        "- Años de experiencia en IT".center(ancho) + "\n" +
        "- Estado de equipo (si ya tenés o no)".center(ancho) + "\n\n" +
        "Con esta información se organizarán los equipos equilibradamente.".center(ancho) + "\n" +
        "=" * ancho
    )


def validarNombre(nombre):
    while len(nombre) < 3:
        print("El nombre es demasiado corto, ingrese nuevamente")
        nombre = input("Ingrese su nombre: ").title()
    return nombre


def validarDNI(dni, listaDNI):
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


def cargaParticipantes(listaNombre, listaDNI, equipo):
    nombre = input("Ingrese su nombre: ").title()
    nombre = validarNombre(nombre)
    listaNombre.append(nombre)
    dni = input("Ingrese su DNI: ").replace(".", "")
    dni = validarDNI(dni, listaDNI)
    listaDNI.append(dni)
    equipo.append(dni)


def registrar_edad(edad):
    if edad <= 1:
        valor = 1  # trainee
    elif edad <= 2:
        valor = 2  # junior
    elif edad <= 5:
        valor = 4  # semi senior
    else:
        valor = 6  # senior
    return valor


def pregExperienciaIt():
    preg = input("Ingrese la cantidad de años de experiencia que tiene en Informática: ")
    while not preg.isdigit():
        preg = input("Ingresá la cantidad de años usando solo números: ")
    respuesta = registrar_edad(int(preg))
    return respuesta


def pregEquipos(contador, equipo):
    preg = input("¿Tienes un equipo ya armado? (si/no)\n=> ").lower()
    while preg not in ["si", "no"]:
        preg = input("Perdón, no entendí. ¿Tienes un equipo ya armado? (si/no)\n=> ").lower()

    if preg == "si":
        if contador < 4:
            print(f"Llevas {contador} integrante(s) en tu grupo.")
            main(contador + 1, equipo)   
        else:
            print("Tu equipo ya tiene el máximo de 4 integrantes.")
            print("Tu equipo completo es:", equipo)
    else:
        print("Te asignaremos con gente que le falte integrantes")
        print("Tu equipo parcial es:", equipo)




def validar_numero(mensaje, minimo, maximo):
    num = int(input(mensaje))
    while num < minimo or num > maximo:
        print(f"Tiene que ser entre {minimo} y {maximo}.")
        num = int(input(mensaje))
    return num


def cargar_habilidades():
    lenguajes = ["Python", "Java", "C++", "JavaScript", "PHP", "C#"]
    niveles = []
    respuestas_correctas = []

    for i in range(len(lenguajes)):
        niveles.append("nulo")
        respuestas_correctas.append(0)

    print("\nLenguajes para evaluar:")
    for i in range(len(lenguajes)):
        print(f"{i+1}. {lenguajes[i]}")

    cant = validar_numero("¿En cuántos de estos lenguajes tenés conocimiento? (1-6): ", 1, 6)

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

    for i in range(cant):
        opcion = validar_numero(f"\nElige el lenguaje {i+1} (1-6): ", 1, 6)
        lenguaje_index = opcion - 1

        print(f"\nPreguntas sobre {lenguajes[lenguaje_index]}:")
        aciertos = 0

        for pregunta_num in range(3):
            pregunta = preguntas[lenguaje_index][pregunta_num]
            correcta = respuestas_correctas_lista[lenguaje_index][pregunta_num]
            respuesta = input(pregunta + "\nTu respuesta: ").upper()
            if respuesta == correcta:
                aciertos += 1

        respuestas_correctas[lenguaje_index] = aciertos

        if aciertos == 3:
            niveles[lenguaje_index] = "Avanzado"
        elif aciertos == 2:
            niveles[lenguaje_index] = "Intermedio"
        elif aciertos == 1:
            niveles[lenguaje_index] = "Básico"
        else:
            niveles[lenguaje_index] = "Nulo"

        print(f"Resultado de {lenguajes[lenguaje_index]}: {aciertos}/3 - Nivel: {niveles[lenguaje_index]}")

    print("\nTus resultados finales:")
    for i in range(len(lenguajes)):
        if niveles[i] != "nulo":
            print(f"{lenguajes[i]}: {niveles[i]} ({respuestas_correctas[i]}/3)")

    return lenguajes, niveles, respuestas_correctas



def main(contador=1, equipo="nuevo"):
    if equipo == "nuevo":
        equipo = []
    mensajeBienvenida(80)
    listaDNIs = []
    listaNombres = []

    
    cargaParticipantes(listaNombres, listaDNIs, equipo)

    
    print("\n=== Evaluación de habilidades ===")
    lenguajes, niveles, correctas = cargar_habilidades()

    experienciaLaboral = pregExperienciaIt()

    
    pregEquipos(contador, equipo)

