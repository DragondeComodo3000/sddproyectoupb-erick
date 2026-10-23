# Plan de implementación: MVP de hábitos de estudio

Este plan traduce la especificación en una solución mínima y mantenible. No
añade funcionalidades fuera del MVP ni cambia sus reglas de negocio.

## Trazabilidad de requisitos

| Requisito | Cobertura principal |
|---|---|
| RF-1 | `core.py`, `storage.py`, `cli.py`, pruebas de creación y validación |
| RF-2 | `core.py`, `storage.py`, `cli.py`, pruebas de marcado y errores |
| RF-3 | `core.py`, `cli.py`, pruebas de orden, campos y listado vacío |
| RF-4 | `core.py`, `cli.py`, pruebas de rachas consecutivas e interrupciones |

## Estructura de módulos

- `habits/core.py`: modelo `Habit`, validaciones de negocio, creación, marcado
  y cálculo de racha. No dependerá de argumentos de consola ni imprimirá
  mensajes. Cubre RF-1, RF-2 y RF-4.
- `habits/storage.py`: lectura y escritura del conjunto de hábitos en JSON
  local. Convertirá fechas entre texto ISO y fechas del dominio. Cubre la
  persistencia de RF-1 y RF-2, y la disponibilidad requerida por RF-3.
- `habits/cli.py`: definición de argumentos, selección de operación, mensajes
  en español, códigos de salida y conexión entre dominio y persistencia. Cubre
  RF-1, RF-2 y RF-3.
- `habits/__main__.py`: punto de entrada para ejecutar la CLI como módulo. Cubre
  la exposición de RF-1, RF-2 y RF-3.
- `tests/`: pruebas del núcleo, persistencia y CLI. Verifica RF-1 a RF-4 y los
  requisitos no funcionales verificables.

## Modelo de datos JSON

El archivo local contendrá una lista de hábitos. La racha no se almacenará:
se derivará de `completed_dates` para evitar valores obsoletos.

Campos por hábito:

- `name`: texto no vacío y único.
- `description`: texto no vacío.
- `frequency`: valor `daily` para representar frecuencia diaria.
- `start_date`: fecha ISO `YYYY-MM-DD`, no futura.
- `completed_dates`: lista de fechas ISO, sin duplicados por hábito.

Ejemplo:

```json
[
  {
    "name": "Leer",
    "description": "Leer apuntes de la asignatura",
    "frequency": "daily",
    "start_date": "2026-10-20",
    "completed_dates": ["2026-10-21", "2026-10-22", "2026-10-23"]
  }
]
```

La creación y el marcado guardarán los cambios después de una operación válida;
una operación rechazada no modificará los datos existentes. Esto cubre RF-1,
RF-2 y la persistencia entre ejecuciones.

## Algoritmo de cálculo de racha

La racha mostrada es la racha actual: debe terminar en el día actual. Si el
día actual no está marcado, el resultado es cero.

```text
calcular_racha(habito, hoy):
    si hoy no pertenece a habito.completed_dates:
        devolver 0

    fechas = convertir completed_dates a conjunto
    racha = 0
    dia = hoy

    mientras dia pertenece a fechas:
        racha = racha + 1
        dia = dia anterior

    devolver racha
```

El conjunto permite consultar las fechas sin duplicarlas; la iteración hacia
atrás detiene el conteo en el primer día ausente. Cubre RF-4 y su uso en RF-3.

## Contrato de la CLI

La opción global `--data` permite indicar el archivo local; si se omite, se
usará el archivo local predeterminado del proyecto.

### Crear un hábito (RF-1)

```text
python -m habits --data RUTA create NOMBRE --description DESCRIPCION --frequency daily --start-date YYYY-MM-DD
```

- Éxito: muestra `Hábito creado: NOMBRE` y devuelve código `0`.
- Datos faltantes, frecuencia no diaria, fecha inválida, fecha futura o nombre
  duplicado: muestra un error en español y devuelve código `1`.
- El uso incorrecto de argumentos: muestra la ayuda de argumentos y devuelve
  código `2`.

### Marcar como hecho hoy (RF-2)

```text
python -m habits --data RUTA mark NOMBRE
```

