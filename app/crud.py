from sqlalchemy.orm import Session
from app import schemas
from app import models


def get_producto(db: Session, producto_id: int):
    return db.query(models.Producto).filter(models.Producto.id == producto_id).first()

def get_productos(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Producto).offset(skip).limit(limit).all()

def create_producto(db: Session, producto: schemas.ProductoCreate):
    db_producto = models.Producto(**producto.dict())
    db.add(db_producto)
    db.commit()
    db.refresh(db_producto)
    return db_producto


def update_producto(db: Session, producto_id: int, producto: schemas.ProductoUpdate):
    db_producto = db.query(models.Producto).filter(models.Producto.id == producto_id).first()
    if db_producto is None:
        return None
    if producto.nombre is not None:
        db_producto.nombre = producto.nombre
    if producto.descripcion is not None:
        db_producto.descripcion = producto.descripcion
    if producto.precio is not None:
        db_producto.precio = producto.precio
    if producto.categoria_id is not None:
        db_producto.categoria_id = producto.categoria_id

    db.commit()
    db.refresh(db_producto)
    return db_producto

def delete_producto(db: Session, producto_id: int):
    filas_afectadas = db.query(models.Producto).filter(models.Producto.id == producto_id).delete()
    db.commit()
    return filas_afectadas

#categorias
def get_categoria(db: Session, categoria_id: int):
    result = (
        db.query(models.Categoria)
        .filter(models.Categoria.id == categoria_id)
        .with_entities(models.Categoria.id, models.Categoria.nombre)
        .first()
    )

    if result:
        return schemas.CategoryResponse(id=result[0], nombre=result[1])

    return None

def create_categoria(db: Session, categoria: schemas.CategoriaCreate):
    db_categoria = models.Categoria(**categoria.dict())
    db.add(db_categoria)
    db.commit()
    db.refresh(db_categoria)
    return db_categoria
def update_categoria(db: Session, categoria_id: int, categoria:schemas.CategoriaUpdate):
    db_categoria = db.query(models.Categoria).filter(categoria.id == categoria_id).first()
    if(db_categoria is None):
        return None
    if categoria.nombre is not None:
        db_categoria.nombre = categoria.nombre
    db.commit()
    db.refresh(db_categoria)
    return db_categoria

def delete_categoria(db: Session, categoria_id: int):
    filas_afectadas = db.query(models.Categoria).filter(models.Categoria.id == categoria_id).delete()
    db.commit()
    return filas_afectadas

def get_productos_by_categoria(db: Session, categoria_id: int):
    db_categoria = db.query(models.Categoria).filter(models.Categoria.id == categoria_id).first()
    if db_categoria is None:
        return None
    return db_categoria.productos

def get_productos_by_categoria_page(db: Session, categoria_id: int, page: int = 0, size: int = 10):
    db_categoria = db.query(models.Categoria).filter(models.Categoria.id == categoria_id).first()
    if db_categoria is None:
        return None
    offset = page * size
    if not hasattr(db_categoria, 'productos'):
        raise ValueError(f"La categoría con ID {categoria_id} no tiene productos asociados.")
    return db_categoria.productos[offset:offset + size]
