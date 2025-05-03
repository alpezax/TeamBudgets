# TeamBudgets

## Start

```bash
uvicorn main:app --reload
```


## Tasks

```bash
curl -X POST http://localhost:8000/task/execute \
  -H "Content-Type: application/json" \
  -d '{"task_name": "concilia_diaslaborables_por_oficina"}'
```

## Entidades

### Constantes

```bash
curl http://localhost:8000/constantes
```

```bash
curl http://localhost:8000/constantes/horas-jornada
```

```bash
curl -X POST http://localhost:8000/constantes/horas-jornada -d '{"horas": 9}' -H "Content-Type: application/json"
``` 

```bash 
curl -X POST http://localhost:8000/constantes/tarifa -d '{"fecha": "2025-02", "valor": 50.0}' -H "Content-Type: application/json"
``` 

```bash
curl http://localhost:8000/constantes/ultima-tarifa
``` 

```bash
curl http://localhost:8000/constantes/tarifa-cercana/2025-05
```

### Categoria de trabajadores

```bash
curl -X GET http://localhost:8000/categoria-trabajador/
``` 

```bash
curl -X GET http://localhost:8000/categoria-trabajador/<ID>
```

```bash
curl -X GET http://localhost:8000/categoria-trabajador/simbolo/ANL
```

```bash
curl -X GET http://localhost:8000/categoria-trabajador/csr/ANL/ultimo
``` 

```bash
curl -X GET http://localhost:8000/categoria-trabajador/csr/<ID>/2025-03
``` 

```bash
curl -X PUT "http://localhost:8000/categoria-trabajador/csr/<ID>/2025-04" \
  -H "Content-Type: application/json" \
  -d '{"valor": 23}'

curl -X PUT "http://localhost:8000/categoria-trabajador/csr/68138a0b7a56c166c1379f32/2025-04" \
  -H "Content-Type: application/json" \
  -d '{"valor": 23}'  
```

```bash
curl -X POST "http://localhost:8000/categoria-trabajador/" \
  -H "Content-Type: application/json" \
  -d '{"nombre": "Consultor", "clase": "A", "simbolo": "CNS"}'
```

```bash
curl -X DELETE http://localhost:8000/categoria-trabajador/<ID>
```

### Oficinas

1. Obtener todas las oficinas

```bash
curl -X GET "http://localhost:8000/oficina/"
```

1. Obtener una oficina por ID

```bash
curl -X GET "http://localhost:8000/oficina/{id}"
```

1. Crear una nueva oficina

```bash
curl -X POST "http://localhost:8000/oficina/" \
     -H "Content-Type: application/json" \
     -d '{"ciudad": "Barcelona", "tipo": "Oficina Principal", "simbolo": "BCN"}'
```

1. Actualizar una oficina existente

```bash
curl -X PUT "http://localhost:8000/oficina/{id}" \
     -H "Content-Type: application/json" \
     -d '{"ciudad": "Madrid", "tipo": "Oficina Secundaria", "simbolo": "MAD"}'

curl -X PUT "http://localhost:8000/oficina/681391223898ff6b729c7682" \
     -H "Content-Type: application/json" \
     -d '{"ciudad": "Madrid", "tipo": "Oficina Secundaria", "simbolo": "MAD"}'


```

1. Eliminar una oficina por ID

```bash
curl -X DELETE "http://localhost:8000/oficina/{id}"
``` 

1. Obtener los días laborables de una oficina para un mes específico

```bash
curl -X GET "http://localhost:8000/oficina/{id}/dias-laborables/2025-01"
``` 

1. Establecer los días laborables para una oficina y un mes específico

```bash
curl -X PUT "http://localhost:8000/oficina/{id}/dias-laborables/2025-01" \
     -H "Content-Type: application/json" \
     -d '{"valor": 22}'
```

1. Obtener una oficina por su símbolo

```bash
curl -X GET "http://localhost:8000/oficina/simbolo/BCN"
```

1. Obtener la última fecha laborable para una oficina por su símbolo

```bash
curl -X GET "http://localhost:8000/oficina/simbolo/BCN/ultima-fecha-laborable"
```

### Proyectos 

Aquí tienes los cURL necesarios para probar la API de `Proyecto`:

