# Teste para a Festzap


Um pequeno servidor de Chat usando WebSockets.

## Executando

- Instale as dependências usando o pip

```
pip install -r requirements.txt
```

- Execute o Redis usando o Docker para o gerenciamento de Channel Layers

```
docker run -p 6379:6379 -d redis:5
```

- Inicie o servidor

```
python manage.py runserver
```

## Usando o servidor

- Você pode criar um usuário executando um `POST` em `/api/users/` com o seguinte corpo:

```
{
	"username": "username",
	"password": "password",
	"first_name": "first name"
}
```

- Para fazer o login, execute um `POST` em `/api/token/` com o seguinte corpo:

```
{
	"username": "username",
	"password": "password"
}
```

- Ele irá retornar o seguinte corpo:

```
{
  "refresh": "token",
  "access": "token"
}
```

- Use o token de access para usar as outras rotas da API e se conectar ao websocket

- Para usar o token em uma rota da API, coloque um Cabeçalho na requisição chamado `Authorization` com o padrão:

```
Bearer <token>
```

- Para usar em um WebSocket, coloque um Query Param chamado `token` no final da URL do WebSocket

## Conectar ao WebSocket

- Para conectar ao WebSocket dos chats, use a URL:
`ws://<host:porta>/ws/chat/<chat_id>/?token=<token>`

- Para criar um chat, realize um post na URL `/api/chats/` com o seguinte corpo:
```
{
	"participants": [...]
}
```

Onde `participants` é um array dos IDs de cada usuário que participa daquele chat

- Para enviar uma mensagem, realize um post na URL `/api/chats/<chat_id>/messages/` com o seguinte corpo:
```
{
	"text_content": "text"
}
```
