# Constitución del proyecto

1. **Stack simple:** Python 3.12+ y biblioteca estándar; pytest solo para tests.
2. **Spec primero:** toda funcionalidad debe estar definida en `specs/` antes del código.
3. **Lógica separada:** las reglas de negocio vivirán en `habits/core.py`, independientes de la CLI.
4. **Tests obligatorios:** cada cambio debe incluir o actualizar tests y pasar `pytest -q`.
5. **Persistencia explícita:** los datos se guardarán en JSON local; cualquier cambio de formato actualizará la spec.
6. **Idioma consistente:** identificadores y código estarán en inglés; mensajes visibles para usuarios, en español.
