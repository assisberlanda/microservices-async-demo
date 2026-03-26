# Usa uma imagem oficial leve do Python
FROM python:3.10-slim

# Define variáveis de ambiente para evitar arquivos .pyc e garantir logs em tempo real
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Instala as dependências primeiro para aproveitar o cache do Docker camadas (Layer Caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia o restante do código fonte
COPY . .

# Informa ao Docker que o container ouve na porta 8000
EXPOSE 8000

# Executa o Uvicorn apontando para o objeto 'app' dentro de 'main.py'
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]