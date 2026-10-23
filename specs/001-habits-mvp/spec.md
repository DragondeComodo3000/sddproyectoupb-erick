# Especificación: MVP de hábitos de estudio

## Contexto y objetivo

El proyecto necesita una forma sencilla de registrar hábitos de estudio y
consultar el cumplimiento diario. El objetivo del MVP es permitir crear
hábitos diarios, marcarlos como hechos durante el día actual y consultar la
racha consecutiva de cada hábito.

## Usuarios

- Estudiantes que desean registrar y revisar sus hábitos de estudio.
- Desarrolladores junior que necesitan mantener una funcionalidad pequeña y
  comprensible.

## Historias de usuario

- Como estudiante, quiero crear un hábito con sus datos básicos para empezar a
  registrar mi estudio.
- Como estudiante, quiero marcar un hábito como hecho hoy para registrar mi
  cumplimiento diario.
- Como estudiante, quiero listar mis hábitos con su racha para conocer mi
  continuidad de estudio.

## Requisitos funcionales

### RF-1: Crear un hábito

El usuario podrá crear un hábito proporcionando nombre, descripción, objetivo
de frecuencia y fecha de inicio. En el MVP, la frecuencia será diaria.

**Criterios de aceptación (EARS)**

- **Cuando** el usuario proporcione todos los datos requeridos y la frecuencia
  sea diaria, **el sistema deberá** crear el hábito.
- **Cuando** el hábito sea creado, **el sistema deberá** inicializar su racha
  en cero y conservar sus datos para consultas posteriores.
- **Si** falta el nombre, la descripción, la frecuencia o la fecha de inicio,
  **el sistema deberá** rechazar la creación y mostrar un mensaje explicativo.
- **Si** ya existe un hábito con el mismo nombre, **el sistema deberá**
  rechazar la creación.

### RF-2: Marcar un hábito como hecho

El usuario podrá marcar un hábito existente como hecho únicamente para el día
actual.

**Criterios de aceptación (EARS)**

- **Cuando** el usuario seleccione un hábito existente, **el sistema deberá**
  registrar una única marca de cumplimiento para el día actual.
- **Si** el usuario intenta registrar una fecha anterior o futura, **el
  sistema deberá** rechazar la operación.
- **Si** el hábito ya está marcado como hecho hoy, **el sistema deberá**
  rechazar la operación y conservar una sola marca para ese día.
- **Si** el hábito no existe, **el sistema deberá** rechazar la operación y
  mostrar un mensaje de error.

### RF-3: Listar hábitos y rachas

El usuario podrá consultar todos sus hábitos ordenados alfabéticamente por
nombre, mostrando nombre, descripción, frecuencia diaria, fecha de inicio y
racha actual.

**Criterios de aceptación (EARS)**

- **Cuando** el usuario solicite el listado, **el sistema deberá** mostrar
  todos los hábitos ordenados alfabéticamente por nombre.
- **Cuando** se muestre un hábito, **el sistema deberá** incluir sus datos
  registrados y su racha actual.
- **Si** no existen hábitos, **el sistema deberá** mostrar un resultado vacío
  con un mensaje comprensible.

### RF-4: Calcular la racha

El sistema deberá calcular la cantidad de días consecutivos en que cada hábito
ha sido marcado como hecho.

**Criterios de aceptación (EARS)**

- **Cuando** un hábito tenga marcas en días consecutivos, **el sistema deberá**
  contar esos días como una sola racha.
- **Si** falta una marca en un día que interrumpe la continuidad, **el sistema
  deberá** finalizar la racha en ese punto.
- **Si** el hábito no está marcado hoy, **el sistema deberá** mostrar una racha
  actual de cero.

## Requisitos no funcionales

- Los mensajes dirigidos al usuario estarán en español.
- Las operaciones deberán producir errores comprensibles y no borrar datos
  válidos ante una entrada incorrecta.
- Los datos creados deberán mantenerse disponibles entre ejecuciones.
- El comportamiento especificado deberá ser verificable mediante pruebas.

## Casos límite

- Crear un hábito con nombre vacío o compuesto únicamente por espacios; deberá
  rechazarse.
- Crear un hábito con descripción vacía; deberá rechazarse.
- Crear un hábito con una fecha de inicio futura o inválida; deberá rechazarse.
- Crear dos hábitos con el mismo nombre.
- Marcar un hábito inexistente.
- Marcar dos veces el mismo hábito durante el mismo día.
- Solicitar el listado sin hábitos creados.
- Consultar un hábito sin marcas de cumplimiento.
- Existencia de días sin cumplimiento entre dos marcas.

## Fuera de alcance

- Frecuencias distintas de la diaria.
- Marcar hábitos para fechas pasadas o futuras.
- Editar o eliminar hábitos.
- Recordatorios, notificaciones o metas de rendimiento.
- Usuarios múltiples, autenticación o sincronización remota.
- Estadísticas distintas de la racha consecutiva.

## Criterios de finalización

- Las tres operaciones del MVP están especificadas y permiten crear, marcar y
  listar hábitos.
- Los requisitos funcionales tienen criterios de aceptación en notación EARS.
- Los casos límite y el fuera de alcance están documentados.
- No quedan dudas marcadas como `[NECESITA ACLARACIÓN]`.
- La especificación es coherente con la constitución del proyecto.

## Dudas abiertas

No hay dudas abiertas para el alcance del MVP.
