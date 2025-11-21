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
	FROM {BDp}
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
			FROM {BDs2} AS soap
				JOIN idade i ON i.atendimento_id = soap.atendimento_id
				AND i.data_coleta <= soap.data_do_soap_evolution
		) sub
	WHERE rn = 1
),
sexo AS (
	SELECT 
	    atendimento_id,
		symptoms_values,
		ROW_NUMBER() OVER (
			PARTITION BY atendimento_id
			ORDER BY y DESC,
				m DESC,
				d DESC
		) AS rownumber
	FROM {BDv}
	WHERE LOWER(symptoms_question) LIKE '%sexo%'
),
tele_hora AS (
    SELECT DISTINCT 
        atendimento_id,
        data_coleta 
        FROM 
            {BDr}
                WHERE 
                    entidade_id=147                     
                      AND setor='IN_PROGRESS'
                      AND servicestep='telemedicine'
                      AND usuario<>'SISTEMA'
            ),
tele_hora_join AS (
    SELECT DISTINCT 
        tele_hora.atendimento_id,
        tele_hora.data_coleta,
        ROW_NUMBER() OVER(PARTITION BY tele_hora.atendimento_id ORDER BY tele_hora.data_coleta DESC) AS rankk 
        FROM 
            tele_hora 
                LEFT JOIN 
                    {BDs2} AS soap
                    ON tele_hora.atendimento_id = soap.atendimento_id
                    AND tele_hora.data_coleta < soap.data_do_soap_evolution 
        )
SELECT DISTINCT 
    soap.atendimento_id,
	idade_filtrada.age,
	sexo.symptoms_values,
	soap.completed_teleconsult,
	soap.data_do_soap_evolution,
	tele_hora_join.data_coleta,
	HOUR(tele_hora_join.data_coleta) AS hora_teleconsulta
        FROM {BDs2} AS soap
	        LEFT JOIN 
	            idade_filtrada 
	            ON idade_filtrada.atendimento_id = soap.atendimento_id
	            AND idade_filtrada.data_do_soap_evolution = soap.data_do_soap_evolution
	        LEFT JOIN 
	            sexo 
	            ON sexo.atendimento_id = soap.atendimento_id
	            AND (sexo.rownumber = 1 OR sexo.rownumber IS NULL)
            LEFT JOIN 
                tele_hora_join
                ON tele_hora_join.atendimento_id = soap.atendimento_id
                AND tele_hora_join.rankk = 1 
        WHERE 
			soap.entidade_id = {a} 
            	AND DATE_TRUNC('month', soap.data_do_soap_evolution) = DATE_TRUNC('month', DATE_ADD('month', -1, NOW()))
	        	AND LOWER(soap.completed_teleconsult)='true'