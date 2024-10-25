from fastapi import FastAPI, HTTPException, Path, status
from models import Person


NOT_FOUND_MESSAGE = "This ID is not assigned to any person."
people = {
    1: {
        "name": "João Amgarten",
        "dob": "12/16/2003",
        "hobbies": ["Programming", "Listen to music", "Play the guitar"]
    },
    2: {
        "name": "Thiago Kammholz",
        "dob": "03/09/2005",
        "hobbies": ["Read the scriptures", "Study business", "Listen to music"]
    }
}

app = FastAPI()

@app.get("/people")
async def get_people():
    return people

@app.get("/people/{person_id}")
async def get_person(person_id: int = Path(gt=0, lt=3)):
    return people[person_id]

@app.post("/people")
async def post_person(person: Person):
    next_id = len(people) + 1
    people[next_id] = person
    return people[next_id]

@app.put("/people/{person_id}")
async def put_person(person: Person, person_id: int = Path(gt=0, lt=3)):
    people[person_id] = person
    return people[person_id]

@app.delete("/people/{person_id}")
async def delete_person(person_id: int = Path(gt=0, lt=3)):
    if person_id not in people:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=NOT_FOUND_MESSAGE)
    
    deleted_person = people[person_id]
    del people[person_id]
    return deleted_person


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("teste:app", log_level="info", reload=True)
