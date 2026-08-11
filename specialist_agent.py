from langchain_openai import ChatOpenAI
from langchain.agents import create_agent

from memory.memory_manager import memory_manager
from database.materias import obter_id_materia, obter_nome_materia

from tools.topico_tools import (
    buscar_topicos,
    buscar_progresso_materia
)

from tools.conversa_tools import (
    buscar_contexto_materia
)

from tools.avaliacao_tools import (
    buscar_avaliacoes_aluno
)

from tools.finalizar_topico import (
    finalizar_topico
)

llm = ChatOpenAI(
    model="gpt-5.4-mini",
    temperature=0.3
)

PALAVRAS_CONCLUSAO = [
    "concluir tópico",
    "concluir topico",
    "finalizei",
    "terminei",
    "já terminei",
    "ja terminei",
    "completei",
    "encerrar tópico",
    "encerrar topico",
    "pode concluir"
]


def aluno_deseja_concluir(mensagem: str) -> bool:
    texto = mensagem.lower()
    return any(palavra in texto for palavra in PALAVRAS_CONCLUSAO)


def localizar_topico(mensagem: str, topicos: list):
    texto = mensagem.lower()
    for topico in topicos:
        topico_id = topico[0]
        titulo = topico[1]
        if titulo.lower() in texto:
            return (topico_id, titulo, topico)
    return None


def obter_primeiro_topico(topicos: list):
    if not topicos:
        return None
    primeiro = topicos[0]
    return (primeiro[0], primeiro[1], primeiro)


def criar_agente_especialista(
    materia_id: int,
    nome_materia: str,
    prompt_especialista: str,
    ferramentas_extras: list = None
):
    """
    Fábrica reutilizável de Agente Especialista.
    """
    ferramentas_base = [
        buscar_topicos,
        buscar_progresso_materia,
        buscar_contexto_materia,
        buscar_avaliacoes_aluno
    ]
    if ferramentas_extras:
        ferramentas_base.extend(ferramentas_extras)

    def executar(student_id: int, mensagem: str):
        contexto_materia = buscar_contexto_materia.invoke(
            {"aluno_id": student_id, "materia_id": materia_id}
        )

        progresso = buscar_progresso_materia.invoke(
            {"aluno_id": student_id, "materia_id": materia_id}
        )
        topicos = buscar_topicos.invoke({"materia_id": materia_id})
        avaliacoes = buscar_avaliacoes_aluno.invoke(
            {"aluno_id": student_id, "materia_id": materia_id}
        )
        memoria = memory_manager.buscar_memoria_materia(student_id, materia_id)

        # Checa se o aluno quer finalizar/concluir tópico
        if aluno_deseja_concluir(mensagem):
            topico = localizar_topico(mensagem, topicos)
            if topico is None:
                topico = obter_primeiro_topico(topicos)

            if topico is None:
                return "Não encontrei tópicos cadastrados para esta matéria."

            topico_id = topico[0]
            titulo = topico[1]

            resultado = finalizar_topico.invoke(
                {
                    "aluno_id": student_id,
                    "materia_id": materia_id,
                    "topico_id": topico_id,
                    "titulo_topico": titulo
                }
            )

            texto = (
                f"✅ {resultado['mensagem']}\n\n"
                f"=============================\n"
                f"AVALIAÇÃO (3 QUESTÕES)\n"
                f"=============================\n\n"
                f"{resultado['pergunta']}\n\n"
                "Por favor, responda às 3 questões na sua próxima mensagem para que a IA avaliadora possa corrigi-las."
            )

            memory_manager.adicionar_mensagem_materia(student_id, materia_id, texto)
            return texto

        contexto = f"""
Você é especialista em {nome_materia}.

=========================
CONTEXTO DA MATÉRIA
=========================
{contexto_materia}

=========================
PROGRESSO DO ALUNO
=========================
{progresso}

=========================
TÓPICOS DISPONÍVEIS
=========================
{topicos}

=========================
MEMÓRIA RECENTE DESTA MATÉRIA
=========================
{memoria}

Regras:
- Ensine apenas a matéria {nome_materia}.
- Nunca responda sobre assuntos de outras disciplinas sem direcionar adequadamente.
- Utilize as ferramentas de cálculo se for especialista em Matemática.
- Incentive o aluno a responder exercícios e concluir tópicos.
"""

        specialist_agent = create_agent(
            model=llm,
            tools=ferramentas_base,
            system_prompt=(prompt_especialista + "\n\n" + contexto)
        )

        resposta = specialist_agent.invoke(
            {"messages": [{"role": "user", "content": mensagem}]}
        )

        try:
            texto_resposta = resposta["messages"][-1].content
        except Exception:
            texto_resposta = str(resposta)

        if not texto_resposta:
            texto_resposta = "Não consegui gerar uma resposta."

        memory_manager.adicionar_mensagem_materia(student_id, materia_id, mensagem)
        memory_manager.adicionar_mensagem_materia(student_id, materia_id, texto_resposta)

        return texto_resposta

    return executar
