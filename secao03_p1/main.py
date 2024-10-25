from time import sleep
from typing import Optional, Any

from fastapi import (Depends, FastAPI, Header, HTTPException, Path, Query,
                     Response, status)
from fastapi.responses import JSONResponse
from models import Curso, cursos


def fake_db():
    try:
        print("Abrindo conexão com banco de dados...")
        sleep(1)
    finally:
        print("Fechando conexão com banco de dados...")
        sleep(1)


app = FastAPI(
    title="API de Cursos",
    version="0.0.1",
    description="Uma API para estudos do FastAPI",
    )


@app.get("/cursos", 
         description="Retorna todos os cursos ou uma lista vazia.", 
         summary="Retorna todos os cursos",
         response_model=list[Curso],
         response_description="Cursos encontrados com sucesso")
async def get_cursos(db: Any = Depends(fake_db)):
    return cursos


@app.get("/cursos/{curso_id}",
         description="Retorna um curso específico da lista de cursos.",
         summary="Retorna um curso específico",
         response_model=Curso)
async def get_curso(curso_id: int = Path(title="ID do curso", description="Deve ser entre 1 e 2", gt=0, lt=3), db: Any = Depends(fake_db)):
    try:
        curso = cursos[curso_id]
        return curso
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Curso não encontrado.")


@app.post("/cursos", 
          status_code=status.HTTP_201_CREATED, 
          description="Adiciona um novo curso à lista de cursos.", 
          summary="Adiciona um novo curso",
          response_model=Curso)
async def post_curso(curso: Curso):
    next_id = len(cursos) + 1
    curso.id = next_id
    cursos.append(curso)
    return curso


@app.put("/cursos/{curso_id}",
         description="Atualiza um curso já existente na lista de cursos.",
         summary="Atualiza um curso",
         response_model=Curso)
async def put_curso(curso_id: int, curso: Curso, db: Any = Depends(fake_db)):
    if curso_id not in cursos:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Curso não encontrado.")

    cursos[curso_id] = curso
    del curso.id
    return curso


@app.delete("/cursos/{curso_id}",
            description="Deleta um curso da lista de cursos.",
            summary="Deleta um curso",
            response_model=Curso)
async def delete_curso(curso_id: int, db: Any = Depends(fake_db)):
    if curso_id not in cursos:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Curso não encontrado.")

    del cursos[curso_id]
    # return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.get("/calculadora")
async def calcular(a: int = Query(gt=5), b: int = Query(gt=10), x_geek: str = Header(), c: int = 0):
    print(f"X-GEEK: {x_geek}")
    return a + b + c


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info", reload=True)
