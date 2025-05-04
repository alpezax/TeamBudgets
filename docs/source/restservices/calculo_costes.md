## 📘 API: Cálculo de Costes de Equipo

### 🔹 `POST /equipo/coste-mensual`

Calcula el coste mensual de un equipo para una fecha específica.

#### 🧾 Payload

```json
{
  "equipo_id": "string",     // ID del equipo
  "fecha": "YYYY-MM"         // Mes y año para el cálculo (ej. "2025-05")
}
```

#### ✅ Respuesta exitosa (200)

```json
{
  "fecha": "2025-05",
  "nombre-equipo": "Equipo-Imputaciones",
  "id": "681686f56166caa24736087a",
  "trabajadores": [
    {
      "id": "6814da9dce46f9c6485633b1",
      "nombre": "Carlos Rodríguez Pérez",
      "oficina": {
        "id": "6813daa75344e9f2e9a01b9b",
        "nombre": "MAD"
      },
      "participacion": 100,
      "dias-laborables_mes": 21,
      "dias-vacaciones": 2,
      "dias-imputables": 19,
      "total-horas": 152.0,
      "coste-hora-mensual": 22.5,
      "coste-trabajador": 3420.0,
      "desc": "Carlos Rodríguez Pérez (MAD) tiene una participación del 100%..."
    },
    {
      "id": "6814dba0ce46f9c6485633c8",
      "nombre": "Lucía García Fernández",
      "oficina": {
        "id": "6813daa75344e9f2e9a01b9b",
        "nombre": "MAD"
      },
      "participacion": 80,
      "dias-laborables_mes": 21,
      "dias-vacaciones": 2,
      "dias-imputables": 19,
      "total-horas": 152.0,
      "coste-hora-mensual": 18.0,
      "coste-trabajador": 3240.0,
      "desc": "Lucía García Fernández (MAD) tiene una participación del 80%..."
    },
    {
      "id": "6814db2bce46f9c6485633be",
      "nombre": "Juan Martínez López",
      "oficina": {
        "id": "6813daa75344e9f2e9a01b9b",
        "nombre": "BAR"
      },
      "participacion": 100,
      "dias-laborables_mes": 20,
      "dias-vacaciones": 1,
      "dias-imputables": 19,
      "total-horas": 152.0,
      "coste-hora-mensual": 20.0,
      "coste-trabajador": 3800.0,
      "desc": "Juan Martínez López (BAR) tiene una participación del 100%..."
    },
    {
      "id": "6814dc0ece46f9c6485633d0",
      "nombre": "Ana Sánchez Gómez",
      "oficina": {
        "id": "6813daa75344e9f2e9a01b9b",
        "nombre": "VAL"
      },
      "participacion": 50,
      "dias-laborables_mes": 21,
      "dias-vacaciones": 2,
      "dias-imputables": 19,
      "total-horas": 152.0,
      "coste-hora-mensual": 25.0,
      "coste-trabajador": 1900.0,
      "desc": "Ana Sánchez Gómez (VAL) tiene una participación del 50%..."
    },
    {
      "id": "6814dc45ce46f9c6485633d5",
      "nombre": "Pedro López Martínez",
      "oficina": {
        "id": "6813daa75344e9f2e9a01b9b",
        "nombre": "MAL"
      },
      "participacion": 100,
      "dias-laborables_mes": 22,
      "dias-vacaciones": 2,
      "dias-imputables": 20,
      "total-horas": 160.0,
      "coste-hora-mensual": 19.0,
      "coste-trabajador": 3040.0,
      "desc": "Pedro López Martínez (MAL) tiene una participación del 100%..."
    }
  ],
  "totales": {
    "total-horas": 760.0,
    "coste": 14400.0
  }
}
```

#### ⚠️ Posibles errores

* `404`: Equipo no encontrado, trabajador no encontrado o información incompleta
* `500`: Error interno inesperado

#### 📌 Ejemplo `curl`

```bash
curl -X POST http://localhost:8000/equipo/coste-mensual \
     -H "Content-Type: application/json" \
     -d '{
           "equipo_id": "681686f56166caa24736087a",
           "fecha": "2025-05"
         }'
```

---

### 🔹 `POST /equipo/forecast-coste`

Calcula el coste del equipo durante los próximos `n` meses desde una fecha inicial.

#### 🧾 Payload

```json
{
  "equipo_id": "string",         // ID del equipo
  "fecha_inicio": "YYYY-MM",     // Fecha de inicio del forecast
  "n_meses": 3                   // Número de meses hacia adelante
}
```

#### ✅ Respuesta exitosa (200)

```json
[
  {
    "fecha": "2025-05",
    "nombre-equipo": "MiEquipo-Imputaciones",
    "id": "681686f56166caa24736087a",
    "trabajadores": [...],
    "totales": {
      "total-horas": 760.0,
      "coste": 14400.0
    }
  },
  {
    "fecha": "2025-06",
    "nombre-equipo": "MiEquipo-Imputaciones",
    ...
  },
  ...
]
```

#### ⚠️ Posibles errores

* `500`: Error interno inesperado

#### 📌 Ejemplo `curl`

```bash
curl -X POST http://localhost:8000/equipo/forecast-coste \
     -H "Content-Type: application/json" \
     -d '{
           "equipo_id": "681686f56166caa24736087a",
           "fecha_inicio": "2025-05",
           "n_meses": 3
         }'
```
