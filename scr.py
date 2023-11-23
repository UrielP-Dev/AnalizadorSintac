class AnalizadorSintactico:
    tabla_predictiva = {
        'E': {
            'ID': ['T', "E'"],
            '(': ['T', "E'"]
        },
        "E'": {
            '+': ['+', 'T', "E'"],
            '$': [],  # Caso de vacío
            ')': [],  # Caso de vacío
        },
        'T': {
            'ID': ['F', "T'"],
            '(': ['F', "T'"]
        },
        "T'": {
            '+': [],  # Caso de vacío
            '*': ['*', 'F', "T'"],
            '$': [],  # Caso de vacío
            ')': [],  # Caso de vacío
        },
        'F': {
            'ID': ['ID'],
            '(': ['(', 'E', ')']
        }
    }

    # Ejemplo de uso
    def obtener_produccion(cls,no_terminal, siguiente_simbolo):
        return cls.tabla_predictiva[no_terminal][siguiente_simbolo]



    def validar_cadena(cls, cadena):
        
        caracteres_especiales = ['ID', '+', '*', '(', ')']
        for caracter in caracteres_especiales:
            cadena = cadena.replace(caracter, caracter + ' ')
        
        cadena_tokens = [token for token in cadena.split() if token != ''] + ['$']
        pila = ['$', 'E']
        indice = 0

        print("Cadena de entrada:", ' '.join(cadena_tokens))  # Mostrar cada caracter separado por un espacio

        while len(pila) > 0:
            simbolo_pila = pila.pop()
            
            # Manejar caso de fin de cadena
            if indice >= len(cadena_tokens):
                simbolo_actual = '$'
            else:
                simbolo_actual = cadena_tokens[indice]

            if simbolo_pila == simbolo_actual:
                indice += 1
            else:
                if simbolo_pila in cls.tabla_predictiva and simbolo_actual in cls.tabla_predictiva[simbolo_pila]:
                    produccion = cls.tabla_predictiva[simbolo_pila][simbolo_actual]
                    if produccion:
                        pila.extend(reversed(produccion))
                    else:
                        continue

            print("Pila:", pila)
            print("Cadena de entrada actual:", ' '.join(cadena_tokens[indice:]))  # Mostrar caracteres actuales separados

        if simbolo_pila == '$' and simbolo_actual == '$':
            return "La cadena es válida."
        else:
            return "La cadena no es válida."


    def validar_archivo(cls, nombre_archivo):
            todas_validas = True  # Bandera para verificar si todas las cadenas son válidas

            with open(nombre_archivo, 'r') as archivo:
                # Iterar sobre cada línea del archivo
                for linea in archivo:
                    # Procesar cada línea (quitar espacios adicionales al inicio y al final)
                    cadena_validar = linea.strip()
                    resultado = cls.validar_cadena(cadena_validar)
                    print(f"La cadena '{cadena_validar}' es: {resultado}")

                    if resultado == "La cadena no es válida.":
                        todas_validas = False  # Si alguna cadena es inválida, actualiza la bandera

            # Verificar si todas las cadenas son válidas y mostrar el mensaje correspondiente
            if todas_validas:
                print("El código fuente es correcto, todas las cadenas son válidas.")
            else:
                print("El código fuente contiene errores.")