WITH falar_com_data AS (
    SELECT 
        atendimento_id,
        data_atendimento
    FROM {BDt}
    WHERE entidade_id = {a} 
    AND data_atendimento >= TIMESTAMP '2023-01-01 00:00:00.000' 
    AND data_do_handover <> data_atendimento
    AND handover_reason = 'REQUESTED_TEAM_SUPPORT'
),
idade_filtrada AS (
    SELECT *
    FROM (
        SELECT 
            p.atendimento_id,
            p.age,
            DATE_PARSE(
                CAST(p.y AS VARCHAR) || '-' || 
                LPAD(CAST(p.m AS VARCHAR), 2, '0') || '-' || 
                LPAD(CAST(p.d AS VARCHAR), 2, '0'), 
                '%Y-%m-%d'
            ) AS data_idade,
            f.data_atendimento,
            ROW_NUMBER() OVER (
                PARTITION BY p.atendimento_id, f.data_atendimento
                ORDER BY 
                    ABS(DATE_DIFF(
                        'day', 
                        DATE_PARSE(CAST(p.y AS VARCHAR) || '-' || LPAD(CAST(p.m AS VARCHAR), 2, '0') || '-' || LPAD(CAST(p.d AS VARCHAR), 2, '0'), '%Y-%m-%d'), 
                        f.data_atendimento
                    )) ASC,
                    DATE_PARSE(CAST(p.y AS VARCHAR) || '-' || LPAD(CAST(p.m AS VARCHAR), 2, '0') || '-' || LPAD(CAST(p.d AS VARCHAR), 2, '0'), '%Y-%m-%d') ASC
            ) AS rownumber
        FROM {BDp} p
        JOIN falar_com_data f ON p.atendimento_id = f.atendimento_id
        WHERE p.age <> ''
    ) AS sub
    WHERE rownumber = 1
),
sexo AS (
    SELECT DISTINCT 
        ROW_NUMBER() OVER (PARTITION BY atendimento_id ORDER BY y DESC, m DESC, d DESC) AS rownumber,
        atendimento_id,
        symptoms_values
    FROM {BDv}
    WHERE LOWER(symptoms_question) LIKE '%sexo%'
)

SELECT DISTINCT 
    alert.atendimento_id,
    idade.age,
    sexo.symptoms_values,
    DATE_FORMAT(alert.data_alerta, '%d-%m-%Y %H:%i:%s') AS Data,
    alert.resultado
FROM {BDa} AS alert
LEFT JOIN (
    SELECT DISTINCT 
        ROW_NUMBER() OVER (PARTITION BY y, m, d, atendimento_id ORDER BY age DESC) AS rownumber,
        atendimento_id,
        age, 
        d, 
        m,
        y
    FROM {BDp}
) AS idade ON alert.atendimento_id = idade.atendimento_id
LEFT JOIN sexo ON alert.atendimento_id = sexo.atendimento_id
WHERE alert.entidade_id = {a} 
AND alert.data_alerta >= TIMESTAMP '2023-01-01 00:00:00.000'  
AND (idade.rownumber = 1 OR idade.rownumber IS NULL)
AND (sexo.rownumber = 1 OR sexo.rownumber IS NULL)
AND DAY(alert.data_alerta) = idade.d 
AND MONTH(alert.data_alerta) = idade.m 
AND YEAR(alert.data_alerta) = idade.y
UNION ALL
-- PARTE 2: FALAR COM EQUIPE
SELECT DISTINCT 
    falar.atendimento_id,
    idade.age,
    sexo.symptoms_values,
    DATE_FORMAT(falar.data_atendimento,  '%d-%m-%Y %H:%i:%s') AS Data, 
    'falar_com_equipe' AS tipo_atendimento
FROM {BDt} AS falar
LEFT JOIN idade_filtrada AS idade ON falar.atendimento_id = idade.atendimento_id 
    AND falar.data_atendimento = idade.data_atendimento
LEFT JOIN sexo ON falar.atendimento_id = sexo.atendimento_id
WHERE falar.entidade_id = {a}
AND falar.data_atendimento >= TIMESTAMP '2023-01-01 00:00:00.000' 
AND falar.data_do_handover <> falar.data_atendimento
AND falar.handover_reason = 'REQUESTED_TEAM_SUPPORT'
AND (sexo.rownumber = 1 OR sexo.rownumber IS NULL)
