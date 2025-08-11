#!/bin/bash 

imagem="img-projeto"

docker build -t $imagem .

docker run --rm -v "$(pwd)/dados:/app/dados" $imagem

