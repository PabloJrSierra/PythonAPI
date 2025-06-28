# API de Segmentación de Usuarios por Tipo de Alimentación

Este proyecto implementa una API REST usando **FastAPI** para clasificar a un usuario en uno de 5 segmentos alimenticios generales basados en sus respuestas a 10 preguntas.

## Segmentos definidos

1. Vegano/Vegetariano  
2. Carnívoro Práctico  
3. Consciente Económico  
4. Dulcero Promocional  
5. Omnívoro Tradicional

## Endpoint

### `POST /recomendar`

#### Entrada:

```json
{
  "usuario_id": "uuid-del-usuario",
  "Frescos": 6,
  "Rapida": 5,
  "Saludable": 7,
  "Vegano": 5,
  "Dulce": 4,
  "Promo": 6,
  "Innovador": 5,
  "Tradicional": 6,
  "Precio": 5,
  "Ambiental": 7
}
```

#### Salida:

```json
{
  "usuario_id": "uuid-del-usuario",
  "grupo": 2,
  "segmento": "Consciente Económico",
  "fecha_registro": "2025-06-28T15:10:00.000000"
}
```

## Uso

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

Accede a la documentación Swagger: http://localhost:8000/docs
