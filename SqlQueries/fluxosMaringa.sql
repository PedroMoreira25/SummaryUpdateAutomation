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
            AND DATE_TRUNC('month', vital.data_coleta) = DATE_TRUNC('month', DATE_ADD('month', -1, NOW()))
            AND vital.symptoms_question NOT IN(
                'Clique em "Outros" e digite o nome completo do responsável legal do paciente e clique em ✅',
                'Clique em "Outros" e digite o CPF do responsável legal do paciente no formato xxx.xxx.xxx-xx e clique em ✅',
                'Clique em "Outros", digite o CPF do paciente no formato xxx.xxx.xxx-xx e clique em ✅',
                'Clique em "Outros", digite a data de nascimento do paciente no formato xx/xx/xxxx e clique em ✅',
                'Não quero mais receber acompanhamento ?',
                'Clique em "Outros" e digite o CPF do paciente no formato xxx.xxx.xxx-xx.',
                'Clique em "Outros" e digite a data de nascimento do paciente no formato xx/xx/xxxx',
                'A paciente está grávida?',
                'O atendimento é para você ou para outra pessoa(filhos, idosos)?',
                'O atendimento é para crianças menores ou iguais a dois anos?',
                'Linha de cuidado:',
                'Selecione seu grau de parentesco com o paciente: ',
                'O paciente é menor de 14 anos completos?',
                'Qual seu sexo?',
                'O paciente tem menos de 14 anos?',
                'O paciente tem menos de 2 anos?',
                'Qual o sexo do paciente?',
                'Você está grávida?',
                'Você declara para os devidos fins que é o(a) representante legal do menor?'
                )
                AND idade.data = CAST(DATE_FORMAT(vital.data_coleta, '%e/%c/%Y') AS VARCHAR)
                AND idade.rownumber = 1 
                AND (sexo.rownumber = 1 OR sexo.rownumber IS NULL)