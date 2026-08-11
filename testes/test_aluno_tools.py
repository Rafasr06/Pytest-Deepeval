import pytest
from unittest.mock import patch

from tools.aluno_tools import buscar_aluno

@pytest.mark.parametrize(
        "aluno_id, expected_result",
        [
            (1, (1, "Rafael", "MAT123")),
            (2, (2, "Ana", "MAT456")),
            (3, (3, "Carlos", "MAT789")),
            (4, (4, "Mariana", "MAT012"))
        ]
    )

@patch('tools.aluno_tools.get_connection')
def test_buscar_aluno(
    mock_get_connection, mock_banco, aluno_id, expected_result
):
    mock_conn, mock_cursor = mock_banco

    mock_get_connection.return_value = mock_conn
    mock_cursor.fetchone.return_value = expected_result


    resultado = buscar_aluno.invoke({
        "aluno_id": aluno_id
    })

    assert resultado == expected_result

    mock_get_connection.assert_called_once()

    mock_cursor.fetchone.assert_called_once()
        
