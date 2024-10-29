from typing import List, Optional

from pydantic import BaseModel, EmailStr
from schemas.artigo_schema import ArtigoSchema


class UsuarioSchemaBase(BaseModel):
    id: Optional[int] = None
    nome: str
    sobrenome: str
    email: EmailStr
    admin: bool = False

    class Config:
        from_attributes = True


class UsuarioSchemaCreate(UsuarioSchemaBase):
    senha: str


class UsuarioSchemaArtigos(UsuarioSchemaBase):
    artigos: Optional[List[ArtigoSchema]]


class UsuarioSchemaUpdate(UsuarioSchemaBase):
    nome: Optional[str] = None
    sobrenome: Optional[str] = None
    email: Optional[str] = None
    senha: Optional[str] = None
    admin: Optional[bool] = None
