from langchain_core.tools import tool
from database.connection import get_connection


@tool
def matricular_aluno(aluno_id: int, materia_id: int):
    """Matricula um aluno em uma matéria."""

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO matricula (aluno_id, materia_id)
        VALUES (%s, %s)
        ON CONFLICT DO NOTHING
        """,
        (aluno_id, materia_id)
    )

    conn.commit()
    cursor.close()
    conn.close()

    return "Matrícula realizada com sucesso"


@tool
def remover_matricula(aluno_id: int, materia_id: int):
    """Remove matrícula do aluno."""

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM matricula
        WHERE aluno_id = %s AND materia_id = %s
        """,
        (aluno_id, materia_id)
    )

    conn.commit()
    cursor.close()
    conn.close()

    return "Matrícula removida"


@tool
def listar_materias_aluno(aluno_id: int):
    """Lista matérias do aluno."""

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT materia.id, materia.nome
        FROM materia
        JOIN matricula ON materia.id = matricula.materia_id
        WHERE matricula.aluno_id = %s
        """,
        (aluno_id,)
    )

    dados = cursor.fetchall()

    cursor.close()
    conn.close()

    return dados


@tool
def verificar_matricula(aluno_id: int, materia_id: int):
    """Verifica se aluno está matriculado."""

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT 1
        FROM matricula
        WHERE aluno_id = %s AND materia_id = %s
        """,
        (aluno_id, materia_id)
    )

    existe = cursor.fetchone()

    cursor.close()
    conn.close()

    return existe is not None
