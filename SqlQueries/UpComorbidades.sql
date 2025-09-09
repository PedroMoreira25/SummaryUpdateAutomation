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
    comor.atendimento_id,
    idade.age,
    sexo.symptoms_values,
    comor.data_coleta,
    TRIM(comor.symptoms_values)
    FROM 
        lc_vital_signs AS comor 
        LEFT JOIN 
            idade 
            ON comor.atendimento_id=idade.atendimento_id 
        LEFT JOIN 
            sexo 
            ON comor.atendimento_id=sexo.atendimento_id 
        WHERE 
            comor.entidade_id={a}
            AND DATE_TRUNC('month', comor.data_coleta) <> DATE_TRUNC('month', NOW())
            AND YEAR(comor.data_coleta) > 2022 
            AND (comor.symptoms_question='Você apresenta alguma doença crônica?' 
                OR comor.symptoms_question='Você apresenta alguma doença crônica como pressão alta, diabetes e câncer?'
                OR comor.symptoms_question='Você apresenta alguma doença crônica ou toma remédio para algum dos itens abaixo?'
                OR comor.symptoms_question='Você se identifica com algum dos grupos indicados abaixo?'
                OR comor.symptoms_question='Possui alguma das doenças indicadas abaixo?'
                OR comor.symptoms_question='Você se identifica com algum dos grupos indicados abaixo? ')
            AND TRIM(comor.symptoms_values) NOT IN (
                'Resultado de teste RT-PCR ou antígeno positivo',
                'Contato positivo',
                'Gestante',
                'Nenhum',
                'Nadou em piscina, mar ou rio nas últimas duas semanas',
                'Outras',
                'Idade ≥ 70 anos',
                'Fumante (cigarro, charuto, narguilé, etc)',
                'Idade ≤ 1 ano',
                'Profissionais de saúde',
                'Idoso',
                'Contato com positivo (domiciliar)',
                'Tabagista',
                'Criança',
                'Usa rotineiramente cotonete',
                'Ex-tabagista',
                'Tem otite de repetição'
                )
            AND idade.dataa = CAST(DATE_FORMAT(comor.data_coleta, '%e/%c/%Y') AS VARCHAR)
            AND idade.rownumber = 1 
            AND (sexo.rownumber = 1 OR sexo.rownumber IS NULL) 