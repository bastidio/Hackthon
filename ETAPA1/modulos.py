from faker import Faker
import random

def agregar_faker_equipo(arch, grupo, listaDNI, listaNombres, lenguajes):
    fake = Faker("es_ES")
    faltan = random.randint(1, 4)

    for k in range(faltan):
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
    while True:
        try:
            dni=input(texto)
            if dni=="":
                break
            if dni.isdigit() and minimo<=len(dni)<=maximo:
                break
            else:
                raise ValueError
        except ValueError:
            print(f"Error, ingrese un DNI con entre {minimo} y {maximo} dígitos.")
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


def generaArchivo():
    try:
        arch = open("hackaton.csv", "wt")
        arch.write("GRUPO;DNI;NOMBRE;PYTHON;JAVA;C++;JAVASCRIPT;PHP;C#\n")
        listaDNI = []
        listaNombres = []
        grupo = 1
        lenguajes = ["Python", "Java", "C++", "JavaScript", "PHP", "C#"]
    except IOError:
        print("Error al abrir el archivo.")
        return
    else:
        

        while True:
            dni = validarDNI("Ingrese su DNI (entre 7 y 8 caracteres)(Vacío para terminar): ", 7, 8)
            if dni == "":
                break
            if dni in listaDNI:
                print("Este DNI ya ha sido registrado. Vuelva a intentar.")
                continue

            nombre = validarNombre("Ingrese su nombre y apellido: ", 3).title()
            listaDNI.append(dni)
            listaNombres.append(nombre)

            niveles = cargarHabilidades()

            linea = f"{grupo};{dni};{nombre};{niveles[0]};{niveles[1]};{niveles[2]};{niveles[3]};{niveles[4]};{niveles[5]}\n"
            arch.write(linea)
            print(f"{nombre} agregado al grupo {grupo}.\n")

            completar = input("¿Desea completar su equipo automáticamente con Faker? (si/no): ").strip().lower()
            while completar not in ("si", "no"):
                completar = input("Responda si/no: ").strip().lower()

            if completar == "si":
                agregar_faker_equipo(arch, grupo, listaDNI, listaNombres, lenguajes)

        arch.close()
        print("Archivo generado con éxito.")


def generaDiccionario(dicc):
    try:
        arch=open("hackaton.csv","rt")
    except IOError:
        print("Error al abrir el archivo.")
    else:
        for linea in arch:
            grupo,dni,nombre,py,java,c,js,php,cs=linea.strip().split(";")
            if grupo not in dicc:
                dicc[grupo]={}
            if dni not in dicc[grupo]:
                dicc[grupo][dni]={}
            dicc[grupo][dni]["python"]=py
            dicc[grupo][dni]["java"]=java
            dicc[grupo][dni]["c++"]=c
            dicc[grupo][dni]["js"]=js
            dicc[grupo][dni]["php"]=php
            dicc[grupo][dni]["c#"]=cs
        arch.close()
        return dicc


def cargarHabilidades():

    lenguajes=["Python", "Java", "C++", "JavaScript", "PHP", "C#"]

    niveles = ["Nulo"] * len(lenguajes)
    respuestas_correctas = [0] * len(lenguajes)

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
        opcion = validarNumero("\nEligí del listado anterior el lenguaje que conocés. Te haremos unas preguntas sobre el mismo para evaluar tu nivel. Seleccioná uno del 1 al 6: ", 1, 6)
        lenguaje_indice = opcion - 1
        while lenguaje_indice in elegidos:
            print("Ya elegiste ese lenguaje. Elegí otro distinto.")
            opcion = validarNumero("\nEligí del listado anterior el lenguaje que conocés. Te haremos unas preguntas sobre el mismo para evaluar tu nivel. Seleccioná uno del 1 al 6: ", 1, 6)
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
    
    return niveles

def generaReportePorcentaje(dicc):
    try:
        arch = open("porcentaje_avanzados_python.csv", "wt")
    except IOError:
        print("Error al crear el archivo")
    else:
        arch.write(f"TOTAL INTEGRANTES;TOTAL AVANZADOS;PORCENTAJE\n")
        total_general = 0
        avanzados_general = 0
        for grupo, participantes in dicc.items():
            for dni, niveles in participantes.items():
                total_general += 1
                if "python" in niveles:
                    if str(niveles["python"]).strip().capitalize() == "Avanzado":
                        avanzados_general += 1
        porcentaje_general = (avanzados_general / total_general * 100) if total_general > 0 else 0.0
        arch.write(f"{total_general};{avanzados_general};{porcentaje_general:.2f}%\n")
        arch.close()

def generaReportePromedio(dicc):
    puntaje = {"Principiante": 1, "Intermedio": 2, "Avanzado": 3}
    try:
        arch = open("promedio_java.csv", "wt")
    except IOError:
        print("Error al crear el archivo")
    else:
        arch.write("PROMEDIO NIVEL JAVA")
        suma_total = 0
        cont_total = 0
        for grupo, participantes in dicc.items():
            for dni, niveles in participantes.items():
                if "java" in niveles:
                    nivel = str(niveles["java"]).strip().capitalize()
                    if nivel in puntaje:
                        suma_total += puntaje[nivel]
                        cont_total += 1
        if cont_total == 0:
            etiqueta = "NULO"
        else:
            promedio = suma_total / cont_total
            if promedio < 1.5:
                etiqueta = "PRINCIPIANTE"
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
        max_c = min_c = len(dicc[ks[0]])
        gmax = [ks[0]]
        gmin = [ks[0]]
        for i in range(1, len(ks)):
            g = ks[i]; c = len(dicc[g])
            if c > max_c: max_c, gmax = c, [g]
            elif c == max_c: gmax.append(g)
            if c < min_c: min_c, gmin = c, [g]
            elif c == min_c: gmin.append(g)
        arch.write(f"MAX;{max_c};{'|'.join(gmax)}\n")
        arch.write(f"MIN;{min_c};{'|'.join(gmin)}\n")
        arch.close()


def main():
    mensajeBienvenida()
    diccionario={}
    generaArchivo()
    if diccionario:
        generaReportePorcentaje(diccionario)
        generaReportePromedio(diccionario)
        generaReporteCantidadIntegrantes(diccionario)

    print("¡Gracias por usar el sistema de inscripción de SkillMatch!. Éxitos en el hackathon!")

if __name__ == "__main__":

    main()


