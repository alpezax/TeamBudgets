
# Reporte de autobalance 

```bash
curl -X POST http://localhost:8000/balance/generar-informe \
  -H "Content-Type: application/json" \
  -d '{
    "equipo_id": "681686f56166caa24736087a",
    "yyyy_mm": "2025-04",
    "nombre_reporte": "informe_custom.pdf",
    "carpeta_salida": "reportes_mensuales"
}'
```

# Validación de presupuesto

```bash
curl -X 'POST' \
  'http://localhost:8000/presupuestos/validar' \
  -H 'Content-Type: application/json' \
  -d '{
    "presupuesto_id": "682057c9be052e66d24dc6d8"
  }'
```

# Ejecución de un presupuesto

```bash
curl -X 'POST' \
  'http://localhost:8000/presupuestos/{presupuesto_id}/aplicar' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json'
```


```bash
curl -X 'POST' \
  'http://localhost:8000/presupuestos/682057c9be052e66d24dc6d8/aplicar' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json'
```