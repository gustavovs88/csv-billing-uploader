# Desafio full-stack Kanastra

## Rodando o projeto

Para rodar o projeto é necessário ter o docker compose devidamente instalado e nenhuma das portas expostas pelos containeres devem estar ocupadas.
portas:

- Servidor: 8000
- Cliente : 8888
- Banco de dados: 5432

1. No terminal rodar o comando:

```
docker-compose up
```

2. Acessar aplicação na url `http://localhost:8888/`
3. Acessar a documentação da api na url `http://localhost:8000/docs`

## Detalhes backend

Para este projeto foi usado o framework fastapi devido sua versatilidade e desempenho.
O banco de dados selecionado foi o PostgreSQL também por sua versatilidade.

O projeto foi separado em três camadas com suas devidas responsabilidades

- Routers -> Provê as rotas, de acordo com o domínio. Neste caso o domínio de cobranças, denominado billings.

- Services -> Provê as lógicas e regras de negócio, de acordo com o domínio

- Repositories -> Provê encapsulamento das lógicas de registro/acesso a dados externos, como operações em banco de dados.

Além disto temos uma pasta de dependências -> dependencies, onde ficam encapsuladas as lógicas de dependências do projeto. Neste caso uma abstração da conexão com o banco de dados foi incluída.

### Visão de alto nível do projeto

Foi criada uma estrutura de dados para permitir o processamento de todas as linhas dos arquivos recebidos do frontend. Incluindo, além dos dados presentes no csv, dados de status do processamento e de criação/remoção das cobranças.

Foram criadas 2 rotas. Uma para receber o arquivo no formato .csv e outra para retornar todos os registros de envio destes arquivos.

Ao receber o arquivo csv pro meio da rota `POST /billings/csv/upload` é realizada a leitura do arquivo csv e todas as linhas do mesmo são salvas no banco de dados. Para otimizar este processo todos os registros são inseridos de uma vez, por meio do método `COPY`. Além disto usamos removemos temporariamente as dependências de chaves externas (foreign keys -fk) para atingir um desempenho ainda maior na escrita do arquivo no banco de dados (ref: https://www.postgresql.org/docs/current/populate.html#POPULATE-RM-FKEYS).

Após inclusão dos registros no banco de dados, a rota retorna o status 200 e o processamento das cobranças inicia-se automaticamente em segundo plano em uma nova thread.

Além disto, foi implementado um cron job simples para verificar cobranças pendentes e processa-las, também em uma nova thread, caso o processamento automático não ocorra devidamente.
Tanto o cron job quanto o processamento automático não devem ocorrer em paralelo para evitar picos muito grandes de processamento e memória e concorrência.

Como existe a possibilidade de termos muitos registros pendentes, estes são retornados através de um stream das cobranças do banco de dados, para evitar alto consumo de memória e interrupção do serviço. Isso é feito iterando sobre o `named_cursor`, que funciona como um server side cursor (https://www.psycopg.org/docs/usage.html#server-side-cursors).

A geração do boleto e envio do e-mail aos sacado foi somente simulada, tendo o status da cobrança atualizado como `SENT` (enviado). Entendo que uma lógica orientada a eventos faria sentido neste caso. Por ex.: Esta api envia os dados de cobrança via mensageria. Um serviço exclusivo para emissão dos boletos consome estas mensagens e gera os boletos, salvando-os em um serviço de armazenamento de arquivos em nuvem. Ao finalizar, este serviço enviaria uma mensagem ao serviço de notificações com o caminho para o arquivo de boleto gerado + dados necessários para o email. O serviço de notificações envia o email para o sacado e no fim retorna uma mensagem que seria consumida por este serviço para atualizar o status da cobrança.

## Detalhes frontend

A interface do usuário ficou simples, com um botão para inserir o arquivo csv. Ao inserir o arquivo, alguns dados deste são apresentados, bem como o botão de submeter o arquivo.
Após sucesso na submissão do arquivo, é apresentada uma tabela contendo a lista de arquivos submetidos, com dados do status destes dentre outras informações.
Com a apresentação da tabela, também é apresentado um botão para atualizar a lista de arquivos, de modo que o usuário possa acompanhar o processamento dos arquivos enviados.

A principal característica do frontend é o uso da context api do react para controlar os estados dos arquivos submetidos e inseridos no input.
Os estados são atualizados por meio de `actions` pré-definidas:

- SET_FILE - atualoza arquivo inserido no input
- UPLOAD_FILE - atualiza lista de arquivos submetidos após submissão de um arquivo
- GET_SUBMITTED_FILES - atualiza lista de arquivos submetidos após clicar no botão de atualizar lista
