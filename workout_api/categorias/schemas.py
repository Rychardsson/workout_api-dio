from typing import Annotated
from pydantic import Field, BaseModel


class CategoriaIn(BaseModel):
    nome: Annotated[str, Field(description='Nome da categoria', example='Scale', max_length=50)]


class CategoriaOut(CategoriaIn):
    id: Annotated[int, Field(description='Identificador da categoria')]


class CategoriaSimpleOut(BaseModel):
    nome: Annotated[str, Field(description='Nome da categoria', max_length=50)]
