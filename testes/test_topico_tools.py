import pytest 
from unittest.mock import patch

from tools.topico_tools import buscar_topicos

@pytest.mark.parametrize(
        "materia_id, expected_result",
        [
            (
                1,
                [
                    (1, "Introdução", "Conceitos iniciais", 1),
                    (2, "SELECT", "Consultas SQL", 2),
                ], 
            ),
            (
                2,
                [
                    (3, "Variáveis", "Tipos e variáveis", 1),
                    (4, "Funções", "Criação de funções", 2),
                ],
            ),
            (
                3,
                [],
            ),
        ]
    )
@patch('tools.topico_tools.get_connection')
def test_buscar_topicos(
    mock_get_connection, mock_banco, materia_id, expected_result
):
    mock_conn, mock_cursor = mock_banco

    mock_get_connection.return_value = mock_conn
    mock_cursor.fetchall.return_value = expected_result

    resultado = buscar_topicos.invoke({
        "materia_id": materia_id
    })

    assert resultado == expected_result

    mock_get_connection.assert_called_once()
    mock_cursor.execute.assert_called_once()
    mock_cursor.fetchall.assert_called_once()

