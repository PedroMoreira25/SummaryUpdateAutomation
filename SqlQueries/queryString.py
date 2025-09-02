import pathlib as p


def queryString(query):
    try: 
        qStr  = p.Path(f'SqlQueries/{query}.sql').read_text()
        return(qStr)
    except:
        return 0 