alertas=f"""
      SELECT 
    CONCAT('01-', CAST(MONTH(data_alerta) AS VARCHAR), '-', CAST(YEAR(data_alerta) AS VARCHAR)) AS mes,
    resultado, 
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY CONCAT('01-', CAST(MONTH(data_alerta) AS VARCHAR), '-', CAST(YEAR(data_alerta) AS VARCHAR))), 2) AS porcentagem
FROM (
    SELECT DISTINCT 
        atendimento_id,
        data_alerta,
        resultado
    FROM 
        lc_alert 
    WHERE 
        entidade_id = 65 
        AND MONTH(data_alerta) = MONTH(NOW()) - 1
        AND YEAR(data_alerta) = YEAR(NOW())
) AS dados_unicos
GROUP BY 
    CONCAT('01-', CAST(MONTH(data_alerta) AS VARCHAR), '-', CAST(YEAR(data_alerta) AS VARCHAR)),
    resultado;
"""

comorbidade="""
    SELECT DISTINCT
    atendimento_id,
    symptoms_values,
    data_coleta
FROM
    lc_vital_signs
WHERE
    entidade_id = 65 
    AND MONTH(data_coleta) = MONTH(NOW()) - 1 
    AND YEAR(data_coleta) = YEAR(NOW())
    AND (
        symptoms_question = 'Você apresenta alguma doença crônica como:'
        OR symptoms_question = 'Você se identifica com algum dos grupos indicados abaixo?'
        OR symptoms_question = 'Você apresenta alguma doença crônica como pressão alta, diabetes e câncer?'
        OR symptoms_question = 'Você apresenta alguma doença crônica?'
        OR symptoms_question = 'Você apresenta alguma doença crônica?'
        OR symptoms_question = 'Você apresenta alguma doença crônica como:'
        OR symptoms_question = 'Você apresenta alguma doença crônica como pressão alta, diabetes e câncer?'
        OR symptoms_question = 'Você apresenta alguma doença crônica?'
        OR symptoms_question = 'Você apresenta alguma doença crônica como pressão alta, diabetes e câncer?'
        OR symptoms_question = 'Possui alguma das doenças indicadas abaixo?'
        OR symptoms_question = 'Possui alguma das doenças indicadas abaixo?'
        OR symptoms_question = 'Você se identifica com algum dos grupos indicados abaixo?'
    )
    AND symptoms_values NOT IN(
        'Tabagismo',
        'Colaborador da Unimed Litoral/Maternidade Santa Luiza'
        )
"""

