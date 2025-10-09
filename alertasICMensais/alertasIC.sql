WITH table_setor 
    AS
    (SELECT DISTINCT 
        CONCAT(CAST(entidade_id AS VARCHAR),setor_id) AS pk,
        setor_nome
            FROM TABELA_IC_MOVIMENTACOES 
                WHERE 
                    setor_nome<>''                    
                    AND CAST((SUBSTRING(data_entrada, 6, 2)) AS INTEGER) = MONTH(DATE_ADD('month', -1, DATE_TRUNC('month', NOW())))
                    AND CAST((SUBSTRING(data_entrada, 1, 4)) AS INTEGER) = YEAR(DATE_ADD('month', -1, DATE_TRUNC('month', NOW())))
        )

SELECT DISTINCT 
    al.atendimento_id,
    CONCAT(SUBSTRING(al.date_alert_updated, 9, 2),'-',SUBSTRING(al.date_alert_updated, 6, 2),'-',SUBSTRING(al.date_alert_updated, 1, 4),' ',SUBSTRING(al.date_alert_updated, 12, 12)) AS Data_do_Alerta,
    al.color_dash,
    al.leito,
    mov.setor_nome,
    CASE 
        WHEN al.status='created' THEN 'Criado'
        WHEN al.status='tma_reached' THEN 'Estourado'
        WHEN al.status='updated' THEN 'Atualizado'
        END AS "status"
            FROM TABELA_IC_ALERTAS AS al 
                LEFT JOIN table_setor AS mov 
                    ON (CONCAT(CAST(al.entidade_id AS VARCHAR),al.process_id) = mov.pk)
                    AND mov.setor_nome NOT IN (
                            'PA',
                            '6 AND',
                            '7 AND',
                            'UPAF 19',
                            'UPAF 21',
                            'UNIDADE CUIDADOS RESPIRATORIOS',
                            'BLOCO CIRURGICO - SALAS'
                            )
                        WHERE 
                            al.entidade_id= {a}
                            AND CAST((SUBSTRING(al.date_alert_updated, 6, 2)) AS INTEGER) = MONTH(DATE_ADD('month', -1, DATE_TRUNC('month', NOW())))
                            AND CAST((SUBSTRING(al.date_alert_updated, 1, 4)) AS INTEGER) = YEAR(DATE_ADD('month', -1, DATE_TRUNC('month', NOW())))
                            AND al.status<>'removed' 
                            