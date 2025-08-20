WITH idade AS(
    SELECT DISTINCT 
        ROW_NUMBER() OVER (PARTITION BY atendimento_id, CONCAT(CAST(d AS VARCHAR),'/',CAST(m AS VARCHAR),'/',CAST(y AS VARCHAR)) ORDER BY age DESC) AS rownumber,
        atendimento_id,
        age,
        CONCAT(CAST(d AS VARCHAR),'/',CAST(m AS VARCHAR),'/',CAST(y AS VARCHAR)) AS dataa
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
    vital.atendiemnto_id, 
    idade.age,
    sexo.symptoms_values,
    CONCAT(CAST(MONTH(vital.data_coleta) AS VARCHAR),'-',CAST(YEAR(vital.data_coleta) AS VARCHAR)) AS "Mês"
    FROM 
        lc_vital_signs AS vital 
        LEFT JOIN 
            idade  
            ON idade.atendimento_id = vital.atendimento_id 
        LEFT JOIN 
            sexo 
            ON sexo.atendimento_id = vital.atendimento_id 
        WHERE 
            vital.entidade_id={a} 
            AND YEAR(vital.data_coleta) > 2022 
            AND DATE_TRUNC('month', vital.data_coleta) <> DATE_TRUNC('month', NOW()) 
            AND sexo.rownumber = 1
            AND idade.rownumber = 1
            AND DATE_FORMAT(vital.data_coleta, '%e/%c/%Y') = idade.dataa