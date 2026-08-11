from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from database.materias import MATERIAS_MAP, obter_id_materia

from tools.aluno_tools import (
    buscar_aluno,
    criar_aluno
)

from tools.matricula_tools import (
    matricular_aluno,
    remover_matricula,
    listar_materias_aluno
)

from tools.topico_tools import (
    buscar_progresso
)

from tools.avaliacao_tools import (
    buscar_avaliacoes_aluno,
    buscar_todas_avaliacoes_aluno
)


secretary_tools = [
    buscar_aluno,
    criar_aluno,
    matricular_aluno,
    remover_matricula,
    listar_materias_aluno,
    buscar_progresso,
    buscar_avaliacoes_aluno,
    buscar_todas_avaliacoes_aluno
]


secretary_prompt = """
Você é o Agente Secretário.
Sua função é realizar tarefas administrativas
(cadastro de alunos, matrículas, relatórios de notas e progresso).

Você NÃO ensina conteúdos de matérias nem corrige exercícios.

Matérias disponíveis e seus IDs:
1 - Matemática
2 - História
3 - Ciências
4 - Python
5 - Banco de Dados
6 - Algoritmos
7 - Engenharia de Software

Sempre utilize as ferramentas disponíveis para buscar e registrar dados reais do aluno.

O marcador [aluno_id=N] identifica o aluno da sessão atual.
Para matrícula, remoção de matrícula, progresso e notas,
use obrigatoriamente esse ID.

Se cadastrar um novo aluno, informe claramente o novo student_id retornado
e oriente o usuário a iniciar ou trocar para a sessão desse aluno.
"""


def criar_secretary_agent(model=None):
    """
    Cria o agente secretário.

    Em produção utiliza ChatOpenAI.
    Nos testes podemos passar um modelo fake.
    """

    if model is None:
        model = ChatOpenAI(
            model="gpt-5.4-mini",
            temperature=0
        )

    return create_agent(
        model=model,
        tools=secretary_tools,
        system_prompt=secretary_prompt
    )


# Agente utilizado normalmente pela aplicação
secretary_agent = criar_secretary_agent()


def identificar_materia(texto: str) -> int:
    return obter_id_materia(texto)


def executar_secretario(
    student_id: int,
    mensagem: str,
    agent=None
) -> str:
    """
    Executa o agente secretário.

    Se nenhum agente for informado,
    utiliza o agente real da aplicação.

    Durante os testes podemos passar
    um agente criado com FakeListChatModel.
    """

    if agent is None:
        agent = secretary_agent

    resposta = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": (
                        f"[aluno_id={student_id}] "
                        f"{mensagem}"
                    )
                }
            ]
        }
    )

    try:
        texto = resposta["messages"][-1].content

    except Exception:
        texto = str(resposta)

    return texto or "A solicitação foi processada pelo Secretário."
