WITH idade AS(
    SELECT DISTINCT 
        ROW_NUMBER() OVER (PARTITION BY atendimento_id, CONCAT(CAST(d AS VARCHAR),'/',CAST(m AS VARCHAR),'/',CAST(y AS VARCHAR)) ORDER BY age DESC) AS rownumber,
        atendimento_id,
        age,
        CONCAT(CAST(d AS VARCHAR),'/',CAST(m AS VARCHAR),'/',CAST(y AS VARCHAR)) AS dataa
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
    alert.atendimento_id, 
    idade.age,
    sexo.symptoms_values,
    CONCAT(CAST(MONTH(alert.data_alerta) AS VARCHAR),'-',CAST(YEAR(alert.data_alerta) AS VARCHAR)) AS "Mês"
    FROM 
        {BDa} AS alert 
        LEFT JOIN 
            idade  
            ON idade.atendimento_id = alert.atendimento_id 
        LEFT JOIN 
            sexo 
            ON sexo.atendimento_id = alert.atendimento_id 
        WHERE 
            alert.entidade_id={a} 
            AND alert.data_alerta >= TIMESTAMP '2023-01-01 00:00:00.000' 
            AND (sexo.rownumber = 1 OR sexo.rownumber IS NULL)
            AND idade.rownumber = 1
            AND idade.age<>''
            AND DATE_FORMAT(alert.data_alerta, '%e/%c/%Y') = idade.dataa