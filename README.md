# Experimento Arquitectura ABC Jobs

## Integrantes

- Camilo Ramírez Restrepo\
- Laura Daniela Molina Villar
- Leidy Viviana Osorio Jiménez
- Tim Ulf Pambor 

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


