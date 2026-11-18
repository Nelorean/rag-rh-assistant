# RAG RH Assistant

Assistente para consultar políticas internas de uma empresa fictícia, como benefícios, jornada de trabalho e home office. O projeto usa RAG para recuperar trechos de um PDF e gerar respostas em português com o Gemini.

O manual da Senda Aurora Tecnologia incluído no projeto contém dados fictícios para estudo e demonstração.

## Tecnologias

- Python 3.13
- Streamlit para a interface de chat
- LangChain para conectar a busca ao modelo
- Gemini para respostas e embeddings
- FAISS para a busca vetorial
- PyPDF e python-dotenv

## Como executar

Você precisa de Python instalado e de uma chave da API do Gemini, disponível no [Google AI Studio](https://aistudio.google.com/apikey).

Na pasta do projeto, crie um ambiente virtual e instale as dependências pelo PowerShell.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Abra o arquivo `.env` e preencha sua chave.

```dotenv
GOOGLE_API_KEY=sua_chave_aqui
```

Inicie a aplicação na mesma pasta do arquivo `politica_rh.pdf`.

```powershell
.\.venv\Scripts\python.exe -m streamlit run app_basic.py
```

Acesse o endereço local mostrado no terminal e envie uma pergunta no chat.

## Como funciona

O app lê `politica_rh.pdf`, divide o texto em trechos e gera os embeddings com `gemini-embedding-2`. O FAISS encontra os trechos relacionados à pergunta e o `gemini-3.5-flash-lite` recebe esse contexto para gerar a resposta.

O índice fica em memória com `st.cache_resource` e é compartilhado entre as sessões enquanto o processo estiver ativo. Ao reiniciar o app ou limpar o cache, ele será criado novamente.

## Exemplos de perguntas

- Quantos dias por semana posso trabalhar em home office?
- Qual é o valor do vale alimentação?
- Como solicito férias?

