# Projeto - Pytest & Deepeval

## Objetivo:

Esse projeto teve como objetivo praticar diferentes tipos de testes aplicados a um projeto com agentes de IA, usando: Pytest, Mocks, AsyncMock e DeepEval.

Para isso foram implementados testes unitários, parametrizados, assíncronos, integração AWS com client mockado e avaliação da qualidade de respostas geradas por LLM.

## Como rodar?
Primeiro, instale as dependências do projeto:

pip install pytest pytest-mock pytest-asyncio deepeval langchain langchain-openai boto3

Dependência:

- Pytest - Executar os testes.

- Pytest-mock - Disponibiliza a fixture Mocker.

- Pytest-Asyncio - Permite testar funções async.

- Deepeval - Avaliação das respostas de um LLM.

- LangChain - Execução dos agentes.

- LangChain-openai - ChatOpenAI usado pelos agentes.

- boto3 - Client da AWS/S3

## Para executar os testes:

Executar todos os testes: py -m pytest testes -v

Executar somente os testes unitários: py -m pytest testes/unit -v

Executar os testes de integração: py -m pytest testes/integration -v

Executar os testes assíncronos: py -m pytest testes/async -v

Executar as avaliações com o DeepEval: py -m pytest testes/deepeval -v

Observação:
Os testes que utilizam uma chamada a um LLM e as métricas do DeepEval precisam das credenciais necessárias configuradas no ambiente.

## O que cada arquivo demonstra 

### test_aluno_tools.py

Demonstra o uso de fixture, mock de conexão com banco de dados e
@pytest.mark.parametrize para executar o mesmo teste com diferentes casos.

### test_matricula_tools.py

Demonstra o uso de mocks para testar operações de matrícula sem acessar
o banco de dados real.

### test_topico_tools.py

Demonstra testes parametrizados das tools relacionadas aos tópicos,
utilizando uma conexão de banco mockada.

### test_agents.py

Demonstra como testar uma função que depende de uma LLM utilizando um
Fake LLM, evitando chamadas reais ao modelo durante testes unitários.

### test_specialist_agent.py

Demonstra como testar um agente que utiliza uma LLM sem realizar uma chamada
real ao modelo.

O teste utiliza `FakeListChatModel` para fornecer uma resposta controlada,
permitindo validar o comportamento do Secretary Agent sem consumir tokens
ou depender de uma API externa.

### test_aws_s3.py

Demonstra o teste da camada de integração com AWS S3 utilizando um client
boto3 mockado.

Dessa forma, é possível validar a chamada ao S3 sem acessar a AWS real.

### test_async.py

Demonstra o teste de uma função assíncrona utilizando AsyncMock.

Também utiliza parametrização para validar diferentes cenários de progresso
do aluno.

### test_llm_quality.py

Demonstra a criação de um LLMTestCase com retrieval_context e sua avaliação
utilizando as métricas:

- Answer Relevancy
- Faithfulness

### test_llm_chamada.py

Demonstra uma avaliação utilizando uma resposta realmente gerada pelo LLM.

As dependências de banco, contexto e memória são mockadas, enquanto a
chamada ao LLM é real. A resposta gerada é utilizada como actual_output
do LLMTestCase e posteriormente avaliada pelo DeepEval.

## Dúvidas encontradas durante a implementação

Durante os estudos e a implementação, as principais dúvidas foram:

- Diferença entre Mock e MagicMock.
- Entendimento de quando usar FakeLLM ou Mock.
- Entendimento de patchar onde a dependência é utilizada, e não onde necessariamente onde ela foi originalmente definida.

## Recomendações de padrões para o projeto

Para o projeto, recomenda-se: 

- Manter os testes unitários rápidos e independentes de serviços externos.
- Sempre utilizar fixtures para dependências reaproveitadas entre diferentes testes.
- Sempre utilizae o parametrize quando a mesma regra precisar ser validada com diferentes entradas.
- Utilizar o AsyncMock para dependências assíncronas.
- Separar testes unitários das avaliações de qualidade de LLM.
- Utilizar métricas adequadas ao objetivo da avaliação, como Answer Relevancy
  e Faithfulness em cenários de RAG.

# Por que testar um agente de RAG é diferente de testar uma função comum?

Quando temos uma função comum, normalmente temos uma saída previsível e esperada para uma determinada entrada, assim é possível validar o resultados das funções apenas usando asserts tradicionais.

Agora quando temos um agente de RAG, a resposta é gerada por um LLM e pode váriar entre execuções, e nem por isso a resposta está errada. Por conta disso usamos métricas de avaliação para analisar a qualidade da resposta da LLM.

Neste projeto foram utilizadas as métricas:

- Answer Relevancy: verifica se a resposta é relevante para a pergunta.
- Faithfulness: verifica se a resposta está de acordo com o contexto
  recuperado (retrieval_context).

Dessa forma, o Pytest é utilizado para validar o comportamento determinístico
do sistema, enquanto DeepEval complementa os testes avaliando a qualidade
das respostas geradas pela LLM.

## Saída esperada após executar todos os testes do projeto:

```python
collected 18 items                                                                                                                                             

testes/async/test_async.py::test_buscar_progresso_materia_async[1-6-retorno_banco0-50.0] PASSED                                                          [  5%]
testes/async/test_async.py::test_buscar_progresso_materia_async[2-4-retorno_banco1-100.0] PASSED                                                         [ 11%]
testes/async/test_async.py::test_buscar_progresso_materia_async[3-5-retorno_banco2-25.0] PASSED                                                          [ 16%]
testes/deepeval/test_llm_chamada.py::test_qualidade_resposta_real_algoritmos PASSED                                                                      [ 22%]
testes/deepeval/test_llm_quality.py::test_qualidade_resposta_algoritmo PASSED                                                                            [ 27%]
testes/integration/test_aws_s3.py::test_salvar_arquivo_s3 PASSED                                                                                         [ 33%]
testes/unit/test_aluno_tools.py::test_buscar_aluno[1-expected_result0] PASSED                                                                            [ 38%]
testes/unit/test_aluno_tools.py::test_buscar_aluno[2-expected_result1] PASSED                                                                            [ 44%]
testes/unit/test_aluno_tools.py::test_buscar_aluno[3-expected_result2] PASSED                                                                            [ 50%]
testes/unit/test_aluno_tools.py::test_buscar_aluno[4-expected_result3] PASSED                                                                            [ 55%]
testes/unit/test_matricula_tools.py::test_matricular_aluno[1-2] PASSED                                                                                   [ 61%]
testes/unit/test_matricula_tools.py::test_matricular_aluno[3-3] PASSED                                                                                   [ 66%]
testes/unit/test_matricula_tools.py::test_matricular_aluno[5-5] PASSED                                                                                   [ 72%]
testes/unit/test_secretary_agent.py::test_secretary_agent_com_fake_llm PASSED                                                                            [ 77%]
testes/unit/test_specialist_agent.py::test_agente_especialista_com_mock PASSED                                                                           [ 83%]
testes/unit/test_topico_tools.py::test_buscar_topicos[1-expected_result0] PASSED                                                                         [ 88%]
testes/unit/test_topico_tools.py::test_buscar_topicos[2-expected_result1] PASSED                                                                         [ 94%]
testes/unit/test_topico_tools.py::test_buscar_topicos[3-expected_result2] PASSED                                                                         [100%]Running teardown with pytest sessionfinish...


===================================================================== 18 passed in 24.72s =====================================================================
```





















