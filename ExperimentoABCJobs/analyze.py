import csv

motor_1_detectado = set()
motor_2_detectado = set()
motor_3_detectado = set()

motor_1_producido = set()
motor_2_producido = set()
motor_3_producido = set()

with open('logs/voting.csv', newline='') as csvfile:
    data = csv.DictReader(csvfile)
    voting = [*data]

with open('logs/motor_emparejamiento_1.csv', newline='') as csvfile:
    data = csv.DictReader(csvfile)
    for row in data:
        motor_1_producido.add(int(row['id_vacante']))

with open('logs/motor_emparejamiento_2.csv', newline='') as csvfile:
    data = csv.DictReader(csvfile)
    for row in data:
        motor_2_producido.add(int(row['id_vacante']))

with open('logs/motor_emparejamiento_3.csv', newline='') as csvfile:
    data = csv.DictReader(csvfile)
    for row in data:
        motor_3_producido.add(int(row['id_vacante']))

for error_detectado in voting:
    if error_detectado['instancia'] == "motor_emparejamiento_1":
        motor_1_detectado.add(int(error_detectado['id_vacante']))
    if error_detectado['instancia'] == "motor_emparejamiento_2":
        motor_2_detectado.add(int(error_detectado['id_vacante']))
    if error_detectado['instancia'] == "motor_emparejamiento_3":
        motor_3_detectado.add(int(error_detectado['id_vacante']))

print("--- MotorEmparejamiento 1 ---")
#print(motor_1_producido)
#print(motor_1_detectado)
motor_1_identificados = motor_1_producido & motor_1_detectado
motor_1_falso_positivo = motor_1_detectado - motor_1_producido
motor_1_falso_negativo = motor_1_producido - motor_1_detectado
print(f"Detectados correctos: {len(motor_1_identificados)}")
print(f"Falsos positivos: {len(motor_1_falso_positivo)}")
print(f"Falsos negativos: {len(motor_1_falso_negativo)} {motor_1_falso_negativo}")

print("")
print("--- MotorEmparejamiento 2 ---")
#print(motor_2_producido)
#print(motor_2_detectado)
motor_2_identificados = motor_2_producido & motor_2_detectado
motor_2_falso_positivo = motor_2_detectado - motor_2_producido
motor_2_falso_negativo = motor_2_producido - motor_2_detectado
print(f"Detectados correctos: {len(motor_2_identificados)}")
print(f"Falsos positivos: {len(motor_2_falso_positivo)}")
print(f"Falsos negativos: {len(motor_2_falso_negativo)} {motor_2_falso_negativo}")

print("")
print("--- MotorEmparejamiento 3 ---")
#print(motor_3_producido)
#print(motor_3_detectado)
motor_3_identificados = motor_3_producido & motor_3_detectado
motor_3_falso_positivo = motor_3_detectado - motor_3_producido
motor_3_falso_negativo = motor_3_producido - motor_3_detectado
print(f"Detectados correctos: {len(motor_3_identificados)}")
print(f"Falsos positivos: {len(motor_3_falso_positivo)}")
print(f"Falsos negativos: {len(motor_3_falso_negativo)} {motor_3_falso_negativo}")

print("")
print("--- Total ---")
total_identificados = len(motor_1_identificados) + len(motor_2_identificados) + len(motor_3_identificados)
total_falso_positivo = len(motor_1_falso_positivo) + len(motor_2_falso_positivo) + len(motor_3_falso_positivo)
total_falso_negativo = len(motor_1_falso_negativo) + len(motor_2_falso_negativo) + len(motor_3_falso_negativo)
print(f"Detectados correctos: {total_identificados}")
print(f"Falsos positivos: {total_falso_positivo}")
print(f"Falsos negativos: {total_falso_negativo}")

un_error = len(motor_1_identificados - motor_2_identificados - motor_3_identificados) \
         + len(motor_2_identificados - motor_1_identificados - motor_3_identificados) \
         + len(motor_3_identificados - motor_1_identificados - motor_2_identificados)

dos_errores = len(motor_1_identificados & motor_2_identificados - motor_3_identificados) \
            + len(motor_1_identificados & motor_3_identificados - motor_2_identificados) \
            + len(motor_3_identificados & motor_2_identificados - motor_1_identificados)

tres_errores = len(motor_1_identificados & motor_2_identificados & motor_3_identificados)

print("")
print("--- Vacantes ---")
print(f"Con un error:          {un_error} (enmascarados)")
print(f"Con dos errores:        {dos_errores}")
print(f"Con tres errores:        {tres_errores}")
print(f"Con al menos un error: {un_error+dos_errores+tres_errores}")

print("")
print(f"Errores enviado a EmpresaProyecto: {dos_errores+tres_errores}")
