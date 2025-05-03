# TeamBudgets - Documentación de la API

## Inicio

```bash
uvicorn main:app --reload
```

## Tareas

### Ejecutar una tarea programada

Ejecuta una tarea de backend por nombre.

```bash
curl -X POST http://localhost:8000/task/execute \
  -H "Content-Type: application/json" \
  -d '{"task_name": "concilia_diaslaborables_por_oficina"}'
```

## Constantes

### Obtener todas las constantes

```bash
curl http://localhost:8000/constantes
```

### Obtener horas por jornada laboral

```bash
curl http://localhost:8000/constantes/horas-jornada
```

### Establecer horas por jornada laboral

```bash
curl -X POST http://localhost:8000/constantes/horas-jornada -d '{"horas": 9}' -H "Content-Type: application/json"
```

### Establecer tarifa para una fecha

```bash
curl -X POST http://localhost:8000/constantes/tarifa -d '{"fecha": "2025-02", "valor": 50.0}' -H "Content-Type: application/json"
```

### Obtener la última tarifa definida

```bash
curl http://localhost:8000/constantes/ultima-tarifa
```

### Obtener tarifa más cercana a una fecha dada

```bash
curl http://localhost:8000/constantes/tarifa-cercana/2025-05
```

## Categoría de Trabajadores

### Obtener todas las categorías

```bash
curl -X GET http://localhost:8000/categoria-trabajador/
```

### Obtener una categoría por ID

```bash
curl -X GET http://localhost:8000/categoria-trabajador/<ID>
```

### Obtener categoría por símbolo

```bash
curl -X GET http://localhost:8000/categoria-trabajador/simbolo/ANL
```

### Obtener último CSR por símbolo

```bash
curl -X GET http://localhost:8000/categoria-trabajador/csr/ANL/ultimo
```

### Obtener CSR por ID y mes

```bash
curl -X GET http://localhost:8000/categoria-trabajador/csr/<ID>/2025-03
```

### Actualizar CSR por ID y mes

```bash
curl -X PUT "http://localhost:8000/categoria-trabajador/csr/<ID>/2025-04" \
  -H "Content-Type: application/json" \
  -d '{"valor": 23}'
```

### Crear una nueva categoría

```bash
curl -X POST "http://localhost:8000/categoria-trabajador/" \
  -H "Content-Type: application/json" \
  -d '{"nombre": "Consultor", "clase": "A", "simbolo": "CNS"}'
```

### Eliminar categoría por ID

```bash
curl -X DELETE http://localhost:8000/categoria-trabajador/<ID>
```

## Oficinas

### Obtener todas las oficinas

```bash
curl -X GET "http://localhost:8000/oficina/"
```

### Obtener una oficina por ID

```bash
curl -X GET "http://localhost:8000/oficina/{id}"
```

### Crear nueva oficina

```bash
curl -X POST "http://localhost:8000/oficina/" \
     -H "Content-Type: application/json" \
     -d '{"ciudad": "Barcelona", "tipo": "Oficina Principal", "simbolo": "BCN"}'
```

### Actualizar oficina existente

```bash
curl -X PUT "http://localhost:8000/oficina/{id}" \
     -H "Content-Type: application/json" \
     -d '{"ciudad": "Madrid", "tipo": "Oficina Secundaria", "simbolo": "MAD"}'
```

### Eliminar oficina por ID

```bash
curl -X DELETE "http://localhost:8000/oficina/{id}"
```

### Obtener días laborables por mes

```bash
curl -X GET "http://localhost:8000/oficina/{id}/dias-laborables/2025-01"
```

### Establecer días laborables por mes

```bash
curl -X PUT "http://localhost:8000/oficina/{id}/dias-laborables/2025-01" \
     -H "Content-Type: application/json" \
     -d '{"valor": 22}'
```

### Obtener oficina por símbolo

```bash
curl -X GET "http://localhost:8000/oficina/simbolo/BCN"
```

### Obtener última fecha laborable de una oficina

```bash
curl -X GET "http://localhost:8000/oficina/simbolo/BCN/ultima-fecha-laborable"
```

## Proyectos

### Crear un proyecto

