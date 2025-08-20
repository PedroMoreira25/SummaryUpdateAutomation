WITH teleconsulta_data AS (
    SELECT 
        atendimento_id,
        data_coleta
    FROM 
        lc_evolution_record
    WHERE 
        entidade_id = {a}
        AND DATE_TRUNC('month', data_coleta) = DATE_TRUNC('month', DATE_ADD('month', -1, NOW())) 
        AND setor='IN_PROGRESS'
        AND fromservicestep='telemedicine'
        AND servicestep='telemedicine'
        AND usuario<>'SISTEMA' 
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
            f.data_coleta,
            ROW_NUMBER() OVER (
                PARTITION BY p.atendimento_id, f.data_coleta
                ORDER BY 
                    ABS(DATE_DIFF(
                        'day', 
                        DATE_PARSE(CAST(p.y AS VARCHAR) || '-' || LPAD(CAST(p.m AS VARCHAR), 2, '0') || '-' || LPAD(CAST(p.d AS VARCHAR), 2, '0'), '%Y-%m-%d'), 
                        f.data_coleta
                    )) ASC,
                    DATE_PARSE(CAST(p.y AS VARCHAR) || '-' || LPAD(CAST(p.m AS VARCHAR), 2, '0') || '-' || LPAD(CAST(p.d AS VARCHAR), 2, '0'), '%Y-%m-%d') ASC
            ) AS rownumber
        FROM 
            lc_patient p
        JOIN 
            teleconsulta_data f ON p.atendimento_id = f.atendimento_id
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

SELECT DISTINCT 
    record.atendimento_id,
    idade.age,
    sexo.symptoms_values,
    record.data_coleta,
    'Teleconsulta' AS teleconsulta
FROM 
    lc_evolution_record AS record
LEFT JOIN 
    idade_filtrada AS idade ON record.atendimento_id = idade.atendimento_id 
        AND record.data_coleta = idade.data_coleta
LEFT JOIN 
    sexo ON record.atendimento_id = sexo.atendimento_id
WHERE 
    record.entidade_id = {a}
    AND DATE_TRUNC('month', record.data_coleta) = DATE_TRUNC('month', DATE_ADD('month', -1, NOW()))
    AND record.setor='IN_PROGRESS'
    AND record.servicestep='telemedicine'
    AND record.usuario<>'SISTEMA'  
    AND (sexo.rownumber = 1 OR sexo.rownumber IS NULL)