from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
import logging

from workout_api.atleta.controller import router as atleta_router
from workout_api.categorias.controller import router as categorias_router
from workout_api.centro_treinamento.controller import router as centro_treinamento_router
from workout_api.contrib.exception_handlers import (
    validation_exception_handler,
    integrity_exception_handler,
    sqlalchemy_exception_handler,
    generic_exception_handler
)

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

app = FastAPI(
    title='WorkoutAPI',
    description='API para gerenciamento de competições de CrossFit',
    version='1.0.0',
    docs_url='/docs',
    redoc_url='/redoc'
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especifique os domínios permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar exception handlers
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(IntegrityError, integrity_exception_handler)
app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

# Registrar routers
app.include_router(atleta_router, prefix='/atletas', tags=['atletas'])
app.include_router(categorias_router, prefix='/categorias', tags=['categorias'])
app.include_router(centro_treinamento_router, prefix='/centros_treinamento', tags=['centros_treinamento'])

# Add pagination support
add_pagination(app)


@app.get('/', tags=['health'])
async def health_check():
    """Endpoint de health check"""
    return {
        "status": "ok",
        "message": "WorkoutAPI está funcionando!",
        "version": "1.0.0"
    }
