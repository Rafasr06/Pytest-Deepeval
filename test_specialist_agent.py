from agents.specialist_agent import criar_agente_especialista


def test_agente_especialista_com_mock(mocker):
    # Mock da tool buscar_contexto_materia
    mock_contexto = mocker.MagicMock()
    mock_contexto.invoke.return_value = "Contexto anterior da matéria"

    mocker.patch(
        "agents.specialist_agent.buscar_contexto_materia",
        mock_contexto
    )

    # Mock da tool buscar_progresso_materia
    mock_progresso = mocker.MagicMock()
    mock_progresso.invoke.return_value = {
        "porcentagem": 50
    }

    mocker.patch(
        "agents.specialist_agent.buscar_progresso_materia",
        mock_progresso
    )

    # Mock da tool buscar_topicos
    mock_topicos = mocker.MagicMock()
    mock_topicos.invoke.return_value = [
        (1, "Introdução", "Conceitos iniciais", 1)
    ]

    mocker.patch(
        "agents.specialist_agent.buscar_topicos",
        mock_topicos
    )

    # Mock da tool buscar_avaliacoes_aluno
    mock_avaliacoes = mocker.MagicMock()
    mock_avaliacoes.invoke.return_value = []

    mocker.patch(
        "agents.specialist_agent.buscar_avaliacoes_aluno",
        mock_avaliacoes
    )

    # Mock da memória
    mocker.patch(
        "agents.specialist_agent.memory_manager.buscar_memoria_materia",
        return_value=[]
    )

    mock_adicionar_memoria = mocker.patch(
        "agents.specialist_agent.memory_manager.adicionar_mensagem_materia"
    )

    # Mock do agente que representa a parte do LLM
    mock_agent = mocker.MagicMock()

    mock_message = mocker.MagicMock()
    mock_message.content = (
        "Algoritmos são uma sequência de passos "
        "para resolver um problema."
    )

    mock_agent.invoke.return_value = {
        "messages": [mock_message]
    }

    mock_create_agent = mocker.patch(
        "agents.specialist_agent.create_agent",
        return_value=mock_agent
    )

    # Cria o especialista
    executar = criar_agente_especialista(
        materia_id=6,
        nome_materia="Algoritmos",
        prompt_especialista="Você é especialista em Algoritmos."
    )

    # Executa o agente
    resultado = executar(
        student_id=1,
        mensagem="O que é um algoritmo?"
    )

    # Valida retorno
    assert resultado == (
        "Algoritmos são uma sequência de passos "
        "para resolver um problema."
    )

    # Valida chamadas principais
    mock_create_agent.assert_called_once()
    mock_agent.invoke.assert_called_once()

    assert mock_adicionar_memoria.call_count == 2