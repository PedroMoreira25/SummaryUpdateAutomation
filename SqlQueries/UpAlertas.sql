WITH idade AS(
    SELECT DISTINCT 
        ROW_NUMBER() OVER(PARTITION BY y, m, d, atendimento_id ORDER BY age DESC) AS rownumber,
        atendimento_id,
        age, 
        d, 
        m,
        y
    FROM lc_patient
    WHERE age<>''
),
sexo AS(
    SELECT DISTINCT 
        ROW_NUMBER() OVER(PARTITION BY atendimento_id ORDER BY Y DESC, M DESC, D DESC) AS rownumber,
        atendimento_id,
        symptoms_values
    FROM lc_vital_signs
    WHERE symptoms_question LIKE '%Sexo%' OR symptoms_question LIKE '%sexo%'
)
SELECT DISTINCT 
    alert.atendimento_id,
    idade.age,
    sexo.symptoms_values,
    DATE_FORMAT(alert.data_alerta, '%d-%m-%Y %H:%i:%s') AS data, 
    alert.resultado
FROM lc_alert AS alert
LEFT JOIN idade ON alert.atendimento_id = idade.atendimento_id 
LEFT JOIN sexo ON alert.atendimento_id = sexo.atendimento_id
WHERE alert.entidade_id={a} 
    AND YEAR(alert.data_alerta) > 2022
    AND DATE_TRUNC('month', alert.data_alerta) <> DATE_TRUNC('month', NOW()) 
    AND (idade.rownumber=1 OR idade.rownumber IS NULL)
    AND (sexo.rownumber=1 OR sexo.rownumber IS NULL)
    AND DAY(alert.data_alerta)=idade.d 
    AND MONTH(alert.data_alerta)=idade.m 
    AND YEAR(alert.data_alerta)=idade.y