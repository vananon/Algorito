
def RefRespuesta(op, respuesta, nombreAlgoritmo):

    if op == '0':
        if respuesta[1:5] == "NONE":
            nombreAlgoritmo = "NONE" 
            respuesta = 'Ese algoritmo no existe :(\n Intenta mencionando otro o escribiendo el comando /recomendar para sugerirte un algoritmo :))'
        else:
            nombreAlgoritmo = respuesta[1:]
            respuesta = f"¡Perfecto!¿Qué buscas entender sobre {nombreAlgoritmo}? \nPuedo ayudarte a entender: \n1 Teoría \n2 Código \nHazmelo saber escribiendo 'Codigo' o 'Teoria'"
    elif op == '1':
        respuesta = respuesta[1:]  

    elif op == '2':
        respuesta = respuesta[1:]  

    elif op == '3':
        respuesta = f"El algoritmo que te recomiendo aprender es {respuesta[1:]}\nSi deseas entenderlo, utiliza el comando /aprender y escribe el nombre del algoritmo :)."

    elif op == '?':
        if nombreAlgoritmo != "NONE":
            respuesta = f"Veo que ya entendiste el algoritmo {nombreAlgoritmo}\nSi quieres entender otro, escribe el comando /aprender :)"
        else:
            respuesta = "Por favor, elige un comando :)"
    return op, respuesta, nombreAlgoritmo


def DefOp(op, mensaje, nombreAlgoritmo, respuesta):
    print(f"Valores antes de imprimir: op={op}, mensaje={mensaje[0:5]}, nombreAlgoritmo={nombreAlgoritmo}, respuesta={respuesta}")

    if (mensaje[0:6] == "Codigo" or mensaje[0] == '2') and nombreAlgoritmo != "NONE":
        op = '2'
        respuesta = "Por favor, indique el lenguaje de programación en que desea el código"
    
    elif (mensaje[0:6] == "Teoria" or mensaje[0] == '1') and nombreAlgoritmo != "NONE":
        op = '1'
        respuesta = '---'
    print(f"Valores despues de cambiar: op={op}, mensaje={mensaje}, nombreAlgoritmo={nombreAlgoritmo}, respuesta={respuesta}")
    return respuesta , op


def FormularReq(op, mensaje, nombreAlgoritmo):
    if(op== "3" or op== "0"):
        mensaje= op + mensaje
    else:
        mensaje= op + nombreAlgoritmo + " " +mensaje

    return mensaje