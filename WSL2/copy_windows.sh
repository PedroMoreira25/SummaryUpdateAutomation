#!/bin/bash

origem=/home/pedro/Main-Estagio

destino="/mnt/c/Users/pedro/Desktop"

nome_pasta_copiada="Python Munai"

echo "Copiando $origem para $destino/$nome_pasta_copiada ..."

cp -r "$origem" "$destino/$nome_pasta_copiada" 

echo "Copiado com sucesso!!!"
