a=0
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
                            alert.entidade_id={a} 
                                AND DATE_TRUNC('month', alert.data_alerta) = DATE_TRUNC('month', DATE_ADD('month', -1, NOW())) 
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
        entidade_id = {a} 
        AND DATE_TRUNC('month', data_atendimento) = DATE_TRUNC('month', DATE_ADD('month', -1, NOW())) 
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
    alert.entidade_id = {a} 
    AND DATE_TRUNC('month', alert.data_alerta) = DATE_TRUNC('month', DATE_ADD('month', -1, NOW())) 
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
    falar.entidade_id = {a}
    AND DATE_TRUNC('month', falar.data_atendimento) = DATE_TRUNC('month', DATE_ADD('month', -1, NOW()))
    AND falar.data_do_handover <> falar.data_atendimento
    AND falar.handover_reason = 'REQUESTED_TEAM_SUPPORT'
    AND (sexo.rownumber = 1 OR sexo.rownumber IS NULL)
"""

teleconsultas="""
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
"""

cidades = """
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
    city.atendimento_id,
    idade.age,
    sexo.symptoms_values,
    city.bairro,
    CONCAT(CAST(city.d AS VARCHAR),'/',CAST(city.m AS VARCHAR),'/',CAST(city.y AS VARCHAR)) AS dataa
FROM 
    lc_patient AS city
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
    AND m = MONTH(DATE_ADD('month', -1, NOW()))
    AND y = YEAR(DATE_ADD('month', -1, NOW()))
"""

fluxos = """
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
            vital.entidade_id={a} 
            AND DATE_TRUNC('month', vital.data_coleta) = DATE_TRUNC('month', DATE_ADD('month', -1, NOW()))  
            AND (vital.symptoms_question='Qual é o seu principal sintoma? Aqui vai uma lista das queixas mais frequentes:' OR vital.symptoms_question='OK! Qual é o seu principal sintoma? ' 
                OR vital.symptoms_question='Qual é o seu principal sintoma? ')
                AND idade.data = CAST(DATE_FORMAT(vital.data_coleta, '%e/%c/%Y') AS VARCHAR)
                AND idade.rownumber = 1 
                AND (sexo.rownumber = 1 OR sexo.rownumber IS NULL)

"""

cid = """
WITH idade AS (
	SELECT atendimento_id,
		age,
		DATE_PARSE(
			CONCAT(
				CAST(y AS VARCHAR),
				'-',
				CAST(m AS VARCHAR),
				'-',
				CAST(d AS VARCHAR)
			),
			'%Y-%c-%e'
		) AS data_coleta
	FROM lc_patient
),
idade_filtrada AS (
	SELECT *
	FROM (
			SELECT soap.atendimento_id,
				i.age,
				i.data_coleta,
				soap.data_do_soap_evolution,
				ROW_NUMBER() OVER (
					PARTITION BY soap.atendimento_id,
					soap.data_do_soap_evolution
					ORDER BY i.data_coleta DESC
				) AS rn
			FROM lc_soap_infos AS soap
				JOIN idade i ON i.atendimento_id = soap.atendimento_id
				AND i.data_coleta <= soap.data_do_soap_evolution
		) sub
	WHERE rn = 1
),
sexo AS (
	SELECT atendimento_id,
		symptoms_values,
		ROW_NUMBER() OVER (
			PARTITION BY atendimento_id
			ORDER BY y DESC,
				m DESC,
				d DESC
		) AS rownumber
	FROM lc_vital_signs
	WHERE LOWER(symptoms_question) LIKE '%sexo%'
)
SELECT DISTINCT soap.atendimento_id,
	idade_filtrada.age,
	sexo.symptoms_values,
	soap.document_evolution_soap_cid,
	soap.data_do_soap_evolution
FROM lc_soap_infos AS soap
	LEFT JOIN idade_filtrada ON idade_filtrada.atendimento_id = soap.atendimento_id
	AND idade_filtrada.data_do_soap_evolution = soap.data_do_soap_evolution
	LEFT JOIN sexo ON sexo.atendimento_id = soap.atendimento_id
	AND (sexo.rownumber = 1 OR sexo.rownumber IS NULL)
WHERE soap.entidade_id = {a}
	AND DATE_TRUNC('month', soap.data_do_soap_evolution) = DATE_TRUNC('month', DATE_ADD('month', -1, NOW()))

"""

comorbidades = """
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
            AND DATE_TRUNC('month', comor.data_coleta) = DATE_TRUNC('month', DATE_ADD('month', -1, NOW()))
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
"""

idade = """
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
    alert.atendimento_id, 
    idade.age,
    sexo.symptoms_values,
    CONCAT(CAST(MONTH(alert.data_alerta) AS VARCHAR),'-',CAST(YEAR(alert.data_alerta) AS VARCHAR)) AS "Mês"
    FROM 
        lc_alert AS alert 
        LEFT JOIN 
            idade  
            ON idade.atendimento_id = alert.atendimento_id 
        LEFT JOIN 
            sexo 
            ON sexo.atendimento_id = alert.atendimento_id 
        WHERE 
            alert.entidade_id={a} 
            AND DATE_TRUNC('month', alert.data_alerta) = DATE_TRUNC('month', DATE_ADD('month', -1, NOW())) 
            AND (sexo.rownumber = 1 OR sexo.rownumber IS NULL)
            AND idade.rownumber = 1
            AND idade.age<>''
            AND DATE_FORMAT(alert.data_alerta, '%e/%c/%Y') = idade.dataa
"""

sexo = """
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
            AND DATE_TRUNC('month', vital.data_coleta) = DATE_TRUNC('month', DATE_ADD('month', -1, NOW())) 
            AND sexo.rownumber = 1
            AND idade.rownumber = 1
            AND DATE_FORMAT(vital.data_coleta, '%e/%c/%Y') = idade.dataa
"""

