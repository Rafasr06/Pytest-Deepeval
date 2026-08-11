from langchain_core.tools import tool
from database.connection import get_connection


# ==========================================================
# BUSCAR TÓPICOS DA MATÉRIA
# ==========================================================

@tool
def buscar_topicos(materia_id: int):
    """
    Retorna todos os tópicos de uma matéria.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            id,
            titulo,
            descricao,
            ordem

        FROM topico

        WHERE materia_id = %s

        ORDER BY ordem
        """,
        (materia_id,)
    )

    dados = cursor.fetchall()

    cursor.close()
    conn.close()

    return dados


# ==========================================================
# VERIFICAR SE O TÓPICO JÁ FOI CONCLUÍDO
# ==========================================================

@tool
def verificar_topico_concluido(
    aluno_id: int,
    topico_id: int
):
    """
    Verifica se o aluno já concluiu o tópico.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT 1

        FROM topico_aluno

        WHERE

        aluno_id = %s

        AND

        topico_id = %s
        """,
        (
            aluno_id,
            topico_id
        )
    )

    resultado = cursor.fetchone()

    cursor.close()
    conn.close()

    return resultado is not None


# ==========================================================
# CONCLUIR TÓPICO
# ==========================================================

@tool
def concluir_topico(
    aluno_id: int,
    topico_id: int
):
    """
    Marca um tópico como concluído.
    Um tópico não pode ser concluído duas vezes.
    """

    if verificar_topico_concluido.invoke(
        {
            "aluno_id": aluno_id,
            "topico_id": topico_id
        }
    ):
        return "Este tópico já foi concluído."

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO topico_aluno (
            aluno_id,
            topico_id
        )

        VALUES (%s,%s)
        """,
        (
            aluno_id,
            topico_id
        )
    )

    conn.commit()

    cursor.close()
    conn.close()

    return "Tópico concluído com sucesso."


# ==========================================================
# BUSCAR PROGRESSO GERAL
# ==========================================================

@tool
def buscar_progresso(aluno_id: int):
    """
    Retorna o progresso do aluno em todas as matérias.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT

            materia.id,

            materia.nome,

            COUNT(topico.id) AS total,

            COUNT(topico_aluno.id) AS concluidos

        FROM matricula

        JOIN materia

            ON materia.id = matricula.materia_id

        JOIN topico

            ON topico.materia_id = materia.id

        LEFT JOIN topico_aluno

            ON topico_aluno.topico_id = topico.id

            AND topico_aluno.aluno_id = %s

        WHERE

        matricula.aluno_id = %s

        GROUP BY

        materia.id,

        materia.nome

        ORDER BY

        materia.nome
        """,
        (
            aluno_id,
            aluno_id
        )
    )

    progresso = []

    for materia_id, nome, total, concluidos in cursor.fetchall():

        porcentagem = 0

        if total > 0:
            porcentagem = round(
                (concluidos / total) * 100,
                2
            )

        progresso.append(
            {
                "materia_id": materia_id,
                "materia": nome,
                "total_topicos": total,
                "concluidos": concluidos,
                "porcentagem": porcentagem
            }
        )

    cursor.close()
    conn.close()

    return progresso


@tool
def buscar_progresso_materia(aluno_id: int, materia_id: int):
    """Retorna apenas o progresso do aluno na matéria informada."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT
            materia.id,
            materia.nome,
            COUNT(topico.id) AS total,
            COUNT(topico_aluno.id) AS concluidos
        FROM materia
        LEFT JOIN topico
            ON topico.materia_id = materia.id
        LEFT JOIN topico_aluno
            ON topico_aluno.topico_id = topico.id
            AND topico_aluno.aluno_id = %s
        WHERE materia.id = %s
        GROUP BY materia.id, materia.nome
        """,
        (aluno_id, materia_id)
    )

    resultado = cursor.fetchone()
    cursor.close()
    conn.close()

    if not resultado:
        return None

    _, nome, total, concluidos = resultado
    porcentagem = round((concluidos / total) * 100, 2) if total else 0
    return {
        "materia_id": materia_id,
        "materia": nome,
        "total_topicos": total,
        "concluidos": concluidos,
        "porcentagem": porcentagem,
    }


# ==========================================================
# CONTAR TÓPICOS CONCLUÍDOS DA MATÉRIA
# ==========================================================

@tool
def contar_topicos_concluidos(
    aluno_id: int,
    materia_id: int
):
    """
    Conta quantos tópicos foram concluídos
    em uma matéria específica.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT COUNT(*)

        FROM topico_aluno ta

        JOIN topico t

            ON t.id = ta.topico_id

        WHERE

        ta.aluno_id = %s

        AND

        t.materia_id = %s
        """,
        (
            aluno_id,
            materia_id
        )
    )

    total = cursor.fetchone()[0]

    cursor.close()
    conn.close()

    return total


# ==========================================================
# LISTAR TÓPICOS CONCLUÍDOS
# ==========================================================

@tool
def listar_topicos_concluidos(
    aluno_id: int,
    materia_id: int
):
    """
    Lista os tópicos concluídos pelo aluno.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT

            t.id,

            t.titulo

        FROM topico_aluno ta

        JOIN topico t

            ON t.id = ta.topico_id

        WHERE

        ta.aluno_id = %s

        AND

        t.materia_id = %s

        ORDER BY t.ordem
        """,
        (
            aluno_id,
            materia_id
        )
    )

    dados = cursor.fetchall()

    cursor.close()
    conn.close()

    return dados


# ==========================================================
# PRÓXIMO TÓPICO
# ==========================================================

@tool
def buscar_proximo_topico(
    aluno_id: int,
    materia_id: int
):
    """
    Retorna o primeiro tópico ainda não concluído.
    """

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT

            t.id,

            t.titulo,

            t.descricao

        FROM topico t

        WHERE

        t.materia_id = %s

        AND

        t.id NOT IN (

            SELECT topico_id

            FROM topico_aluno

            WHERE aluno_id = %s

        )

        ORDER BY t.ordem

        LIMIT 1
        """,
        (
            materia_id,
            aluno_id
        )
    )

    resultado = cursor.fetchone()

    cursor.close()
    conn.close()

    return resultado
