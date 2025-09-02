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
    city.atendimento_id,
    idade.age,
    sexo.symptoms_values,
    city.bairro,
    CONCAT(CAST(city.d AS VARCHAR),'/',CAST(city.m AS VARCHAR),'/',CAST(city.y AS VARCHAR)) AS dataa
FROM 
    {BDp} AS city
LEFT JOIN 
    idade ON city.atendimento_id = idade.atendimento_id 
LEFT JOIN 
    sexo ON city.atendimento_id = sexo.atendimento_id
WHERE 
    city.entidade_id = {a}
    AND city.bairro <> ''
    AND idade.data = CONCAT(CAST(city.d AS VARCHAR),'/',CAST(city.m AS VARCHAR),'/',CAST(city.y AS VARCHAR))
    AND idade.rownumber=1 
    AND (sexo.rownumber = 1 OR sexo.rownumber IS NULL)
    AND y IN (2023, 2024, 2025)