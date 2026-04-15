from fastapi import FastAPI, HTTPException, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from models import UserCreate, User
from types import SimpleNamespace
import json_users_data as jud
import validations as v

app = FastAPI(
    title="API Usuarios",
    description="API REST para gestionar usuarios con validación",
    version="1.0.0"
)

templates = Jinja2Templates(directory="templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ========================
# RUTAS CON TEMPLATES (interfaz visual)
# ========================

@app.get("/")
def formulario(request: Request):
    return templates.TemplateResponse("form.html", {
        "request": request,
        "mensaje": "",
        "valores": None
    })

@app.post("/")
async def formulario_post(
    request: Request,
    nombre: str = Form(""),
    apellido: str = Form(""),
    email: str = Form(""),
    contraseña: str = Form(""),
    phone_num: str = Form(""),
    edad: str = Form("")
):
    data = {
        "user_name": nombre.strip(),
        "user_surname": apellido.strip(),
        "email": email.strip(),
        "password": contraseña.strip(),
        "phone_num": phone_num.strip(),
        "user_age": edad.strip()
    }

    validator = v.UserValidator(data)

    if validator.validate():
        usuarios = jud.Load_users()
        usuarios.append(SimpleNamespace(**data))
        jud.Save_users(usuarios)
        return templates.TemplateResponse("form.html", {
            "request": request,
            "mensaje": "Usuario registrado correctamente!",
            "valores": None
        })
    else:
        mensaje = "Errores: " + ", ".join(validator.errors)
        return templates.TemplateResponse("form.html", {
            "request": request,
            "mensaje": mensaje,
            "valores": SimpleNamespace(**data)
        })


@app.get("/usuarios")
def show_users(request: Request):
    usuarios = jud.Load_users()
    return templates.TemplateResponse("users.html", {
        "request": request,
        "usuarios": usuarios
    })


@app.get("/delete_user/{user_id}")
def delete_user(user_id: int):
    jud.Delete_user(user_id)
    return RedirectResponse(url="/usuarios", status_code=303)


@app.get("/edit/{user_id}")
def edit_user(request: Request, user_id: int):
    index, usuario = jud.User_by_ID(user_id)
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return templates.TemplateResponse("update_users.html", {
        "request": request,
        "usuario": usuario,
        "user_id": user_id,
        "mensaje": ""
    })


@app.post("/update/{user_id}")
async def update_user(
    request: Request,
    user_id: int,
    nombre: str = Form(""),
    apellido: str = Form(""),
    email: str = Form(""),
    contraseña: str = Form(""),
    phone_num: str = Form(""),
    edad: str = Form("")
):
    index, _ = jud.User_by_ID(user_id)
    if index is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    data = {
        "user_name": nombre.strip(),
        "user_surname": apellido.strip(),
        "email": email.strip(),
        "password": contraseña.strip(),
        "phone_num": phone_num.strip(),
        "user_age": edad.strip(),
        "id": user_id
    }

    validator = v.UserValidator(data)

    if validator.validate():
        usuarios = jud.Load_users()
        usuarios[index] = SimpleNamespace(**data)
        jud.Save_users(usuarios)
        return RedirectResponse(url="/usuarios", status_code=303)
    else:
        mensaje = "Errores: " + ", ".join(validator.errors)
        return templates.TemplateResponse("update_users.html", {
            "request": request,
            "usuario": SimpleNamespace(**data),
            "user_id": user_id,
            "mensaje": mensaje
        })


# ========================
# API REST (JSON)
# ========================

@app.get("/api/usuarios", response_model=list[User])
def listar_usuarios():
    """Lista todos los usuarios en formato JSON"""
    return jud.Load_users()


@app.post("/api/usuarios", response_model=dict, status_code=201)
def crear_usuario(user: UserCreate):
    """Crea un nuevo usuario via JSON"""
    data = user.model_dump()
    validator = v.UserValidator(data)

    if not validator.validate():
        raise HTTPException(status_code=400, detail={
            "mensaje": "Errores de validación",
            "errores": validator.errors
        })

    usuarios = jud.Load_users()
    usuarios.append(SimpleNamespace(**data))
    jud.Save_users(usuarios)
    _, usuario_creado = jud.User_by_ID(len(usuarios))

    return {"mensaje": "Usuario creado", "id": usuario_creado.id}


@app.get("/api/usuarios/{user_id}", response_model=User)
def obtener_usuario(user_id: int):
    """Obtiene un usuario por ID en formato JSON"""
    _, usuario = jud.User_by_ID(user_id)
    if usuario is None:
        raise HTTPException(status_code=404, detail=f"Usuario {user_id} no encontrado")
    return usuario


@app.put("/api/usuarios/{user_id}", response_model=dict)
def actualizar_usuario(user_id: int, user: UserCreate):
    """Actualiza un usuario via JSON"""
    index, _ = jud.User_by_ID(user_id)
    if index is None:
        raise HTTPException(status_code=404, detail=f"Usuario {user_id} no encontrado")

    data = user.model_dump()
    validator = v.UserValidator(data)

    if not validator.validate():
        raise HTTPException(status_code=400, detail={
            "mensaje": "Errores de validación",
            "errores": validator.errors
        })

    usuarios = jud.Load_users()
    usuarios[index] = SimpleNamespace(**{**data, 'id': user_id})
    jud.Save_users(usuarios)

    return {"mensaje": "Usuario actualizado", "id": user_id}


@app.delete("/api/usuarios/{user_id}", response_model=dict)
def eliminar_usuario(user_id: int):
    """Elimina un usuario via JSON"""
    index, _ = jud.User_by_ID(user_id)
    if index is None:
        raise HTTPException(status_code=404, detail=f"Usuario {user_id} no encontrado")

    jud.Delete_user(user_id)
    return {"mensaje": f"Usuario {user_id} eliminado"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
