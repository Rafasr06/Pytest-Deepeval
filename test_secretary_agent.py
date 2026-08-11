from langchain_core.language_models.fake_chat_models import FakeListChatModel

from agents.secretary_agent import (
    criar_secretary_agent,
    executar_secretario
)


class FakeChatModelComTools(FakeListChatModel):

    def bind_tools(self, tools, **kwargs):
        return self


def test_secretary_agent_com_fake_llm():

    fake_llm = FakeChatModelComTools(
        responses=[
            "Sua matrícula foi realizada com sucesso."
        ]
    )

    agent_fake = criar_secretary_agent(
        model=fake_llm
    )

    resultado = executar_secretario(
        student_id=1,
        mensagem="Quero me matricular em Python.",
        agent=agent_fake
    )

    assert resultado == "Sua matrícula foi realizada com sucesso."