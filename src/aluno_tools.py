from langchain_core.tools import tool
from database.connection import get_connection
import uuid


@tool
def buscar_aluno(aluno_id: int):
    """
    Busca um aluno pelo ID.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, nome, matricula
        FROM aluno
        WHERE id = %s
        """,
        (aluno_id,)
    )

    aluno = cursor.fetchone()

    cursor.close()
    conn.close()

    return aluno



@tool
def criar_aluno(nome: str):
    """
    Cria um aluno e gera matrícula UUID.
    """

    conn = get_connection()
    cursor = conn.cursor()

    matricula = str(uuid.uuid4())[:20]

    cursor.execute(
        """
        INSERT INTO aluno(nome, matricula)
        VALUES (%s, %s)
        RETURNING id
        """,
        (nome, matricula)
    )

    aluno_id = cursor.fetchone()[0]

    conn.commit()

    cursor.close()
    conn.close()

    return {
        "student_id": aluno_id,
        "matricula": matricula
    }
