def idCustomer(eid):
    if eid == 65:
        return "Unimed Litoral"
    elif eid == 76:
        return "Unimed VTRP"
    elif eid == 112:
        return "Unimed Salto/Itú"
    elif eid == 130:
        return "Unimed Sul Capixaba"
    elif eid == 146:
        return "Unimed Noroeste Capixaba"
    elif eid == 147:
        return "Unimed Maringá"
    
def queriesCustomer(eid):
    if eid == 65: 
        return["alertas", "atendimentos", "comorbidades", "desfechoEmTriagem", "fluxos", "idade", "sexo", "teleconsultas"]
    elif eid == 112:
        return["alertas", "atendimentos", "fluxos", "idade", "sexo", "tag"]
    elif eid == 130:
        return["alertas", "atendimentos", "teleconsultas", "cid", "comorbidades", "fluxos", "idade", "sexo", "retornou48h"]
    elif eid == 146: 
        return["alertas", "atendimentos", "cid", "comorbidades", "fluxos", "idade", "sexo"]
    elif eid == 147: 
        return["alertas", "atendimentosTeleRealizada", "encPAPresencial", "fluxosMaringa", "idade", "retornou72h", "sexo", "tempoEmSetor"]