```bash
curl -X POST "http://localhost:8000/proyecto/" \
     -H "Content-Type: application/json" \
     -d '{"nombre": "Proyecto A", "idext": "EXT123", "descripcion": "Descripción del Proyecto A", "horas": {"venta": 100, "consumidas": 5}, "margen_contrato": {"2025-01": 0.3, "2025-02": 0.4, "2025-03": 0.5}}'
```

### Obtener todos los proyectos

```bash
curl -X GET "http://localhost:8000/proyectos/"
```

### Obtener proyecto por ID

```bash
curl -X GET "http://localhost:8000/proyecto/{id_str}"
```

### Actualizar un proyecto

```bash
curl -X PUT "http://localhost:8000/proyecto/{id_str}" \
     -H "Content-Type: application/json" \
     -d '{"nombre": "Proyecto A Modificado", "idext": "EXT123", "descripcion": "Descripción actualizada", "horas": {"venta": 120, "consumidas": 10}}'
```

### Eliminar un proyecto

```bash
curl -X DELETE "http://localhost:8000/proyecto/{id_str}"
```

### Obtener horas de un proyecto

```bash
curl -X GET "http://localhost:8000/proyecto/{id_str}/horas"
```

### Actualizar horas de un proyecto

```bash
curl -X PUT "http://localhost:8000/proyecto/{id_str}/horas" \
     -H "Content-Type: application/json" \
     -d '{"venta": 150, "consumidas": 20}'
```

### Obtener margen de contrato por mes

```bash
curl -X GET "http://localhost:8000/proyecto/{id_str}/margen-contrato/{yyyy_mm}"
```

### Actualizar margen de contrato por mes

```bash
curl -X PUT "http://localhost:8000/proyecto/{id_str}/margen-contrato/{yyyy_mm}" \
     -H "Content-Type: application/json" \
     -d '{"valor": 0.35}'
```

## Trabajadores

### Obtener todos los trabajadores

```bash
curl -X GET "http://localhost:8000/trabajadores/"
```

### Obtener trabajador por ID

```bash
curl -X GET "http://localhost:8000/trabajador/{id_str}"
```

### Obtener trabajador por alias

```bash
curl -X GET "http://localhost:8000/trabajador/alias/pperezg"
```

### Crear nuevo trabajador

```bash
curl -X POST "http://localhost:8000/trabajador/" \
     -H "Content-Type: application/json" \
     -d '{
           "nombre": "Pedro Perez Garcia",
           "oficina": "<ID_DE_LA_OFICINA>",
           "categoria": "<ID_DE_LA_CATEGORIA>",
           "alias": "pperezg",
           "tags": ["go"],
           "workpool": ["DEC"],
           "dedicacion_mensual": {
               "05-2025": {"work": 20, "vacation": 2},
               "06-2025": {"work": 19, "vacation": 1}
           },
           "coste_hora_mensual": {
               "2025-01": 22,
               "2025-02": 20,
               "2025-03": 21
           }
         }'
```

### Actualizar trabajador

```bash
curl -X PUT "http://localhost:8000/trabajador/{id_str}" \
     -H "Content-Type: application/json" \
     -d '{
           "tags": ["go", "python"],
           "alias": "pedrop"
         }'
```

### Eliminar trabajador

```bash
curl -X DELETE "http://localhost:8000/trabajador/{id_str}"
```

### Obtener dedicación mensual

```bash
curl -X GET "http://localhost:8000/trabajador/{id_str}/dedicacion/05-2025"
```

### Actualizar dedicación mensual

```bash
curl -X PUT "http://localhost:8000/trabajador/{id_str}/dedicacion/05-2025" \
     -H "Content-Type: application/json" \
     -d '{"work": 18, "vacation": 4}'
```

### Obtener coste-hora mensual

```bash
curl -X GET "http://localhost:8000/trabajador/{id_str}/coste/2025-03"
```

### Actualizar coste-hora mensual

```bash
curl -X PUT "http://localhost:8000/trabajador/{id_str}/coste/2025-03" \
     -H "Content-Type: application/json" \
     -d '21.5'
```

### Obtener dedicaciones de todos los trabajadores para un mes

```bash
curl -X GET "http://localhost:8000/trabajadores/dedicacion/05-2025"
```

### Obtener coste-hora de todos los trabajadores para un mes

```bash
curl -X GET "http://localhost:8000/trabajadores/coste/2025-03"
```
