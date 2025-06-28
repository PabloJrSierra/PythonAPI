from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import json
from datetime import datetime

app = FastAPI()

scaler = joblib.load("modelos/scaler.pkl")
kmeans = joblib.load("modelos/kmeans_model.pkl")
with open("modelos/etiquetas.json", "r") as f:
    etiquetas = json.load(f)

class UsuarioInput(BaseModel):
    usuario_id: str
    Frescos: int
    Rapida: int
    Saludable: int
    Vegano: int
    Dulce: int
    Promo: int
    Innovador: int
    Tradicional: int
    Precio: int
    Ambiental: int

@app.post("/recomendar")
def recomendar(usuario: UsuarioInput):
    datos = [[
        usuario.Frescos, usuario.Rapida, usuario.Saludable,
        usuario.Vegano, usuario.Dulce, usuario.Promo,
        usuario.Innovador, usuario.Tradicional,
        usuario.Precio, usuario.Ambiental
    ]]
    datos_scaled = scaler.transform(datos)
    grupo = int(kmeans.predict(datos_scaled)[0])
    segmento = etiquetas.get(str(grupo), "Desconocido")

    return {
        "usuario_id": usuario.usuario_id,
        "grupo": grupo,
        "segmento": segmento,
        "fecha_registro": datetime.now().isoformat()
    }
