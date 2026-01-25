"""
LocalAI Assistant - Database Router
API endpoints para gerenciamento de bancos de dados
Author: Manus AI
"""

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import Dict, Any, List
from ..services.database_service import database_service

router = APIRouter(prefix="/database", tags=["Database"])


class SQLiteConnectionRequest(BaseModel):
    """Request model for SQLite connection"""
    db_path: str


class PostgreSQLConnectionRequest(BaseModel):
    """Request model for PostgreSQL connection"""
    host: str
    port: int = 5432
    database: str
    user: str
    password: str


class QueryRequest(BaseModel):
    """Request model for query execution"""
    connection_id: str
    query: str


class CreateTableRequest(BaseModel):
    """Request model for table creation"""
    connection_id: str
    table_name: str
    schema: Dict[str, str]


@router.post("/connect/sqlite")
async def connect_sqlite(request: SQLiteConnectionRequest):
    """
    Conectar a banco SQLite.
    
    - **db_path**: Caminho do banco de dados
    """
    result = await database_service.connect_sqlite(request.db_path)
    
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    
    return result


@router.post("/connect/postgresql")
async def connect_postgresql(request: PostgreSQLConnectionRequest):
    """
    Conectar a banco PostgreSQL.
    
    - **host**: Host do servidor
    - **port**: Porta
    - **database**: Nome do banco
    - **user**: Usuário
    - **password**: Senha
    """
    result = await database_service.connect_postgresql(
        request.host,
        request.port,
        request.database,
        request.user,
        request.password
    )
    
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    
    return result


@router.post("/execute")
async def execute_query(request: QueryRequest):
    """
    Executar query no banco de dados.
    
    - **connection_id**: ID da conexão
    - **query**: Query SQL
    """
    result = await database_service.execute_query(
        request.connection_id,
        request.query
    )
    
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    
    return result


@router.post("/create-table")
async def create_table(request: CreateTableRequest):
    """
    Criar tabela no banco de dados.
    
    - **connection_id**: ID da conexão
    - **table_name**: Nome da tabela
    - **schema**: Schema da tabela
    """
    result = await database_service.create_table(
        request.connection_id,
        request.table_name,
        request.schema
    )
    
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    
    return result


@router.post("/backup")
async def backup_database(
    connection_id: str = Query(...),
    backup_path: str = Query(...)
):
    """
    Fazer backup do banco de dados.
    
    - **connection_id**: ID da conexão
    - **backup_path**: Caminho do backup
    """
    result = await database_service.backup_database(connection_id, backup_path)
    
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    
    return result


@router.post("/restore")
async def restore_database(
    connection_id: str = Query(...),
    backup_path: str = Query(...)
):
    """
    Restaurar banco de dados de backup.
    
    - **connection_id**: ID da conexão
    - **backup_path**: Caminho do backup
    """
    result = await database_service.restore_database(connection_id, backup_path)
    
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    
    return result


@router.post("/migrate")
async def migrate_database(
    source_connection_id: str = Query(...),
    target_connection_id: str = Query(...)
):
    """
    Migrar dados entre bancos de dados.
    
    - **source_connection_id**: ID da conexão de origem
    - **target_connection_id**: ID da conexão de destino
    """
    result = await database_service.migrate_database(
        source_connection_id,
        target_connection_id
    )
    
    if "error" in result:
        raise HTTPException(status_code=500, detail=result["error"])
    
    return result
