# основной fastAPI сервер
from typing import List

from fastapi import FastAPI, Depends, HTTPException, status
from neomodel import db
from .models import Person
from .schemas import PersonCreate, PersonResponse, RelationshipCreate
from .auth import verify_token

app = FastAPI()

# Точка доступа для получения всех узлов
@app.get("/people", response_model=List[PersonResponse])
async def get_all_people():
    people = Person.nodes.all()
    return [PersonResponse(id=person.id, name=person.name, age=person.age) for person in people]

# Точка доступа для получения узла и его связей
@app.get("/people/{person_id}", response_model=PersonResponse)
async def get_person_and_relationships(person_id: str):
    person = Person.nodes.get(id=person_id)
    relationships = []
    for friend in person.friends:
        relationships.append({
            "id": friend.id,
            "name": friend.name,
            "age": friend.age
        })
    return {"id": person.id, "name": person.name, "age": person.age, "friends": relationships}

# Точка доступа для добавления узлов и связей (требует авторизации)
@app.post("/people", dependencies=[Depends(verify_token)])
async def create_person(person: PersonCreate):
    person_node = Person(name=person.name, age=person.age).save()
    return {"id": person_node.id, "name": person_node.name, "age": person_node.age}

# Точка доступа для добавления связи между двумя узлами (требует авторизации)
@app.post("/relationship", dependencies=[Depends(verify_token)])
async def create_relationship(relationship: RelationshipCreate):
    person_from = Person.nodes.get(id=relationship.from_person)
    person_to = Person.nodes.get(id=relationship.to_person)
    person_from.friends.connect(person_to)
    return {"message": "Связь добавлена"}

# Точка доступа для удаления узлов и связей (требует авторизации)
@app.delete("/people/{person_id}", dependencies=[Depends(verify_token)])
async def delete_person(person_id: str):
    person = Person.nodes.get(id=person_id)
    person.delete()
    return {"message": "Узел (профиль) удален"}

@app.delete("/relationship", dependencies=[Depends(verify_token)])
async def delete_relationship(relationship: RelationshipCreate):
    person_from = Person.nodes.get(id=relationship.from_person)
    person_to = Person.nodes.get(id=relationship.to_person)
    person_from.friends.disconnect(person_to)
    return {"message": "Связь удалена"}
