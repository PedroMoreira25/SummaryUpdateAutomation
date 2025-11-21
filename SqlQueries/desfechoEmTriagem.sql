WITH idade AS (
	SELECT atendimento_id,
		age,
		DATE_PARSE(
			CONCAT(CAST(y AS VARCHAR), '-', CAST(m AS VARCHAR), '-', CAST(d AS VARCHAR)), '%Y-%c-%e'
			) AS data_coleta
	FROM {BDp}
),
idade_filtrada AS (
	SELECT *
	FROM (
			SELECT rec.atendimento_id,
				idade.age,
				idade.data_coleta AS idade_data_coleta,
				rec.data_coleta AS rec_data_coleta, 
				ROW_NUMBER() OVER (
					PARTITION BY 
					rec.atendimento_id,
					rec.data_coleta
					ORDER BY idade.data_coleta DESC
				) AS rn
			FROM {BDr} AS rec 
				JOIN idade 
    				ON idade.atendimento_id = rec.atendimento_id
    				AND idade.data_coleta <= rec.data_coleta
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
)

SELECT DISTINCT 
    rec.atendimento_id,
    sexo.symptoms_values,
    idade_filtrada.age,
    rec.currentalert_data_alerta,
    rec.data_coleta,
    rec.email,
    rec.fromservicestep,
    rec.motivo,
    rec.servicestep,
    rec.setor,
    rec.usuario
    FROM 
        {BDr} AS rec 
        LEFT JOIN 
            sexo 
                ON sexo.atendimento_id = rec.atendimento_id
                AND (sexo.rownumber = 1 OR sexo.rownumber IS NULL)
        LEFT JOIN 
            idade_filtrada
                ON idade_filtrada.atendimento_id = rec.atendimento_id 
                AND idade_filtrada.rec_data_coleta = rec.data_coleta 
            WHERE 
                rec.entidade_id = {a} 
                AND DATE_TRUNC('month', rec.data_coleta) = DATE_TRUNC('month', DATE_ADD('month', -1, NOW()))
            ORDER BY rec.atendimento_id, rec.data_coleta, rec.currentalert_data_alerta ASC
            