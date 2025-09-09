import pathlib as p

"""
# esse é só para eu usar para atualizar as bases
def queryString(query):
    try: 
        qStr  = p.Path(f'alertasICMensais/{query}.sql').read_text()
        str(qStr)
        return(qStr)
    except:
        return 0 
        print("Deu erro ao encontrar o arquivo SQL")
   """

#esse é o do projeto de estágio
def queryString(query):
    try: 
        qStr  = p.Path(f'SqlQueries/{query}.sql').read_text(encoding="utf-8")
        str(qStr)
        return(qStr)
    except:
        return 0 
        print("Deu erro ao encontrar o arquivo SQL")
     