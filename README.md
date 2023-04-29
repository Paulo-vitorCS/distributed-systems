# Etapa 01: Projeto de Sistemas Distribuídos
Projeto desenvolvido para a disciplina de Sistemas Distribuídos da Universidade Federal de Uberlândia (UFU), o qual consiste em um sistemas com dois tipos de papéis, **cliente** e **administradores**. Os **Administradores** gerenciam cadastros de clientes e produtos. **Clientes** realizam pedidos de compra. As funcionalidades são expostas para estes usuários via dois tipos de aplicações distintas, o **portal de pedidos** e o **portal administrativo**, mas ambos manipulam a mesma base de dados.

#### Equipe
- [Paulo Vitor Costa Silva](https://github.com/Paulo-vitorCS)  |  [LinkedIn](https://www.linkedin.com/in/paulo-vitor-costa/)
- [Pedro Henrique Resende Ribeiro](https://github.com/pedro-hr-resende)  |  [LinkedIn](https://www.linkedin.com/in/pedro-hr-resende/)

#### Requisições da Etapa 01:

- Implementar os casos de uso usando como cache tabelas hash locais aos portais Administrador e de Pedidos.
- Certificar-se de que todas as API possam retornar erros/exceções e que estas são tratadas; explicar sua decisão de tratamento dos erros.
- Implementar testes automatizados de sucesso e falha de cada uma das operações na API.
- Documentar o esquema de dados usados nas tabelas.
- O sistema deve permitir a execução de múltiplos clientes, administradores, portais de pedido e portais administrador.
- Implementar a propagação de informação entre as diversas caches do sistema usando necessariamente pub-sub, já que a comunicação é de 1 para muitos.

#### Vídeo de apresentação da Etapa 01:
- [Apresentação | Etapa 01](https://www.youtube.com/watch?v=Pywk76ytAzM)
