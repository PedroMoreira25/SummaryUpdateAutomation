WITH idade AS (
    SELECT DISTINCT 
        atendimento_id,
        age, 
        DATE_PARSE(CONCAT(CAST(y AS VARCHAR),'-',CAST(m AS VARCHAR),'-',CAST(d AS VARCHAR)),'%Y-%c-%e') AS data_coleta
        FROM 
            lc_patient
),
idade_filtrada AS (
    SELECT *
    	FROM (
    			SELECT 
    			    tag.atendimento_id,
                    i.age,
    				tag.data_atendimento,
    				ROW_NUMBER() OVER (
    					PARTITION BY tag.atendimento_id, tag.data_atendimento
    					ORDER BY i.data_coleta DESC
    				) AS rn
    			FROM 
    			    lc_team_tags AS tag
        				JOIN idade i ON i.atendimento_id = tag.atendimento_id
        				AND i.data_coleta <= tag.data_atendimento
    		) sub
    	WHERE rn = 1    
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
    tag.atendimento_id,
    idade_filtrada.age,
    sexo.symptoms_values,
    tag.data_atendimento,
    tag.document_tags
    FROM    
        lc_team_tags AS tag
        LEFT JOIN 
            sexo 
                ON sexo.atendimento_id = tag.atendimento_id 
                AND (sexo.rownumber = 1 OR sexo.rownumber IS NULL)
        LEFT JOIN   
            idade_filtrada 
                ON idade_filtrada.atendimento_id = tag.atendimento_id 
                AND idade_filtrada.data_atendimento = tag.data_atendimento
            WHERE 
                tag.entidade_id = {a}
                AND DATE_TRUNC('month', tag.data_atendimento) = DATE_TRUNC('month', DATE_ADD('month', -1, NOW()))