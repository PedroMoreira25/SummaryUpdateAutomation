WITH idade AS(
    SELECT DISTINCT 
        ROW_NUMBER() OVER (PARTITION BY atendimento_id, CONCAT(CAST(d AS VARCHAR),'/',CAST(m AS VARCHAR),'/',CAST(y AS VARCHAR)) ORDER BY age DESC) AS rownumber,
        atendimento_id,
        age,
        CONCAT(CAST(d AS VARCHAR),'/',CAST(m AS VARCHAR),'/',CAST(y AS VARCHAR)) AS data
        FROM 
            lc_patient
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
    vital.atendimento_id,
    vital.data_coleta,
    idade.age,
    sexo.symptoms_values,
    vital.symptoms_values
    FROM 
        lc_vital_signs AS vital 
        LEFT JOIN 
            idade 
            ON idade.atendimento_id=vital.atendimento_id
        LEFT JOIN 
            sexo 
            ON sexo.atendimento_id=vital.atendimento_id
        WHERE 
            vital.entidade_id=65 
            AND vital.data_coleta >= TIMESTAMP '2023-01-01 00:00:00.000'  
            AND vital.symptoms_question IN (
                'Qual é o seu principal sintoma? Aqui vai uma lista das queixas mais frequentes:', 
                'OK! Qual é o seu principal sintoma? ',
                'Qual é o seu principal sintoma? ',
                'OK! E qual é o seu PRINCIPAL sintoma? Aqui vai uma lista dos mais comuns'
                )
                AND idade.data = CAST(DATE_FORMAT(vital.data_coleta, '%e/%c/%Y') AS VARCHAR)
                AND idade.rownumber = 1 
                AND (sexo.rownumber = 1 OR sexo.rownumber IS NULL)
/*
WITH idade AS(
    SELECT DISTINCT 
        ROW_NUMBER() OVER (PARTITION BY atendimento_id, CONCAT(CAST(d AS VARCHAR),'/',CAST(m AS VARCHAR),'/',CAST(y AS VARCHAR)) ORDER BY age DESC) AS rownumber,
        atendimento_id,
        age,
        CONCAT(CAST(d AS VARCHAR),'/',CAST(m AS VARCHAR),'/',CAST(y AS VARCHAR)) AS data
        FROM 
            {BDp}
        ),
sexo AS (
    SELECT DISTINCT 
        ROW_NUMBER() OVER (PARTITION BY atendimento_id ORDER BY y DESC, m DESC, d DESC) AS rownumber,
        atendimento_id,
        symptoms_values
    FROM 
        {BDv}
    WHERE 
        LOWER(symptoms_question) LIKE '%sexo%'
)

SELECT DISTINCT 
    vital.atendimento_id,
    vital.data_coleta,
    idade.age,
    sexo.symptoms_values,
    vital.symptoms_values
    FROM 
        {BDv} AS vital 
        LEFT JOIN 
            idade 
            ON idade.atendimento_id=vital.atendimento_id
        LEFT JOIN 
            sexo 
            ON sexo.atendimento_id=vital.atendimento_id
        WHERE 
            vital.entidade_id={a} 
            AND vital.data_coleta >= TIMESTAMP '2023-01-01 00:00:00.000'  
            AND vital.symptoms_question IN (
                'Qual é o seu principal sintoma? Aqui vai uma lista das queixas mais frequentes:', 
                'OK! Qual é o seu principal sintoma? ',
                'Qual é o seu principal sintoma? ',
                'OK! E qual é o seu PRINCIPAL sintoma? Aqui vai uma lista dos mais comuns'
                )
                AND idade.data = CAST(DATE_FORMAT(vital.data_coleta, '%e/%c/%Y') AS VARCHAR)
                AND idade.rownumber = 1 
                AND (sexo.rownumber = 1 OR sexo.rownumber IS NULL)
                */