<h1 align="center"> Gerenciador de Projetos e Tarefas </h1>

<p>
  Este é um projeto para gerenciar tarefas dentro de diferentes projetos. 
  Ele oferece funcionalidades de criação, edição, visualização e marcação de projetos e tarefas como concluídas. 
  Além disso, permite adicionar fotos de capa aos projetos e visualizar uma lista das tarefas divididas em concluídas e pendentes.
</p>

<h2>
  Como rodar o projeto
</h2>

- Instale as dependências no VENV:
```
$ pip install -r requirements.txt
```

- No arquivo .env adicione o Usuário, Senha e Database do PostgreSQL:

```
DATABASE_URL= postgresql://SeuUsuário:SuaSenha@localhost:5432/SeuBanco
```

- Inicie o Banco com::
```
$ flask db init
$ flask db migrate -m "Criação das tabelas"
$ flask db upgrade
```

- Rode o main.py e acesse o localhost!

