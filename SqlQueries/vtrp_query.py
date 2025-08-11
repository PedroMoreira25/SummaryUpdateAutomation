alertas="""
WITH idade AS(
    SELECT DISTINCT 
        ROW_NUMBER() OVER(PARTITION BY y, m, d, atendimento_id ORDER BY age DESC) AS rownumber,
        atendimento_id,
        age, 
        d, 
        m,
        y
        FROM 
            lc_patient
                WHERE 
                    age<>''
                ),
sexo AS(
    SELECT DISTINCT 
        ROW_NUMBER() OVER(PARTITION BY atendimento_id ORDER BY Y DESC, M DESC, D DESC) AS rownumber,
        atendimento_id,
        symptoms_values
        FROM 
            lc_vital_signs
                WHERE 
                    symptoms_question LIKE '%Sexo%' OR symptoms_question LIKE '%sexo%'
                )    
SELECT DISTINCT 
    alert.atendimento_id,
    idade.age,
    sexo.symptoms_values,
    DATE_FORMAT(alert.data_alerta, '%d-%m-%Y %H:%i:%s') AS data, 
    alert.resultado
    FROM 
        lc_alert AS alert
            LEFT JOIN 
                idade 
                    ON alert.atendimento_id = idade.atendimento_id 
            LEFT JOIN 
                sexo 
                    ON alert.atendimento_id = sexo.atendimento_id
                        WHERE 
                            alert.entidade_id=76 
                                AND MONTH(alert.data_alerta) = MONTH(NOW()) - 1 
                                AND YEAR(alert.data_alerta) = YEAR(NOW())
                                AND (idade.rownumber=1 OR idade.rownumber IS NULL)
                                AND (sexo.rownumber=1 OR sexo.rownumber IS NULL)
                                AND DAY(alert.data_alerta)=idade.d 
                                AND MONTH(alert.data_alerta)=idade.m 
                                AND YEAR(alert.data_alerta)=idade.y

"""

atendimentos="""
WITH falar_com_data AS (
    SELECT 
        atendimento_id,
        data_atendimento
    FROM 
        lc_speak_to_team
    WHERE 
        entidade_id = 76 
        AND MONTH(data_atendimento) = MONTH(NOW()) - 1 
        AND YEAR(data_atendimento) = YEAR(NOW())
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
        FROM 
            lc_patient p
        JOIN 
            falar_com_data f ON p.atendimento_id = f.atendimento_id
        WHERE 
            p.age <> ''
    ) AS sub
    WHERE rownumber = 1
),
sexo AS (
    SELECT DISTINCT 
        ROW_NUMBER() OVER (PARTITION BY atendimento_id ORDER BY y DESC, m DESC, d DESC) AS rownumber,
        atendimento_id,
        symptoms_values
    FROM 
        lc_vital_signs
    WHERE 
        LOWER(symptoms_question) LIKE '%sexo%'
)

-- PARTE 1: ALERTAS
SELECT DISTINCT 
    alert.atendimento_id,
    idade.age,
    sexo.symptoms_values,
    DATE_FORMAT(alert.data_alerta, '%d-%m-%Y %H:%i:%s') AS Data,
    'Alerta' AS tipo_atendimento
FROM 
    lc_alert AS alert
LEFT JOIN 
    (
        SELECT DISTINCT 
            ROW_NUMBER() OVER (PARTITION BY y, m, d, atendimento_id ORDER BY age DESC) AS rownumber,
            atendimento_id,
            age, 
            d, 
            m,
            y
        FROM 
            lc_patient
        WHERE 
            age <> ''
    ) AS idade ON alert.atendimento_id = idade.atendimento_id
LEFT JOIN 
    sexo ON alert.atendimento_id = sexo.atendimento_id
WHERE 
    alert.entidade_id = 76 
    AND MONTH(alert.data_alerta) = MONTH(NOW()) - 1 
    AND YEAR(alert.data_alerta) = YEAR(NOW())
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
FROM 
    lc_speak_to_team AS falar
LEFT JOIN 
    idade_filtrada AS idade ON falar.atendimento_id = idade.atendimento_id 
        AND falar.data_atendimento = idade.data_atendimento
LEFT JOIN 
    sexo ON falar.atendimento_id = sexo.atendimento_id
WHERE 
    falar.entidade_id = 76
    AND MONTH(falar.data_atendimento) = MONTH(NOW()) - 1
    AND YEAR(falar.data_atendimento) = YEAR(NOW())
    AND falar.data_do_handover <> falar.data_atendimento
    AND falar.handover_reason = 'REQUESTED_TEAM_SUPPORT'
    AND (sexo.rownumber = 1 OR sexo.rownumber IS NULL)
"""