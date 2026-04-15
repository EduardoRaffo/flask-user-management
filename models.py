from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    """Datos que envía el cliente para crear o actualizar un usuario"""
    user_name: str = Field(..., min_length=2, description="Nombre del usuario")
    user_surname: str = Field(..., min_length=2, description="Apellido del usuario")
    email: str = Field(..., description="Email válido")
    password: str = Field(..., min_length=6, description="Contraseña (mínimo 6 caracteres)")
    phone_num: str = Field(..., description="Número de teléfono (9-10 dígitos)")
    user_age: int = Field(..., ge=10, le=120, description="Edad entre 10 y 120 años")

    class Config:
        json_schema_extra = {
            "example": {
                "user_name": "Juan",
                "user_surname": "Pérez",
                "email": "juan@example.com",
                "password": "123456",
                "phone_num": "1234567890",
                "user_age": 25
            }
        }


class User(UserCreate):
    """Usuario con ID (respuesta del servidor)"""
    id: int
