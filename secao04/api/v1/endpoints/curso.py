from typing import List

from core.deps import get_session
from fastapi import APIRouter, Depends, HTTPException, Response, status
from models.curso_model import CursoModel
from schemas.curso_schema import CursoSchema
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

CURSO_NAO_ENCONTRADO = "Curso não encontrado."

router = APIRouter()


# POST curso
@router.post("/", response_model=CursoSchema, status_code=status.HTTP_201_CREATED)
async def post_curso(curso: CursoSchema, db: AsyncSession = Depends(get_session)):
    novo_curso = CursoModel(titulo=curso.titulo, aulas=curso.aulas, horas=curso.horas)

    db.add(novo_curso)
    await db.commit()
    return novo_curso


# GET cursos
@router.get("/", response_model=List[CursoSchema], status_code=status.HTTP_200_OK)
async def get_cursos(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CursoModel)
        result = await session.execute(query)
        cursos: List[CursoModel] = result.scalars().all()

        return cursos


# GET curso
@router.get("/{curso_id}", response_model=CursoSchema, status_code=status.HTTP_200_OK)
async def get_curso(curso_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CursoModel).filter(CursoModel.id == curso_id)
        result = await session.execute(query)
        curso = result.scalar_one_or_none()

        if not curso:
            raise HTTPException(detail=CURSO_NAO_ENCONTRADO, status_code=status.HTTP_404_NOT_FOUND)
        return curso


# PUT curso
@router.put("/{curso_id}", response_model=CursoSchema, status_code=status.HTTP_202_ACCEPTED)
async def put_curso(curso_id: int, curso: CursoSchema, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CursoModel).filter(CursoModel.id == curso_id)
        result = await session.execute(query)
        curso_update = result.scalar_one_or_none()

        if not curso_update:
            raise HTTPException(detail=CURSO_NAO_ENCONTRADO, status_code=status.HTTP_404_NOT_FOUND)
        
        curso_update.titulo = curso.titulo
        curso_update.aulas = curso.aulas
        curso_update.horas = curso.horas
        await session.commit()
        return curso


# DELETE curso
@router.delete("/{curso_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_curso(curso_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(CursoModel).filter(CursoModel.id == curso_id)
        result = await session.execute(query)
        curso_delete = result.scalar_one_or_none()

        if not curso_delete:
            raise HTTPException(detail=CURSO_NAO_ENCONTRADO, status_code=status.HTTP_404_NOT_FOUND)

        await session.delete(curso_delete)
        await session.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
