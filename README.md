# SmartAI Assistant

Assistente com IA generativa para transformar anotações em resumos,
listas de tarefas e planos de ação.

## Funcionalidades

- Resumir textos.
- Extrair tarefas, responsáveis e prazos informados.
- Propor planos de ação.
- Salvar e consultar o histórico de solicitações.
- Acessar o assistente por uma interface no navegador.

## Tecnologias

- Python e programação orientada a objetos.
- FastAPI para a API REST.
- Google Gen AI SDK para integração com Gemini.
- TinyDB como banco NoSQL orientado a documentos.
- HTML, CSS e JavaScript para a interface.
- Git para versionamento.

## Arquitetura

O projeto separa as responsabilidades em camadas:

- `api`: recebe requisições HTTP e retorna respostas.
- `schemas`: define e valida os dados de entrada.
- `services`: coordena a geração e o armazenamento dos resultados.
- `integrations`: comunica-se com o provedor de IA.
- `repositories`: grava e consulta o histórico.
- `static`: contém os arquivos da interface.
- `main.py`: configura a aplicação e conecta as rotas.

Fluxo principal:

Interface → API → Serviço → Gemini → Repositório → TinyDB

## Como executar no Windows

Pré-requisitos: Python 3.13 e uma chave de API do Gemini com acesso
ao modelo configurado.

Execute os comandos na pasta principal do projeto.

1. Crie um ambiente virtual:

```powershell
python -m venv .venv
```

2. Instale as dependências:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

3. Copie `.env.example` para `.env`:

```powershell
Copy-Item .env.example .env
```

Se já possui um `.env` configurado, mantenha-o.

4. Preencha `GEMINI_API_KEY` no `.env` com sua chave.
   Ajuste `GEMINI_MODEL` se necessário.

5. Inicie o servidor:

```powershell
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8001
```

6. Acesse:

- Interface: http://127.0.0.1:8001/interface
- Documentação da API: http://127.0.0.1:8001/docs

Mantenha o terminal do servidor aberto durante o uso.
Para parar, pressione Ctrl + C.

## Rotas

| Método | Rota | Finalidade |
|---|---|---|
| GET | `/` | Consultar mensagem inicial |
| POST | `/assistente` | Processar texto com IA |
| GET | `/historico` | Consultar registros salvos |
| GET | `/interface` | Abrir a interface |

Exemplo de corpo para POST /assistente:

```json
{
  "texto": "Ana deve revisar o cadastro até sexta-feira.",
  "acao": "extrair_tarefas"
}
```

Ações aceitas: `resumir`, `extrair_tarefas` e `plano_de_acao`.
O texto deve conter de 10 a 10.000 caracteres.

## Armazenamento e configuração

O histórico é criado automaticamente em `data/historico.json`.

O arquivo `.env` e a pasta `data` ficam fora do versionamento.
Nunca inclua chaves reais no código ou no `.env.example`.

## Limitações

- Requer internet, uma chave válida e cota disponível na API.
- O texto enviado é encaminhado ao provedor Gemini.
- Respostas de IA podem conter erros e devem ser revisadas.
- A aplicação não possui autenticação e foi criada para uso local.
- O TinyDB está configurado para um único processo de servidor.