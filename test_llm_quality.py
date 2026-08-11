from deepeval import evaluate
from deepeval.test_case import LLMTestCase
from deepeval.metrics import (
    AnswerRelevancyMetric,
    FaithfulnessMetric
)


def test_qualidade_resposta_algoritmo():

    test_case = LLMTestCase(
        input="O que é um algoritmo?",
        actual_output=(
            "Um algoritmo é uma sequência ordenada "
            "de passos utilizados para resolver um problema."
        ),
        retrieval_context=[
            (
                "Algoritmo é uma sequência finita e ordenada "
                "de instruções utilizada para resolver um problema."
            )
        ]
    )

    answer_relevancy_metric = AnswerRelevancyMetric(
        threshold=0.7,
        include_reason=True
    )

    faithfulness_metric = FaithfulnessMetric(
        threshold=0.7,
        include_reason=True
    )

    evaluate(
        test_cases=[test_case],
        metrics=[
            answer_relevancy_metric,
            faithfulness_metric
        ]
    )