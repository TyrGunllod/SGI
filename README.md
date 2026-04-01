# SGI
Sistema de Gestão Integrado - Um Hub de aplicativos modulares como em um ERP

🚀 MiniERP - Backend (API)Este é o núcleo do MiniERP, desenvolvido com FastAPI e PostgreSQL. Ele funciona como o "cérebro" do sistema, gerenciando o Hub de módulos, autenticação e a persistência de dados.🛠️ Tecnologias PrincipaisLinguagem: Python 3.10+Framework: FastAPIBanco de Dados: PostgreSQLORM: SQLAlchemy ou SQLModelServidor: Uvicorn🏃 Como Rodar o Projeto LocalmenteSiga o passo a passo abaixo para configurar o ambiente de desenvolvimento:1. Clonar o RepositórioBashgit clone https://github.com/SEU_USUARIO/NOME_DO_REPOSITORIO.git
cd NOME_DO_REPOSITORIO
2. Configurar o Ambiente Virtual (Venv)O uso de um ambiente virtual é essencial para isolar as dependências e evitar conflitos.No Windows:Bashpython -m venv venv
.\venv\Scripts\activate
No Linux/macOS:Bashpython3 -m venv venv
source venv/bin/activate
3. Instalar as DependênciasCertifique-se de que o driver do PostgreSQL (psycopg2-binary) está instalado para a comunicação com o banco.Bashpip install -r requirements.txt
4. Configurar as Variáveis de AmbienteCrie um arquivo chamado .env na raiz da pasta do backend e adicione sua string de conexão com o PostgreSQL:Code snippetDATABASE_URL=postgresql://USUARIO:SENHA@localhost:5432/NOME_DO_BANCO
5. Iniciar o ServidorBashuvicorn main:app --reload
O servidor estará disponível em: http://localhost:8000📑 Documentação da APIO FastAPI gera documentação interativa automaticamente. Com o servidor rodando, você pode testar os endpoints em:Swagger UI: http://localhost:8000/docsReDoc: http://localhost:8000/redoc🔌 Endpoints de Integração (Hub)Estes são os principais endpoints consumidos pelo Frontend para montar o Hub dinâmico:MétodoEndpointDescriçãoGET/appsLista todos os módulos disponíveis para a SidebarGET/healthVerifica o status da API e a saúde da conexão com o Banco🗄️ Estrutura Sugerida do ProjetoPara manter a escalabilidade conforme novos módulos forem criados:Plaintextbackend/
├── main.py             # Ponto de entrada (Configuração do FastAPI e CORS)
├── database.py         # Configuração da Session e Engine do Postgres
├── models/             # Definição das tabelas (User, App, Venda, etc.)
├── routes/             # Arquivos de rotas (Router) para cada módulo
├── schemas/            # Modelos Pydantic para validação de entrada/saída
└── requirements.txt    # Dependências do projeto (pip freeze)