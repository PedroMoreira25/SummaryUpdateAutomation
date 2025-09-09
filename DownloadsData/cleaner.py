import os
import glob

# Caminho da pasta
folder = "DownloadsData"

# Lista todos os arquivos CSV
files = glob.glob(os.path.join(folder, "*.csv"))

# Ordena pela data de modificação (mais antigos primeiro)
files.sort(key=os.path.getmtime)

# Se tiver mais de 5, apaga os mais antigos
while len(files) > 5:
    oldest = files.pop(0)  # remove o primeiro (mais antigo)
    os.remove(oldest)
    print(f"Arquivo removido: {oldest}")

