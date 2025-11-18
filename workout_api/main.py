from fastapi import FastAPI
from fastapi_pagination import add_pagination
from workout_api.atleta.controller import router as atleta_router
from workout_api.categorias.controller import router as categorias_router
from workout_api.centro_treinamento.controller import router as centro_treinamento_router

app = FastAPI(title='WorkoutAPI')

app.include_router(atleta_router, prefix='/atletas', tags=['atletas'])
app.include_router(categorias_router, prefix='/categorias', tags=['categorias'])
app.include_router(centro_treinamento_router, prefix='/centros_treinamento', tags=['centros_treinamento'])

# Add pagination support
add_pagination(app)
