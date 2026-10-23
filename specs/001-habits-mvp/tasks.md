# Tareas de implementación: MVP de hábitos de estudio

Las tareas están ordenadas por dependencia. Cada tarea está estimada para un
máximo de 20 a 30 minutos y debe conservar la separación entre dominio, datos e
interfaz.

## Preparación y dominio

- [x] **T1. Preparar la estructura mínima del proyecto.** Crear los paquetes de
  dominio, persistencia, CLI y pruebas definidos en el plan.
  **RF:** RF-1, RF-2, RF-3, RF-4.
  **Hecho cuando:** las rutas previstas existen y `pytest -q` puede descubrir la suite sin errores de importación.

- [x] **T2. Definir el modelo de hábito en el dominio.** Representar nombre,
  descripción, frecuencia, fecha de inicio y fechas completadas.
  **RF:** RF-1, RF-2, RF-3, RF-4.
  **Hecho cuando:** una prueba puede crear un hábito válido con todos los campos y una lista de completados inicialmente vacía.

- [ ] **T3. Implementar validaciones de creación.** Validar campos obligatorios,
  frecuencia diaria, fecha no futura y nombre único.
  **RF:** RF-1.
  **Hecho cuando:** las entradas vacías, inválidas, futuras, no diarias y duplicadas son rechazadas sin modificar la colección existente.

- [ ] **T4. Implementar el marcado del día actual.** Registrar una sola marca
  para un hábito existente y rechazar hábitos inexistentes o marcas repetidas.
  **RF:** RF-2.
  **Hecho cuando:** una primera marca se conserva y una segunda marca del mismo día devuelve un error sin duplicar la fecha.

- [ ] **T5. Implementar el cálculo de racha actual.** Aplicar el algoritmo de
  conteo hacia atrás desde hoy, con cero si hoy no está marcado.
  **RF:** RF-4.
  **Hecho cuando:** las pruebas cubren cero, una racha consecutiva y una interrupción por día ausente.

## Persistencia

- [ ] **T6. Implementar la conversión del modelo a JSON.** Serializar fechas en
  formato ISO y guardar la lista de hábitos sin almacenar la racha calculada.
  **RF:** RF-1, RF-2, RF-3, RF-4.
  **Hecho cuando:** el JSON generado coincide con el modelo documentado y contiene todos los campos esperados.

- [ ] **T7. Implementar la carga desde JSON.** Reconstruir hábitos y fechas desde
  el archivo local, incluyendo el caso de archivo inexistente.
  **RF:** RF-1, RF-2, RF-3.
  **Hecho cuando:** guardar y cargar un hábito produce datos equivalentes y un archivo inexistente produce una colección vacía.

- [ ] **T8. Proteger los datos ante operaciones rechazadas.** Asegurar que una
  validación fallida no sobrescriba ni elimine datos válidos.
  **RF:** RF-1, RF-2.
  **Hecho cuando:** una prueba conserva byte a byte el archivo anterior después de una creación o marca inválida.

## Interfaz de comandos

- [ ] **T9. Definir el contrato de argumentos y entrada.** Configurar los
  comandos `create`, `mark` y `list`, incluida la opción global del archivo JSON.
  **RF:** RF-1, RF-2, RF-3.
  **Hecho cuando:** los comandos válidos y sus argumentos requeridos aparecen en la ayuda de la CLI.

- [ ] **T10. Conectar el comando de creación.** Leer los datos del usuario,
  invocar el dominio, persistir el hábito y mostrar el mensaje de éxito.
  **RF:** RF-1.
  **Hecho cuando:** una ejecución válida crea un hábito persistente y muestra un mensaje de éxito en español.

- [ ] **T11. Conectar el comando de marcado.** Seleccionar el hábito por nombre,
  marcarlo con la fecha actual, persistirlo y mostrar el resultado.
  **RF:** RF-2.
  **Hecho cuando:** una ejecución válida registra hoy una sola vez y una repetida devuelve un error en español.

- [ ] **T12. Conectar el comando de listado.** Ordenar por nombre y mostrar todos
  los campos requeridos junto con la racha actual.
  **RF:** RF-3, RF-4.
  **Hecho cuando:** el listado ordena alfabéticamente, muestra la racha calculada y comunica claramente cuando no hay hábitos.

- [ ] **T13. Centralizar errores y códigos de salida.** Traducir errores de
  dominio, datos y argumentos al contrato de la CLI.
  **RF:** RF-1, RF-2, RF-3.
  **Hecho cuando:** éxito devuelve `0`, error de operación devuelve `1` y uso inválido devuelve `2`, con mensajes en español.

- [ ] **T14. Añadir el punto de entrada ejecutable.** Permitir ejecutar la CLI
  mediante el formato definido en el plan.
  **RF:** RF-1, RF-2, RF-3.
  **Hecho cuando:** `python -m habits --help` funciona y cada comando devuelve el código contratado.

## Verificación integrada

- [ ] **T15. Cubrir el flujo completo de persistencia.** Probar crear, cerrar o
  volver a ejecutar, marcar y listar un hábito.
  **RF:** RF-1, RF-2, RF-3, RF-4.
  **Hecho cuando:** la racha mostrada tras una nueva ejecución coincide con las marcas guardadas.

- [ ] **T16. Cubrir casos límite del MVP.** Añadir pruebas para nombre y
  descripción vacíos, fecha inválida o futura, duplicados, hábito inexistente,
  listado vacío y días sin cumplimiento.
  **RF:** RF-1, RF-2, RF-3, RF-4.
  **Hecho cuando:** cada caso límite de `spec.md` tiene una prueba con resultado esperado verificable.

- [ ] **T17. Ejecutar la verificación final.** Revisar mensajes en español,
  ausencia de dependencias no permitidas y trazabilidad de todos los RF.
  **RF:** RF-1, RF-2, RF-3, RF-4.
  **Hecho cuando:** `pytest -q` pasa completamente y cada RF tiene pruebas de éxito y rechazo.
