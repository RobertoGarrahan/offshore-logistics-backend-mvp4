# Usa uma imagem oficial leve do Python
FROM python:3.10-slim

# Define o diretório de trabalho dentro do container
WORKDIR /app

# Copia o arquivo de dependências e instala
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o código para dentro do container
COPY . .

# Expõe a porta que o Flask vai rodar
EXPOSE 5000

# Comando para iniciar a aplicação
CMD ["python", "app.py"]