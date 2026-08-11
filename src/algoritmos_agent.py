from agents.specialist_agent import criar_agente_especialista
from database.materias import MATERIAS_MAP

ALGORITMOS_PROMPT = """
Você é o Agente Especialista em Algoritmos.
Sua responsabilidade é ensinar lógica de programação, estruturas de dados, fluxogramas e pseudocódigo.
"""

executar_algoritmos_agent = criar_agente_especialista(
    materia_id=MATERIAS_MAP["algoritmos"],
    nome_materia="Algoritmos",
    prompt_especialista=ALGORITMOS_PROMPT
)
