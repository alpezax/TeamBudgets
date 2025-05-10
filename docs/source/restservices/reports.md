
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