def mensajeBienvenida(ancho):
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
    while len(nombre)<3:
        print("El nombre es demasiado corto, ingrese nuevamente")
        nombre=input("Ingrese su nombre: ").title()
    return nombre

def validarDNI(dni,listaDNI):
    while dni.isdigit()==False:
        print("El DNI debe estar compuesto solo de numeros. Ingrese nuevamente.")
        dni=input("Ingrese su DNI: ")
        dni=dni.replace(".","")
    while len(dni)<7 or len(dni)>8:
        print("El DNI debe tener entre 7 y 8 caracteres. Ingrese nuevamente.")
        dni=input("Ingrese su DNI: ")
        dni=dni.replace(".","")
    while dni in listaDNI:
        print("El DNI ya se encuentra registrado. Ingrese nuevamente.")
        dni=input("Ingrese su DNI: ")
        dni=dni.replace(".","")
    return dni


def cargaParticipantes(listaNombre,listaDNI,equipo):
    nombre=input("Ingrese su nombre: ").title()
    nombre=validarNombre(nombre)
    listaNombre.append(nombre)
    dni=input("Ingrese su DNI: ")
    dni=validarDNI(dni,listaDNI)
    listaDNI.append(dni)
    equipo.append(dni)


def registrar_edad(edad):
    if edad <= 1:
        valor = 1 #trainee
    elif edad <=2:
        valor = 2 #junior
    elif edad <= 5:
        valor = 4 #semi senior
    else :
        valor = 6 #senior
    return valor
    

def pregExperienciaIt():
    preg = input("Ingrese la cantidad de años de experiencia que tiene en Informática: ")
    while preg.isdigit() != True:
        preg = input("Ingresá la cantidad de años usando solo números: ")
    respuesta = registrar_edad(int(preg))
    return respuesta

def pregEquipos(contador, equipo):
    preg = input("¿Tienes un equipo ya armado? (si/no)\n=> ").lower()
    while preg != "si" and preg != "no":
        preg = input("Perdón, no entendí. ¿Tienes un equipo ya armado? (si/no)\n=> ").lower()

    if preg == "si":
        if contador < 4:
            print(f"Llevas {contador} integrante(s) en tu grupo.")
            main(contador + 1, equipo)   # vuelve a llamar main con contador+1
        else:
            print("Tu equipo ya tiene el máximo de 4 integrantes.")
            print("Tu equipo completo es:", equipo)
    else:
        print("Te asignaremos con gente que le falte integrantes")
        print("Tu equipo parcial es:", equipo)    

def main(contador=1, equipo = "nuevo"):
    if equipo == "nuevo":
        equipo = []
    if contador == 1:
        mensajeBienvenida(80)
    listaDNIs=[]
    listaNombres=[]
    experienciaLaboral = 0
    cargaParticipantes(listaNombres,listaDNIs,equipo)
    experienciaLaboral = pregExperienciaIt()
    pregEquipos(contador, equipo)
    
    
