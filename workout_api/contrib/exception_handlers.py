from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
import logging

logger = logging.getLogger(__name__)


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handler personalizado para erros de validação"""
    errors = []
    for error in exc.errors():
        field = " -> ".join(str(loc) for loc in error["loc"])
        errors.append({
            "field": field,
            "message": error["msg"],
            "type": error["type"]
        })
    
    logger.warning(f"Erro de validação na rota {request.url.path}: {errors}")
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": "Erro de validação nos dados fornecidos",
            "errors": errors
        }
    )


async def integrity_exception_handler(request: Request, exc: IntegrityError):
    """Handler personalizado para erros de integridade do banco"""
    logger.error(f"Erro de integridade no banco: {str(exc)}")
    
    error_msg = str(exc.orig) if hasattr(exc, 'orig') else str(exc)
    
    # Detecta tipo de erro
    if 'unique constraint' in error_msg.lower() or 'duplicate key' in error_msg.lower():
        if 'cpf' in error_msg.lower():
            message = "Já existe um atleta cadastrado com este CPF"
        elif 'nome' in error_msg.lower():
            message = "Já existe um registro com este nome"
        else:
            message = "Registro duplicado"
        
        return JSONResponse(
            status_code=status.HTTP_303_SEE_OTHER,
            content={"detail": message}
        )
    
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": "Erro de integridade no banco de dados"}
    )


async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    """Handler para erros gerais do SQLAlchemy"""
    logger.error(f"Erro do SQLAlchemy: {str(exc)}")
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Erro interno no servidor ao processar a requisição"}
    )


async def generic_exception_handler(request: Request, exc: Exception):
    """Handler genérico para exceções não tratadas"""
    logger.exception(f"Erro não tratado: {str(exc)}")
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Erro interno no servidor"}
    )
