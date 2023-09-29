import csv
import sys

print(sys.argv[1])

caso_1 = []
caso_2 = []
caso_3 = []
caso_4 = []
caso_5 = []

with open(sys.argv[1], newline='') as csvfile:
    data = csv.DictReader(csvfile)
    for row in data:
        if row['caso'] == 'caso1':
            caso_1.append(row)
        elif row['caso'] == 'caso2':
            caso_2.append(row)
        elif row['caso'] == 'caso3':
            caso_3.append(row)
        elif row['caso'] == 'caso4':
            caso_4.append(row)
        elif row['caso'] == 'caso5':
            caso_5.append(row)

print("######")
print("Escenario 1: No ataque (Operación permitida) - Empleado de RRHH intenta editar el contrato que ha creado con token válido")
print("######")
caso1_intentos = len(caso_1)
caso1_permitidos = len([x for x in caso_1 if x['operacion_exitosa'] == 'True'])
caso1_denegados = len([x for x in caso_1 if x['operacion_exitosa'] == 'False'])
print(f"Intentos: {caso1_intentos}")
print(f"  Acceso permitido: {caso1_permitidos}")
print(f"  Acceso denegado: {caso1_denegados}")
print("")

print("######")
print("Escenario 2: Ataque (Operación prohibida) - Empleado de RRHH intenta editar el contrato que ha creado pero sin token válido")
print("######")
caso2_intentos = len(caso_2)
caso2_permitidos = len([x for x in caso_2 if x['operacion_exitosa'] == 'True'])
caso2_denegados = len([x for x in caso_2 if x['operacion_exitosa'] == 'False'])
print(f"Intentos: {caso2_intentos}")
print(f"  Acceso permitido: {caso2_permitidos}")
print(f"  Acceso denegado: {caso2_denegados} (Ataques resistidas)")
print("")

print("######")
print("Escenario 3: Ataque (Operación prohibida) - Empleado de RRHH intenta editar un contrato que fue creado por otro empleado (con token válido)")
print("######")
caso3_intentos = len(caso_3)
caso3_permitidos = len([x for x in caso_3 if x['operacion_exitosa'] == 'True'])
caso3_denegados = len([x for x in caso_3 if x['operacion_exitosa'] == 'False'])
print(f"Intentos: {caso3_intentos}")
print(f"  Acceso permitido: {caso3_permitidos}")
print(f"  Acceso denegado: {caso3_denegados} (Ataques resistidas)")
print("")

print("######")
print("Escenario 4: Ataque (Operación prohibida) - Candidato intenta editar su contrato (con token válido)")
print("######")
caso4_intentos = len(caso_4)
caso4_permitidos = len([x for x in caso_4 if x['operacion_exitosa'] == 'True'])
caso4_denegados = len([x for x in caso_4 if x['operacion_exitosa'] == 'False'])
print(f"Intentos: {caso4_intentos}")
print(f"  Acceso permitido: {caso4_permitidos}")
print(f"  Acceso denegado: {caso4_denegados} (Ataques resistidas)")
print("")

print("######")
print("Escenario 5: Ataque (Operación prohibida) - Candidato intenta editar contrato de otra persona (con token válido)")
print("######")
caso5_intentos = len(caso_5)
caso5_permitidos = len([x for x in caso_5 if x['operacion_exitosa'] == 'True'])
caso5_denegados = len([x for x in caso_5 if x['operacion_exitosa'] == 'False'])
print(f"Intentos: {caso5_intentos}")
print(f"  Acceso permitido: {caso5_permitidos}")
print(f"  Acceso denegado: {caso5_denegados} (Ataques resistidas)")
