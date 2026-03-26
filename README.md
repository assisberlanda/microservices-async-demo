# Microservices Async Demo 🚀

Este repositório demonstra uma arquitetura de microsserviços assíncrona utilizando Python. O objetivo é ilustrar como dois serviços independentes se comunicam através de eventos, garantindo desacoplamento e resiliência.

## 🛠 Tecnologias Utilizadas
- **Python 3.10+**: Linguagem principal.
- **FastAPI**: Framework para criação das APIs.
- **RabbitMQ**: Message Broker para comunicação assíncrona (AMQP).
- **Pika**: Biblioteca Python para interagir com o RabbitMQ.
- **Docker**: Para orquestração dos serviços e do Broker.

## 🏗 Estrutura do Projeto
O projeto está dividido em pastas independentes para cada contexto de negócio:

- `/service-order`: Gerenciamento de pedidos e publicação de eventos de criação.
- `/service-payment`: Escuta eventos de novos pedidos e processa o pagamento fictício.

## 🔄 Fluxo do Sistema
1. O usuário cria um pedido via `POST /orders`.
2. O `ServiceOrder` salva o pedido com status `PENDING` e envia uma mensagem para a fila.
3. O `ServicePayment` consome a mensagem, processa o pagamento e devolve a confirmação.
4. Fluxo da Arquitetura:
   ```mermaid
   graph LR
    Client((Cliente)) -->|POST /orders| SO[ServiceOrder]
    SO -->|1. Salva Pedido PENDING| DB1[(Database Order)]
    SO -->|2. Publica Evento: order_created| Broker{Message Broker / RabbitMQ}
    Broker -->|3. Consome Evento| SP[ServicePayment]
    SP -->|4. Processa Pagamento| SP
    SP -->|5. Publica Evento: payment_processed| Broker
    Broker -->|6. Atualiza Status| SO
    SO -->|7. Salva Status: PAID/FAILED| DB1
   ```
## 🚀 Como Iniciar e Rodar o Projeto

Siga os passos abaixo para subir todo o ecossistema (Broker + Microsserviços) usando Docker.

### 📋 Pré-requisitos
- [Docker](https://docs.docker.com/get-docker/) instalado.
- [Docker Compose](https://docs.docker.com/compose/install/) instalado.

### 🛠️ Passo a Passo

1. **Clone o repositório:**
   ```bash
   git clone [https://github.com/seu-usuario/microservices-async-demo.git](https://github.com/seu-usuario/microservices-async-demo.git)
   cd microservices-async-demo
   Suba os containers:
2. **Suba os containers:**
Este comando irá baixar as imagens do RabbitMQ e fazer o build dos nossos serviços Python.
```
docker-compose up --build
```
3. Verifique se os serviços estão ativos:

Service Order: [localhost:8000](http://localhost:8000)

RabbitMQ Management (Painel): [localhost:15672](http://localhost:15672) (Login/Senha: guest / guest)

🧪 Testando o Fluxo Assíncrono
Para simular a criação de um pedido e ver a comunicação via mensageria acontecer, abra um novo terminal e execute o comando curl abaixo:
```bash
curl -X 'POST' \
  'http://localhost:8000/orders?order_id=101&item=Macbook' \
  -H 'accept: application/json'
```
O que observar nos logs do terminal:

O service-order receberá a requisição e publicará o evento na fila order_queue.

O service-payment detectará a nova mensagem instantaneamente.

O service-payment processará o pagamento (simulando um delay de 5 segundos) e confirmará a finalização.

🛑 Encerrando o projeto
Para parar todos os serviços, use:
```
docker-compose down
```
1. O Script de Teste (test_load.py)
Como observar o "Efeito Assíncrono"
Para ver a mágica acontecer, siga estes passos:
Prepare o Ambiente: Certifique-se de que o docker-compose up está rodando.
Instale a dependência de teste (na sua máquina local):
```
pip install httpx
```
Execute o script:
```bash
python test_load.py
```
