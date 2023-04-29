# Etapa 1 - Implementação usando gRPC e Mosquitto

<br>

<p align="justify">
Para criar o projeto, utilizou-se a IDE Pycharm. Depois, foram instalados os seguintes pacotes do Python:
</p>

<br>

```bash
pip install protobuf
pip install grpcio
pip install grpcio-tools
pip install paho-mqtt
```

<br>

## Criação dos protocols buffers

<br>

<p align="justify">
Após a instalação dos pacotes, criou-se o diretório <kbd>protos</kbd>. No diretório foi criado o arquivo <kbd>services.proto</kbd> contendo todas assinaturas utilizadas pelos clientes e pelos portais administradores e de pedidos. Em seguida, com o terminal aberto no diretório <kbd>homework-001</kbd>, executou-se o seguindo comando:
</p>

<br>

```bash
python -m grpc_tools.protoc -I protos --python_out=. --pyi_out=. --grpc_python_out=. protos/services.proto
```

<br>

<p align="justify">
Ao finalizar o comando, tem-se os seguintes arquivos no diretório: <kbd>services_pb2.py</kbd>, <kbd>services_pb2.pyi</kbd> e <kbd>services_pb2_grpc.py</kbd>.
</p>
