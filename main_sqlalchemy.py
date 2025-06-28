from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import json
import os
from datetime import datetime
from sqlalchemy import create_engine, Column, String, Integer, DateTime
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
import uuid

# Inicialización de FastAPI
app = FastAPI()

# Cargar modelo y scaler
scaler = joblib.load("modelos/scaler.pkl")
kmeans = joblib.load("modelos/kmeans_model.pkl")
with open("modelos/etiquetas.json", "r") as f:
    etiquetas = json.load(f)

# Variables de entorno para conexión segura
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_DATABASE = os.getenv("DB_DATABASE", "railway")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}"

# SQLAlchemy setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# Modelo de tabla usuarios_respuestas
class UsuarioRespuesta(Base):
    __tablename__ = "usuarios_respuestas"
    id = Column(PG_UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    usuario_id = Column(PG_UUID(as_uuid=True), unique=True, nullable=False)
    grupo = Column(Integer)
    segmento = Column(String)
    fecha_segmentacion = Column(DateTime)

# Pydantic schema
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
    fecha = datetime.now()

    # Guardar en la base de datos
    db = SessionLocal()
    try:
        usuario_uuid = uuid.UUID(usuario.usuario_id)
        existente = db.query(UsuarioRespuesta).filter_by(usuario_id=usuario_uuid).first()
        if existente:
            existente.grupo = grupo
            existente.segmento = segmento
            existente.fecha_segmentacion = fecha
        else:
            nuevo = UsuarioRespuesta(
                usuario_id=usuario_uuid,
                grupo=grupo,
                segmento=segmento,
                fecha_segmentacion=fecha
            )
            db.add(nuevo)
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()

    return {
        "usuario_id": usuario.usuario_id,
        "grupo": grupo,
        "segmento": segmento,
        "fecha_registro": fecha.isoformat()
    }
