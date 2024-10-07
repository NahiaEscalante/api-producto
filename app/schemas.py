from typing import Optional

from pydantic import BaseModel

class ProductoBase(BaseModel):
    nombre: str
    descripcion: str
    precio: float
    categoria_id: int

class ProductoCreate(ProductoBase):
    pass

class Producto(ProductoBase):
    id: int

    class Config:
        from_attributes = True  # Cambia orm_mode a from_attributes

class CategoriaBase(BaseModel):
    nombre: str

class CategoriaCreate(CategoriaBase):
    pass

class Categoria(CategoriaBase):
    id: int
    productos: list[Producto] = []

    class Config:
        from_attributes = True  # Cambia orm_mode a from_attributes

#dtos
class ProductoUpdate(BaseModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    precio: Optional[float] = None
    categoria_id: Optional[int] = None

class CategoriaUpdate(BaseModel):
    nombre: Optional[str] = None

class CategoryResponse(BaseModel):
    id: int
    nombre: str