### 1. **Crear un Proyecto (POST)**
```bash
curl -X POST "http://localhost:8000/proyecto/" \
     -H "Content-Type: application/json" \
     -d '{"nombre": "Proyecto A", "idext": "EXT123", "descripcion": "Descripción del Proyecto A", "horas": {"venta": 100, "consumidas": 5}, "margen_contrato": {"2025-01": 0.3, "2025-02": 0.4, "2025-03": 0.5}}'
```

### 2. **Obtener Todos los Proyectos (GET)**
```bash
curl -X GET "http://localhost:8000/proyectos/"
```

### 3. **Obtener un Proyecto por ID (GET)**
```bash
curl -X GET "http://localhost:8000/proyecto/{id_str}"
```
Reemplaza `{id_str}` con el ID del proyecto que quieres obtener.

### 4. **Actualizar un Proyecto (PUT)**

```bash
curl -X PUT "http://localhost:8000/proyecto/{id_str}" \
     -H "Content-Type: application/json" \
     -d '{"nombre": "Proyecto A Modificado", "idext": "EXT123", "descripcion": "Descripción actualizada", "horas": {"venta": 120, "consumidas": 10}}'
```

### 5. **Eliminar un Proyecto (DELETE)**

```bash
curl -X DELETE "http://localhost:8000/proyecto/{id_str}"
```

### 6. **Obtener las Horas de un Proyecto (GET)**

```bash
curl -X GET "http://localhost:8000/proyecto/{id_str}/horas"
```

### 7. **Actualizar las Horas de un Proyecto (PUT)**

```bash
curl -X PUT "http://localhost:8000/proyecto/{id_str}/horas" \
     -H "Content-Type: application/json" \
     -d '{"venta": 150, "consumidas": 20}'
```

### 8. **Obtener el Margen de Contrato de un Proyecto para un Mes (GET)**
```bash
curl -X GET "http://localhost:8000/proyecto/{id_str}/margen-contrato/{yyyy_mm}"
```

### 9. **Actualizar el Margen de Contrato de un Proyecto para un Mes (PUT)**

```bash
curl -X PUT "http://localhost:8000/proyecto/{id_str}/margen-contrato/{yyyy_mm}" \
     -H "Content-Type: application/json" \
     -d '{"valor": 0.35}'
```


### Trabajadores

🔹 Obtener todos los trabajadores (GET)

```bash
curl -X GET "http://localhost:8000/trabajadores/"
```

🔹 Obtener un trabajador por ID (GET)

```bash
curl -X GET "http://localhost:8000/trabajador/{id_str}"
```


🔹 Obtener un trabajador por alias (GET)

```bash
curl -X GET "http://localhost:8000/trabajador/alias/pperezg"
```

🔹 Crear un nuevo trabajador (POST)

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

🔹 Actualizar un trabajador (PUT)

```bash
curl -X PUT "http://localhost:8000/trabajador/{id_str}" \
     -H "Content-Type: application/json" \
     -d '{
           "tags": ["go", "python"],
           "alias": "pedrop"
         }'
```

🔹 Eliminar un trabajador (DELETE)

```bash
curl -X DELETE "http://localhost:8000/trabajador/{id_str}"
```

🔹 Obtener la dedicación mensual para un trabajador (GET)

```bash
curl -X GET "http://localhost:8000/trabajador/{id_str}/dedicacion/05-2025"
```

🔹 Actualizar la dedicación mensual para un trabajador (PUT)

```bash
curl -X PUT "http://localhost:8000/trabajador/{id_str}/dedicacion/05-2025" \
     -H "Content-Type: application/json" \
     -d '{"work": 18, "vacation": 4}'
```

🔹 Obtener el coste-hora mensual para un trabajador (GET)

```bash
curl -X GET "http://localhost:8000/trabajador/{id_str}/coste/2025-03"
``` 

🔹 Actualizar el coste-hora mensual para un trabajador (PUT)

```bash
curl -X PUT "http://localhost:8000/trabajador/{id_str}/coste/2025-03" \
     -H "Content-Type: application/json" \
     -d '21.5'
``` 

🔹 Obtener dedicaciones de todos los trabajadores para un mes (GET)

```bash
curl -X GET "http://localhost:8000/trabajadores/dedicacion/05-2025"
``` 

🔹 Obtener coste-hora de todos los trabajadores para un mes (GET)

```bash
curl -X GET "http://localhost:8000/trabajadores/coste/2025-03"
```