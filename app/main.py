# app/main.py
from typing import List

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, crud, database
from app import models


models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/productos/", response_model=schemas.Producto,status_code=201)
def crear_producto(producto: schemas.ProductoCreate, db: Session = Depends(get_db)):
    return crud.create_producto(db=db, producto=producto)

@app.get("/productos/{producto_id}", response_model=schemas.Producto)
def leer_producto(producto_id: int, db: Session = Depends(get_db)):
    db_producto = crud.get_producto(db=db, producto_id=producto_id)
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return db_producto
@app.get("/productos/pageable/",response_model=List[schemas.Producto])
def leer_productos_page(skip: int = 0,limit:int=10, db: Session = Depends(get_db)):
    return crud.get_productos(db=db,skip=skip,limit=limit)

@app.put("/productos/{producto_id}", response_model=schemas.Producto)
def update_producto(producto_id: int, producto: schemas.ProductoUpdate, db: Session = Depends(get_db)):
    db_producto = crud.update_producto(db=db, producto_id=producto_id, producto=producto)
    if db_producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return db_producto
@app.delete("/productos/{producto_id}", status_code=204)
def eliminar_producto(producto_id: int, db: Session = Depends(database.get_db)):
    db_producto = crud.delete_producto(db=db, producto_id=producto_id)
    if not db_producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")


#categorias

@app.post("/categorias/", response_model=schemas.Categoria)
def crear_categoria(categoria: schemas.CategoriaCreate, db: Session = Depends(get_db)):
    return crud.create_categoria(db=db, categoria=categoria)

@app.get("/categorias/{categoria_id}", response_model=schemas.CategoryResponse)
def leer_categoria(categoria_id: int, db: Session = Depends(get_db)):
    db_categoria = crud.get_categoria(db=db, categoria_id=categoria_id)
    if db_categoria is None:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return db_categoria
@app.get("/categorias/{categoria_id}/productos/",response_model=List[schemas.Producto])
def leer_productos_categoria(categoria_id:int,db: Session = Depends(get_db)):
    productos = crud.get_productos_by_categoria(db=db,categoria_id=categoria_id)
    if productos is None:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return productos
@app.get("/categorias/{categoria_id}/productos/pageable",response_model=List[schemas.Producto])
def leer_productos_categoria_page(categoria_id:int, page:int,size:int,db: Session = Depends(get_db)):
    productos = crud.get_productos_by_categoria_page(db=db,categoria_id=categoria_id,page=page,size=size)
    if productos is None:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
    return productos
@app.delete("/categorias/{categoria_id}", status_code=204)
def delete_producto(categoria_id: int, db: Session = Depends(database.get_db)):
    db_columnas = crud.delete_categoria(db=db,categoria_id=categoria_id)
    if db_columnas ==0:
        raise HTTPException(status_code=404, detail="Categoría no encontrada")
