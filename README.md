## Integrantes

- Camilo Ramírez Restrepo
- Laura Daniela Molina Villar
- Leidy Viviana Osorio Jiménez
- Tim Ulf Pambor 

# Experimento Seguridad Arquitectura ABC Jobs

[Video: Presentación del experimento](https://uniandes-my.sharepoint.com/:v:/g/personal/t_pambor_uniandes_edu_co/ERJeT5J4rTlOrxvhiDHQgoQBWCNWL8lfeKF4QSMHyhuYqg?nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJPbmVEcml2ZUZvckJ1c2luZXNzIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXciLCJyZWZlcnJhbFZpZXciOiJNeUZpbGVzTGlua0RpcmVjdCJ9fQ&e=bXMWZn)

## Comandos para poder ejecutar el experimento:
- Ejecutar el experimento
  - Instalar Docker y Docker Compose
  - Ejecuta `docker compose up --renew-anon-volumes --abort-on-container-exit --force-recreate` dentro de la carpeta ExperimentoSeguridadABCJobs
  - Nota: Se puede configurar el número de peticiones con `NUM_PETICIONES=5000` dentro del archivo `compose.yaml`
- Analizar los resultados
  - Instalar Python 3
  - Ejecuta `python3 analyze.py logs/app_web.csv` dentro de la carpeta ExperimentoABCJobs

## Propósito del experimento
El objetivo principal de este experimento es evaluar la seguridad del microservicio AdminContrato mediante un sistema de autenticación y autorización implementado a través de un API Gateway y un microservicio Autorizador. Específicamente, se busca verificar si el sistema puede validar correctamente las solicitudes de los usuarios, emitir tokens de acceso solo a usuarios autorizados y controlar el acceso a un microservicio AdminContrato que gestiona (ver/editar) contratos.

## Resultados esperados
- Verificación exitosa de autenticación: Los usuarios que proporcionen credenciales válidas deben recibir un token de acceso. 
- Control de acceso efectivo: Solo los usuarios autorizados deberían poder acceder a contratos y realizar operaciones de escritura. 
- Respuestas adecuadas: 
  1. Si las credenciales son correctas se envía el token, si no un mensaje de error.
  2. Si el Autorizador verifica el rol del usuario y además que el token esté activo, envía a AdminContrato por medio de API Gateway la información del usuario (rol, id usuario). De lo contrario envía un código de acceso denegado
  3. Si AdminContrato verifica que el usuario que intenta hacer la edición del contrato fue la que creó el mismo, envía un mensaje de confirmación a AppWeb, por medio del API Gateway. De lo contrario envía un código de acceso denegado.

## Recursos requeridos
- Cuatro computadores personales con Docker y Docker compose instalados, además deben contar con una licencia de un IDE para programación en Python.
- Framework: Flask.

## Elementos de arquitectura involucrados
- ASR: En una operación normal el componente Autorizador junto con AdminContrato deben garantizar que la edición de un contrato solo sea realizada por usuarios autorizados, esto el 100% de las veces.
- Elementos de la arquitectura afectados: Microservicio AdminContrato, Microservicio Autorizador, ApiGateway, y AppWeb.
- Vistas donde se encuentran elementos: Vista funcional, de despliegue, de información y de concurrencia.
- Punto de sensibilidad que se desean probar: El microservicio Autorizador, ya que será el encargado de generar los tokens, y verificar roles. 

## Esfuerzo estimado
Se estima que el experimento requerirá alrededor de 48 horas (12 horas/hombre) con un sprint de una semana, para la configuración, desarrollo, pruebas y análisis de resultados. 

# Experimento Disponibilidad Arquitectura ABC Jobs

[Video: Presentación del experimento](https://uniandes-my.sharepoint.com/:v:/g/personal/t_pambor_uniandes_edu_co/EWpLbfHMGX9KmgraP3S1Bh0BAPlQLoqeCBJSXkG-ocvKKw?nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJPbmVEcml2ZUZvckJ1c2luZXNzIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXciLCJyZWZlcnJhbFZpZXciOiJNeUZpbGVzTGlua0RpcmVjdCJ9fQ&e=EOoPh2)

## Comandos para poder ejecutar el experimento:
- Ejecutar el experimento
  - Instalar Docker y Docker Compose
  - Ejecuta `docker compose up --renew-anon-volumes --abort-on-container-exit --force-recreate` dentro de la carpeta ExperimentoABCJobs
  - Nota: Se puede configurar el número de peticiones con `NUM_MESSAGES=1000` dentro del archivo `compose.yaml`
- Analizar los resultados
  - Instalar Python 3
  - Ejecuta `python3 analyze.py` dentro de la carpeta ExperimentoABCJobs

## Propósito del experimento
Evaluar la implementación de las tácticas Voting y Redundancia Pasiva en el microservicio Motor de Emparejamiento para la detección de errores y recuperación de dicho servicio.

## Resultados esperados
Se espera que el microservicio Voting pueda detectar de 9 de 10 fallos y devolver el cálculo correcto de los mejores candidatos a EmpresaProyecto.

## Recursos requeridos
Cuatro computadores personales con Docker y Docker compose instalados, además deben contar con una licencia de un IDE para programación en Python.
Framework: Flask.
Librerías: Celery, Redis, SQLAlchemy.

## Elementos de arquitectura involucrados
ASR: En operación normal, al ser creada una vacante, si MotorEmparejamiento falla al calcular los mejores candidatos para dicha vacante, el fallo debe ser detectado 9 de 10 veces. 
Elementos de la arquitectura afectados: Microservicio MotorEmparejamiento, Microservicio Voting, Microservicio EmpresaProyecto, y Cola de mensajes.
Vistas donde se encuentran elementos: Vista funcional, de despliegue, de información y de concurrencia.
Punto de sensibilidad que se desean probar: Uso de Cola de mensajes para la comunicación entre EmpresaProyecto y Voting, además la implementación de la táctica Voting para detectar fallos en MotorEmparejamiento.

## Esfuerzo estimado
Se estima que el experimento requerirá alrededor de 48 horas (12 horas/hombre) con un sprint de una semana, para la configuración, desarrollo, pruebas y análisis de resultados. 
