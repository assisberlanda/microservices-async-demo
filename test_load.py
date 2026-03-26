import httpx
import asyncio
import time

# URL do seu Service Order rodando no Docker
URL = "http://localhost:8000/orders"

async def send_order(order_id):
    params = {
        "order_id": order_id,
        "item": f"Produto_{order_id}"
    }
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(URL, params=params)
            print(f"OrderId {order_id}: {response.json()['message']}")
    except Exception as e:
        print(f"Erro no pedido {order_id}: {e}")

async def main():
    start_time = time.time()
    print("🚀 Iniciando disparo de 50 pedidos...")
    
    # Cria 50 tarefas de envio simultâneas
    tasks = [send_order(i) for i in range(1, 51)]
    await asyncio.gather(*tasks)
    
    end_time = time.time()
    print(f"\n✅ Todos os 50 pedidos foram enviados para a fila em {end_time - start_time:.2f} segundos!")
    print("Verifique agora os logs do Docker para ver o Service Payment processando um por um.")

if __name__ == "__main__":
    # Certifique-se de ter o httpx instalado: pip install httpx
    asyncio.run(main())