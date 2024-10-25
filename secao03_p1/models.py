from typing import Optional

from pydantic import BaseModel, field_validator

class Curso(BaseModel):
    id: Optional[int] = None
    titulo: str
    aulas: int
    horas: int

    @field_validator('titulo')
    def validar_titulo(cls, value: str):
        # Validação 1
        palavras = value.split(' ')
        if len(palavras) < 3:
            raise ValueError('O titulo deve ter pelo menos 3 palavras')
        
        # Validação 2
        if value.islower():
            raise ValueError('O titulo deve ser em capitalizado')
        return value
    
    @field_validator('aulas')
    def validar_aulas(cls, value: int):
        if value <= 12:
            raise ValueError('O curso deve conter mais do que 12 aulas')
        return value

    @field_validator('horas')
    def validar_horas(cls, value: int):
        if value <= 10:
            raise ValueError('O curso deve conter mais do que 10 horas de duração')
        return value


cursos = [
    Curso(id=1, titulo="Programação para leigos", aulas=42, horas=56),
    Curso(id=2, titulo="Algoritmos e lógica de programação", aulas=52, horas=66)
]
