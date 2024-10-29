from typing import List

from core.deps import get_current_user, get_session
from fastapi import APIRouter, Depends, HTTPException, Response, status
from models.artigo_model import ArtigoModel
from models.usuario_model import UsuarioModel
from schemas.artigo_schema import ArtigoSchema
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select


ARTIGO_NAO_ENCONTRADO = "Artigo não encontrado."

router = APIRouter()


# POST Artigo
@router.post("/", response_model=ArtigoSchema, status_code=status.HTTP_201_CREATED)
async def post_artigo(artigo: ArtigoSchema, usuario_logado: UsuarioModel = Depends(get_current_user), db: AsyncSession = Depends(get_session)):
    novo_artigo: ArtigoModel = ArtigoModel(
        titulo=artigo.titulo,
        descricao=artigo.descricao,
        url_fonte=artigo.url_fonte,
        usuario_id=usuario_logado.id,
    )
    db.add(novo_artigo)
    await db.commit()
    return novo_artigo


# GET Artigos
@router.get("/", response_model=List[ArtigoSchema], status_code=status.HTTP_200_OK)
async def get_artigos(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ArtigoModel)
        result = await session.execute(query)
        artigos: List[ArtigoModel] = result.scalars().unique().all()
        return artigos


# GET Artigo
@router.get("/{artigo_id}", response_model=ArtigoSchema, status_code=status.HTTP_200_OK)
async def get_artigo(artigo_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(ArtigoModel).filter(ArtigoModel.id == artigo_id)
        result = await session.execute(query)
        artigo: ArtigoModel = result.scalars().unique().one_or_none()

        if not artigo:
            raise HTTPException(detail=ARTIGO_NAO_ENCONTRADO, status_code=status.HTTP_404_NOT_FOUND)
        return artigo


# PUT Artigo
@router.put("/{artigo_id}", response_model=ArtigoSchema, status_code=status.HTTP_202_ACCEPTED)
async def put_artigo(artigo_id: int, artigo: ArtigoSchema, db: AsyncSession = Depends(get_session), usuario_logado: UsuarioModel = Depends(get_current_user)):
    async with db as session:
        query = select(ArtigoModel).filter(ArtigoModel.id == artigo_id)
        result = await session.execute(query)
        artigo_update: ArtigoModel = result.scalars().unique().one_or_none()

        if not artigo_update:
            raise HTTPException(detail=ARTIGO_NAO_ENCONTRADO, status_code=status.HTTP_404_NOT_FOUND)

        if artigo.titulo:
            artigo_update.titulo = artigo.titulo
        
        if artigo.descricao:
            artigo_update.descricao = artigo.descricao
        
        if artigo.url_fonte:
            artigo_update.url_fonte = artigo.url_fonte
        
        if usuario_logado.id != artigo_update.usuario_id:
            artigo_update.usuario_id = usuario_logado.id

        await session.commit()

        return artigo_update


# DELETE Artigo
@router.delete("/{artigo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_artigo(artigo_id: int, db: AsyncSession = Depends(get_session), usuario_logado: UsuarioModel = Depends(get_current_user)):
    async with db as session:
        query = select(ArtigoModel).filter(ArtigoModel.id == artigo_id).filter(ArtigoModel.usuario_id == usuario_logado.id)
        result = await session.execute(query)
        artigo: ArtigoModel = result.scalars().unique().one_or_none()

        if not artigo:
            raise HTTPException(detail=ARTIGO_NAO_ENCONTRADO, status_code=status.HTTP_404_NOT_FOUND)

        await session.delete()
        await session.commit()

        return Response(status_code=status.HTTP_204_NO_CONTENT)
