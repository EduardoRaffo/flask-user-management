from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from models import UserCreate, User
from types import SimpleNamespace
import json_users_data as jud
import validations as v
import os
from pyngrok import ngrok

load_dotenv()

app = FastAPI(
    title="API Usuarios",
    description="API REST para gestionar usuarios con validación",
    version="1.0.0"
)

# CORS - permite que un frontend en otro puerto acceda a la API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ngrok (opcional, para exponer localmente)
TOKEN = os.getenv("NGROK_TOKEN")
if TOKEN:
    ngrok.set_auth_token(TOKEN)
    try:
        public_url = ngrok.connect(8000)
        print(f"\n[OK] Public URL: {public_url}\n")
    except Exception as e:
        print(f"[WARNING] Ngrok error: {e}")


# ========================
# ENDPOINTS
# ========================

@app.get("/usuarios", response_model=list[User])
def listar_usuarios():
    """
    Obtiene la lista de todos los usuarios registrados.

    Retorna una lista vacía si no hay usuarios.
    """
    usuarios = jud.Load_users()
    return usuarios


@app.post("/usuarios", response_model=dict, status_code=201)
def crear_usuario(user: UserCreate):
    """
    Crea un nuevo usuario.

    Valida:
    - Email válido
    - Nombre y apellido válidos
    - Contraseña mínimo 6 caracteres
    - Teléfono 9-10 dígitos
    - Edad 10-120 años

    Retorna el usuario creado con su ID.
    """
    # Convertir modelo Pydantic a diccionario para pasar a validador
    data = user.dict()

    # Validar con la clase UserValidator existente
    validator = v.UserValidator(data)

    if not validator.validate():
        raise HTTPException(
            status_code=400,
            detail={
                "mensaje": "Errores de validación",
                "errores": validator.errors
            }
        )

    # Cargar usuarios existentes, agregar el nuevo y guardar
    usuarios = jud.Load_users()
    usuarios.append(SimpleNamespace(**data))
    jud.Save_users(usuarios)

    # Obtener el usuario creado con su ID asignado
    index, usuario_creado = jud.User_by_ID(len(usuarios))

    return {
        "mensaje": "Usuario registrado correctamente",
        "usuario": {
            "id": usuario_creado.id,
            "user_name": usuario_creado.user_name,
            "user_surname": usuario_creado.user_surname,
            "email": usuario_creado.email,
            "phone_num": usuario_creado.phone_num,
            "user_age": usuario_creado.user_age
        }
    }


@app.get("/usuarios/{user_id}", response_model=User)
def obtener_usuario(user_id: int):
    """
    Obtiene un usuario específico por su ID.

    Retorna 404 si el usuario no existe.
    """
    index, usuario = jud.User_by_ID(user_id)

    if usuario is None:
        raise HTTPException(
            status_code=404,
            detail=f"Usuario con ID {user_id} no encontrado"
        )

    return usuario


@app.put("/usuarios/{user_id}", response_model=dict)
def actualizar_usuario(user_id: int, user: UserCreate):
    """
    Actualiza un usuario existente.

    Valida los mismos campos que crear usuario.
    Retorna 404 si el usuario no existe.
    """
    index, usuario_existente = jud.User_by_ID(user_id)

    if index is None:
        raise HTTPException(
            status_code=404,
            detail=f"Usuario con ID {user_id} no encontrado"
        )

    # Validar datos
    data = user.dict()
    validator = v.UserValidator(data)

    if not validator.validate():
        raise HTTPException(
            status_code=400,
            detail={
                "mensaje": "Errores de validación",
                "errores": validator.errors
            }
        )

    # Actualizar - mantener el ID original
    usuarios = jud.Load_users()
    # Crear nuevo usuario con los datos pero preservar el ID
    nuevo_usuario = SimpleNamespace(**{**data, 'id': user_id})
    usuarios[index] = nuevo_usuario
    jud.Save_users(usuarios)

    return {
        "mensaje": "Usuario actualizado correctamente",
        "usuario": {
            "id": user_id,
            "user_name": user.user_name,
            "user_surname": user.user_surname,
            "email": user.email,
            "phone_num": user.phone_num,
            "user_age": user.user_age
        }
    }


@app.delete("/usuarios/{user_id}", response_model=dict)
def eliminar_usuario(user_id: int):
    """
    Elimina un usuario por su ID.

    Retorna 404 si el usuario no existe.
    """
    index, usuario = jud.User_by_ID(user_id)

    if index is None:
        raise HTTPException(
            status_code=404,
            detail=f"Usuario con ID {user_id} no encontrado"
        )

    jud.Delete_user(user_id)

    return {
        "mensaje": f"Usuario {user_id} eliminado correctamente"
    }


# Health check
@app.get("/")
def root():
    """Endpoint raíz para verificar que la API está corriendo"""
    return {
        "mensaje": "API de usuarios ejecutándose",
        "docs": "http://localhost:8000/docs",
        "endpoints": [
            "GET /usuarios",
            "POST /usuarios",
            "GET /usuarios/{user_id}",
            "PUT /usuarios/{user_id}",
            "DELETE /usuarios/{user_id}"
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
