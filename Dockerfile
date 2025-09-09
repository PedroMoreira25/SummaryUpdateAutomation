#criação da imagem 
FROM python:3.10-slim 

#diretório de trabalho dentro do container
WORKDIR /app 

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "teste.py"]