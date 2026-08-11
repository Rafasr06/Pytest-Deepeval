import pytest 
from unittest.mock import AsyncMock

from src.progresso_async import buscar_progresso_materia_async

@pytest.mark.parametrize(
    "aluno_id, materia_id, retorno_banco, porcentagem_esperada",
    [
        (
            1,
            6,
            (6, "Algoritmos", 4, 2),
            50.0
        ),
        (
            2,
            4,
            (4, "Python", 10, 10),
            100.0
        ),
        (
            3,
            5,
            (5, "Banco de Dados", 8, 2),
            25.0
        ),
    ]
)
@pytest.mark.asyncio
async def test_buscar_progresso_materia_async(
    aluno_id,
    materia_id,
    retorno_banco,
    porcentagem_esperada
):
    repository = AsyncMock()

    repository.buscar_progresso.return_value = retorno_banco

    resultado = await buscar_progresso_materia_async(
        aluno_id=aluno_id,
        materia_id=materia_id,
        repository=repository
    )

    assert resultado["porcentagem"] == porcentagem_esperada

    repository.buscar_progresso.assert_awaited_once_with(
        aluno_id,
        materia_id
    )
