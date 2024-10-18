from fastapi import APIRouter, status, Depends
from services import service_cast
from sqlalchemy.orm import Session
from typing import List
from uuid import UUID
from shemas.shema import CastIn, CastOut
from models.db import get_db


router = APIRouter(prefix="/cast", tags=["casts"])


#non
@router.post("/", status_code=status.HTTP_201_CREATED , response_model=CastOut)
async def create_cast(film_id:UUID, c: CastIn = Depends(), db: Session = Depends(get_db)):
        return service_cast.create_cast(c, film_id, db)


#non
@router.get("/{id}", status_code=status.HTTP_202_ACCEPTED , response_model=CastOut)
async def get_one_cast(id: UUID, db: Session = Depends(get_db)):
    return service_cast.get_one_cast(id, db)


#oui
@router.get("/cast_film/{title}", status_code=status.HTTP_202_ACCEPTED , response_model=List[CastOut])
async def get_cast_one_film(title: str, db: Session = Depends(get_db)):
    return service_cast.get_cast_one_film(title, db)

#oui
@router.get("/cast_name/{name}", status_code=status.HTTP_202_ACCEPTED , response_model=List[CastOut])
async def get_cast_one_name(name: str, db: Session = Depends(get_db)):
    return service_cast.get_cast_one_name(name, db)


#oui
@router.get("/", status_code=status.HTTP_202_ACCEPTED , response_model=List[CastOut])
async def get_all_cast(db: Session = Depends(get_db), limit: int = 10):
    return service_cast.get_all_cast(limit, db)


#non
@router.put("/{id}", status_code=status.HTTP_202_ACCEPTED , response_model=CastOut)
async def update_cast(id: UUID, film_id: UUID = None, c: CastIn = Depends(), db: Session = Depends(get_db)):
    return service_cast.update_cast(id, film_id, c, db)
    

#non
@router.delete("/{id}", status_code=status.HTTP_202_ACCEPTED , response_model=CastIn)
async def delete_cast(id: UUID, db: Session = Depends(get_db)):
    return service_cast.delete_cast(id, db)