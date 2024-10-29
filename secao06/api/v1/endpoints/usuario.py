from typing import Any, List, Optional

from core.auth import autenticar, criar_token_acesso
from core.deps import get_current_user, get_session
from core.security import gerar_hash_senha
from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from models.usuario_model import UsuarioModel
from schemas.usuario_schema import (UsuarioSchemaArtigos, UsuarioSchemaBase,
                                    UsuarioSchemaCreate, UsuarioSchemaUpdate)
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

USUARIO_NAO_ENCONTRADO = "Usuário não encontrado."

router = APIRouter()


# GET Logado
@router.get("/logado", response_model=UsuarioSchemaBase)
def get_logado(usuario_logado: UsuarioModel = Depends(get_current_user)):
    return usuario_logado


# POST / Signup
@router.post("/signup", response_model=UsuarioSchemaBase, status_code=status.HTTP_201_CREATED)
async def post_usuario(usuario: UsuarioSchemaCreate, db: AsyncSession = Depends(get_session)):
    novo_usuario: UsuarioModel = UsuarioModel(
        nome=usuario.nome,
        sobrenome=usuario.sobrenome,
        email=usuario.email,
        senha=gerar_hash_senha(usuario.senha),
        admin=usuario.admin,
    )
    async with db as session:
        try:
            session.add(novo_usuario)
            await session.commit()
            return novo_usuario
        except IntegrityError:
            raise HTTPException(detail="Já existe um usuário com este email cadastrado.", status_code=status.HTTP_406_NOT_ACCEPTABLE)


# GET Usuarios
@router.get("/", response_model=List[UsuarioSchemaBase], status_code=status.HTTP_200_OK)
async def get_usuarios(db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UsuarioModel)
        result = await session.execute(query)
        usuarios: List[UsuarioSchemaBase] = result.scalars().unique().all()
        return usuarios


# GET Usuario
@router.get("/{usuario_id}", response_model=UsuarioSchemaArtigos, status_code=status.HTTP_200_OK)
async def get_usuario(usuario_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.id == usuario_id)
        result = await session.execute(query)
        usuario: UsuarioSchemaArtigos = result.scalars().unique().one_or_none()

        if not usuario:
            raise HTTPException(detail=USUARIO_NAO_ENCONTRADO, status_code=status.HTTP_404_NOT_FOUND)
        return usuario


# PUT Usuario
@router.put("/{usuario_id}", response_model=UsuarioSchemaBase, status_code=status.HTTP_202_ACCEPTED)
async def put_usuario(usuario_id: int, usuario: UsuarioSchemaUpdate, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.id == usuario_id)
        result = await session.execute(query)
        usuario_update: UsuarioSchemaBase = result.scalars().unique().one_or_none()

        if not usuario:
            raise HTTPException(detail=USUARIO_NAO_ENCONTRADO, status_code=status.HTTP_404_NOT_FOUND)
        
        if usuario.nome:
            usuario_update.nome = usuario.nome
        
        if usuario.sobrenome:
            usuario_update.sobrenome = usuario.sobrenome
        
        if usuario.email:
            usuario_update.email = usuario.email
        
        if usuario.admin:
            usuario_update.admin = usuario.admin

        if usuario.senha:
            usuario_update.senha = gerar_hash_senha(usuario.senha)

        await session.commit()
        return usuario


# DELETE Usuario
@router.delete("/{usuario_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_usuario(usuario_id: int, db: AsyncSession = Depends(get_session)):
    async with db as session:
        query = select(UsuarioModel).filter(UsuarioModel.id == usuario_id)
        result = await session.execute(query)
        usuario: UsuarioSchemaArtigos = result.scalars().unique().one_or_none()

        if not usuario:
            raise HTTPException(detail=USUARIO_NAO_ENCONTRADO, status_code=status.HTTP_404_NOT_FOUND)
        
        await session.delete(usuario)
        await session.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)


# POST Login
@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_session)):
    usuario = await autenticar(email=form_data.username, senha=form_data.password, db=db)

    if not usuario:
        raise HTTPException(detail="Dados de acesso incorretos.", status_code=status.HTTP_400_BAD_REQUEST)
    return JSONResponse(content={
        "access_token": criar_token_acesso(sub=usuario.id),
        "token_type": "bearer"
        }, status_code=status.HTTP_200_OK)
