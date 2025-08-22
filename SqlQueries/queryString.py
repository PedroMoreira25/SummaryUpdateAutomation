import pathlib as p


def queryString(query):
    qStr  = p.Path(f'SqlQueries/{query}.sql').read_text()
    return(qStr)
