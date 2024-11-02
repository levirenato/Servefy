# Usar uma imagem base do Python
FROM python:3.11-slim

# Definir o diretório de trabalho
WORKDIR /app

# Copiar os arquivos requirements.txt para o contêiner
COPY requirements.txt .

# Instalar as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copiar todo o código da aplicação para o diretório de trabalho
COPY . .

# Adicionar o diretório de trabalho ao PYTHONPATH
ENV PYTHONPATH=/app

# Comando para iniciar a aplicação
CMD ["uvicorn", "app.main:app", "--reload", "--host=0.0.0.0", "--port", "8001"]

