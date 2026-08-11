from deepeval import evaluate
from deepeval.test_case import LLMTestCase
from deepeval.metrics import (
    AnswerRelevancyMetric,
    FaithfulnessMetric
)
from deepeval.evaluate import CacheConfig

from agents.algoritmos_agent import executar_algoritmos_agent


def test_qualidade_resposta_real_algoritmos(mocker):

    # Mock das dependências

    mock_contexto = mocker.MagicMock()

    mock_contexto.invoke.return_value = (
        "Algoritmo é uma sequência finita e ordenada "
        "de passos para resolver um problema."
    )

    mocker.patch(
        "agents.specialist_agent.buscar_contexto_materia",
        mock_contexto
    )


    mock_progresso = mocker.MagicMock()

    mock_progresso.invoke.return_value = {
        "materia": "Algoritmos",
        "porcentagem": 50
    }

    mocker.patch(
        "agents.specialist_agent.buscar_progresso_materia",
        mock_progresso
    )


    mock_topicos = mocker.MagicMock()

    mock_topicos.invoke.return_value = [
        (
            1,
            "Introdução a Algoritmos",
            (
                "Algoritmo é uma sequência finita e ordenada "
                "de instruções utilizada para resolver um problema."
            ),
            1
        )
    ]

    mocker.patch(
        "agents.specialist_agent.buscar_topicos",
        mock_topicos
    )


    mock_avaliacoes = mocker.MagicMock()

    mock_avaliacoes.invoke.return_value = []

    mocker.patch(
        "agents.specialist_agent.buscar_avaliacoes_aluno",
        mock_avaliacoes
    )


    # Mock da Memória 

    mocker.patch(
        "agents.specialist_agent.memory_manager.buscar_memoria_materia",
        return_value=[]
    )

    mocker.patch(
        "agents.specialist_agent.memory_manager.adicionar_mensagem_materia"
    )


    # Chamada ao LLM

    pergunta = "O que é um algoritmo?"

    actual_output = executar_algoritmos_agent(
        student_id=1,
        mensagem=pergunta
    )


    # Contexto da avaliação(retrieval context)

    retrieval_context = [
        (
            "Algoritmo é uma sequência finita e ordenada "
            "de instruções utilizada para resolver um problema."
        )
    ]


    # Teste do LLM
    test_case = LLMTestCase(
        input=pergunta,
        actual_output=actual_output,
        retrieval_context=retrieval_context
    )


    # Métricas Deepeval

    answer_relevancy = AnswerRelevancyMetric(
        threshold=0.7,
        include_reason=True
    )

    faithfulness = FaithfulnessMetric(
        threshold=0.7,
        include_reason=True
    )


    # Avaliação

    evaluate(
        test_cases=[test_case],
        metrics=[
            answer_relevancy,
            faithfulness
        ],
        cache_config=CacheConfig(
            use_cache=False,
            write_cache=False
        )
    )
