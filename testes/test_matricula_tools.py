import pytest
from tools.matricula_tools import matricular_aluno

@pytest.mark.parametrize(
    "aluno_id, materia_id",
    [
        (1, 2),
        (3, 3),
        (5, 5)
    ]
)
def test_matricular_aluno(mocker, aluno_id, materia_id):
    mock_conn = mocker.MagicMock()
    mock_cursor = mocker.MagicMock()

    mock_conn.cursor.return_value = mock_cursor

    mocker.patch(
        'tools.matricula_tools.get_connection',
        return_value=mock_conn
    )

    resultado = matricular_aluno.invoke({
        "aluno_id": aluno_id,
        "materia_id": materia_id
    })

    assert resultado == "Matrícula realizada com sucesso"

    mock_cursor.execute.assert_called_once()
    mock_conn.commit.assert_called_once()
