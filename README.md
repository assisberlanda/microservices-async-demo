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
