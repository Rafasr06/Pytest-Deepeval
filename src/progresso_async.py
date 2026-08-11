async def buscar_progresso_materia_async(
        aluno_id: int, materia_id: int, repository
):
    #async
    resultado = await repository.buscar_progresso(
        aluno_id,
        materia_id
    )

    if not resultado:
        return None

    _, nome, total, concluidos = resultado

    porcentagem = (
        round((concluidos / total) * 100, 2)
        if total
        else 0
    )

    return {
        "materia_id": materia_id,
        "materia": nome,
        "total_topicos": total,
        "concluidos": concluidos,
        "porcentagem": porcentagem
    }