- Éxito: muestra `Hábito marcado como hecho hoy: NOMBRE` y devuelve código `0`.
- Hábito inexistente o ya marcado hoy: muestra un error en español, conserva
  los datos y devuelve código `1`.
- No se acepta una fecha como argumento: el comando siempre usa el día actual;
  cualquier intento de fecha pasada o futura queda fuera del contrato y no se
  registra.

### Listar hábitos (RF-3 y RF-4)

```text
python -m habits --data RUTA list
```

- Éxito con hábitos: muestra todos ordenados alfabéticamente por nombre, con
  nombre, descripción, frecuencia diaria, fecha de inicio y racha actual;
  devuelve código `0`.
- Sin hábitos: muestra `No hay hábitos registrados.` y devuelve código `0`.
- Error de lectura o persistencia: muestra un error en español y devuelve
  código `1`.

Los mensajes visibles estarán en español; los nombres de módulos, funciones y
variables estarán en inglés, conforme a la constitución.

## Decisiones técnicas justificadas

### Biblioteca estándar y pytest

- Decisión: usar solo Python 3.12+, biblioteca estándar y pytest para pruebas.
- Justificación: reduce la carga cognitiva y cumple el stack simple exigido.
- Alternativa descartada: incorporar un framework CLI o una librería de fechas;
  aportaría dependencias y abstracciones innecesarias para tres comandos.

### JSON como lista de registros

- Decisión: un archivo JSON local con una lista de hábitos.
- Justificación: es legible, suficiente para el MVP y cumple la persistencia
  explícita de la constitución.
- Alternativa descartada: una base de datos; añadiría configuración y
  complejidad sin una necesidad del alcance actual.

### Racha derivada, no almacenada

- Decisión: guardar únicamente las fechas completadas y calcular la racha al
  listar.
- Justificación: evita inconsistencias entre una racha guardada y sus marcas.
- Alternativa descartada: guardar un contador actualizado al marcar; puede
  quedar obsoleto si el archivo se edita o contiene fechas discontinuas.

### Dominio independiente de la CLI

- Decisión: mantener validaciones y cálculo en el núcleo, dejando argumentos,
  impresión y códigos de salida en la CLI.
- Justificación: cumple la separación de lógica e interfaz y facilita pruebas
  directas del comportamiento.
- Alternativa descartada: implementar las reglas dentro de los manejadores de
  comandos; duplicaría validaciones y dificultaría su mantenimiento.

### Identificación por nombre

- Decisión: usar el nombre como identificador visible del MVP y rechazar
  nombres duplicados.
- Justificación: la spec exige unicidad y no requiere IDs visibles para el
  usuario.
- Alternativa descartada: exponer identificadores numéricos; añadiría un
  concepto que la spec no solicita.

## Estrategia de tests

- Pruebas unitarias del núcleo: creación válida, campos vacíos, frecuencia no
  diaria, fecha inválida o futura y nombres duplicados. Cubre RF-1.
- Pruebas unitarias de marcado: hábito inexistente, primera marca, segunda
  marca el mismo día y conservación de una sola fecha. Cubre RF-2.
- Pruebas unitarias de racha: cero sin marca hoy, una marca, varios días
  consecutivos y corte por día ausente. Cubre RF-4.
- Pruebas de persistencia: guardar y cargar conserva todos los campos y las
  fechas, y una operación rechazada no borra datos válidos. Cubre RF-1, RF-2 y
  el requisito de disponibilidad entre ejecuciones.
- Pruebas de CLI: comandos válidos, mensajes en español, orden alfabético,
  listado vacío, errores y códigos de salida. Cubre RF-1, RF-2 y RF-3.
- Pruebas de integración: crear, marcar, volver a cargar y listar para
  comprobar el flujo completo y la racha mostrada. Cubre RF-1, RF-2, RF-3 y
  RF-4.
- La ejecución obligatoria será `pytest -q`; ningún cambio se considerará
  terminado si la suite no pasa.

## Criterio de verificación del plan

La implementación solo estará lista cuando cada RF tenga pruebas de éxito y de
rechazo, la persistencia sobreviva entre ejecuciones, los mensajes sean en
español, el cálculo de racha coincida con el pseudocódigo y `pytest -q` pase.
