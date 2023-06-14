# **Implementação usando gRPC e Mosquitto**

A primeira etapa do projeto da disciplina de sistemas distribuídos consiste em implementar uma aplicação cliente-servidor na qual são utilizados gRPC e Mosquitto.

## **Criação do projeto e download pacotes**

Para criar o projeto, utilizou-se a IDE Pycharm. Depois, foram instalados os seguintes pacotes:

```bash
pip install protobuf
pip install grpcio
pip install grpcio-tools
pip install paho-mqtt
```

## **Criação dos protocols buffers**

Após a instalação dos pacotes, criou-se o diretório `protos`. No diretório foi criado o arquivo `services.proto` contendo todas assinaturas utilizadas pelos clientes e pelos portais administradores e de pedidos. Em seguida, com o terminal aberto no diretório `homework-001`, executou-se o seguindo comando:

```bash
python -m grpc_tools.protoc -I protos --python_out=. --pyi_out=. --grpc_python_out=. protos/services.proto
```

Ao finalizar o comando, tem-se os seguintes arquivos no diretório: `services_pb2.py`, `services_pb2.pyi` e `services_pb2_grpc.py`.

## **Implementação do admin server**

O portal administrador foi implementado da seguinte forma:

- Possui a implementação das seguintes funções para clientes: `CreateClient`, `RetrieveClient`, `UpdateClient` e `DeleteClient`.
- Possui a implementação das seguintes funções para produtos: `CreateProduct`, `RetrieveProduct`, `UpdateProduct` e `DeleteProduct`.
- É utilizado um módulo chamado `database` que contém todas as verificações necessárias para executar as funções descritas anteriormente.

## **Exemplo de uma função do portal administrador**

Para exemplificar a implementação do portal administrador, considere a função `CreateClient` mostrada abaixo.

``` Python
    def CreateClient(self, request: services_pb2.Client, context):
        try:
            database.create_client(request.CID, request.data)
            data = request.data
            data = json.loads(data)
            message = {request.CID: data}
            message = json.dumps(message)
            message = 'create_client;' + message
            self.mqtt_client.client.publish('distributed_systems', message)
            return services_pb2.Reply(error=0, description=f'The CID:{request.CID} was added successfully')
        except Exception as error:
            return services_pb2.Reply(error=1, description=str(error))
```

A função recebe como parâmetro um cliente, especificado no arquivo `services.proto`. O cliente possui os campos `CID` e `data`. As informações são passadas para a função `create_client`, presente no módulo `database`. A função citada é mostrada a seguir.

``` Python
def create_client(cid, data):
    if cid not in clients:
        clients.update({cid: data})
        print(clients)
    else:
        raise Exception('The database already contains the client')
```

Como pode ser visto, caso o `cid` informado pelo usuário não existir, as informações são adicionadas no dicionário `clients`, que é a estrutura escolhida para armazenar os dados durante a execução. As demais funções citadas anteriormente foram implementadas seguindo uma lógica semelhante.

## **Estrutura de dados para armazenar as informações**

Conforme solicitado no roteiro do projeto, a estrutura de dados utilizada no projeto são dicionários. Esta estrutura armazena dados utilizando chave e valor, onde as chaves são o `CID` (Client ID), `PID` (Product ID) e `OID` (Order ID). Exemplos de utilização são mostrados a seguir.

### **Dicionário para clientes**

```JSON
{
  "CID": "100",
  "name": "Pedro"
}
```

### **Dicionário para produtos**

```JSON
{
  "PID": "200",
  "name": "product-001",
  "quantity": "40",
  "price": "2.50"
}
```

### **Dicionário para pedidos**

```JSON
{
  "OID": "300",
  "CID": "100",
  "products": [
    {
      "PID": "100",
      "quantity": "30",
      "price": "2.50"
    },
    {
      "PID": "101",
      "quantity": "10",
      "price": "1.50"
    }
  ]
}
```
