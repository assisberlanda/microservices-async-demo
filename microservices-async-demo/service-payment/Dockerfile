FROM python:3.10-slim
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
# O payment não precisa de EXPOSE pois ele não recebe requisições HTTP, ele apenas consome a fila
CMD ["python", "consumer.py"]