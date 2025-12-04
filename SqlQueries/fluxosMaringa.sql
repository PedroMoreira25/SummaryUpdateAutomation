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
    CASE 
        WHEN vital.symptoms_question = 'Você acha que quebrou algum osso do seu corpo?' THEN 'Ossos Quebrados'
        WHEN vital.symptoms_question = 'Você está perdendo sangue, ou está com uma queimadura na pele?' THEN 'Perda de Sangue ou Queimadura na Pele'
        WHEN vital.symptoms_question = 'Você está se sentindo donto ou com vertigem?' THEN 'Tontura ou Vertigem'
        WHEN vital.symptoms_question = 'Você está sentindo dor no peito, braços, costas, pescoço ou mandíbula?' THEN 'Dor no peito, braços, costas, pescoço ou mandíbula'
        WHEN vital.symptoms_question = 'Você está sentindo formigamento ou paralisia em algum membro do corpo?' THEN 'Formigamento ou Paralisia'
        WHEN vital.symptoms_question = 'Você está sentindo perda de equilíbrio ou dificuldade para andar?' THEN 'Perda de Equilíbrio ou Dificuldade para Andar'
        WHEN vital.symptoms_question = 'Você sente falta de ar ou dificuldade para respirar?' THEN 'Falta de Ar'
        WHEN vital.symptoms_question = 'Você tem dificuldade para falar ou entender o que os outros estão dizendo?' THEN 'Dificuldade para falar ou Entender o que estão dizendo'
        WHEN vital.symptoms_question = 'Você teve algum episódio de desmaio recentemente (24 horas)?' THEN 'Desmaio recente'
        WHEN vital.symptoms_question = 'Você teve alguma queda e está sentindo muita dor?' THEN 'Queda ou muita dor'
        ELSE vital.symptoms_question
    END AS symptoms_question_indicador,
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
            AND vital.symptoms_values NOT IN ('Não')
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
                AND vital.atendimento_id NOT IN (
                    8558720983,95402592071,70051130041,93442053021,6705385901,88171570070,37447639869,
                    15210845052,98564453029,49152349837,13056433134,71334608075,85000623045,86461736077,
                    37447639869,77924787003,2417826003,87300412017,91986762025,23990611011,2417826003,
                    2506704027,37447639869,51811211011,22658166044,21202182003,30709176074,31907605002,
                    70051130041,30458834009,49152349837,339356022,947786988,95449977093,50434692000,
                    71334608075,32837062987,87006811058,29764709958,63217930002,8947807940,49152349837,
                    87006811058,401381005,49152349837,44800874009,89767592067,52073537057,13056433134,
                    36805362083,81398062006,31176534734,15210845052,54991473020,37447639869,12510920049,
                    35588394046,17985952730,8558720983,88171570070,75789637752,25118796385,23990611011,
                    49152349837,74654741089,49152349837,7275217996,68997285084,70051130041,1878443054,
                    61455891088,9815365908,7671731986,88171570070,2657151051,37524611013,8558720983,
                    55283012034,23990611011,35588394046,27193103016,44035454087,35588394046,24986087029,
                    7671731986,32397504065,1038604958,26984687004,80703716093,1038604958,6705385901,
                    44800874009,88171570070,8558720983,22786615070,403993385,85396097035,7275217996,
                    9815365908,68997285084,84157376021,88264234070,54313557083,37524611013,70051130041,
                    7841955952,57301507097,12815268787,81785783017,37853629001,118996037,41587723034,
                    57867056092,9888251040,30095151036,71334608075,947786988,45221172054,67180527017,
                    94196890008,7841955952,564473022,93442053021,1564157040,63439529002,37447639869,
                    70051130041,13056433134,38748671029,9969770071,15210845052,93214619063,947786988,
                    21202182003,76662273023,67993424038,1038604958,33380076040,3142229019,50348046030,
                    40601186800,99978383000,3860419030,15877201085,29764709958,8223951002,77646297070,
                    37524611013,63985159351,81785783017,50457814055,70051130041,9815365908,88664744521,
                    6946145992,403993385,10423196421,63015897004,88592781043,403993385,6963419051,77261205095,
                    21516745094,41587723034,11773821725,49152349837,49152349837,7671731986,96624437030,95449977093,
                    1038604958,45221172054,24364397024,7841955952,41587723034,37524611013,29764709958,57433470000,
                    91402050020,41587723034,25955083006,42685264205,37524611013,401381005,15210845052,88664744521,
                    42142971806,40070517045,6362626001,40601186800,57345410013,26093058000,403993385,57301507097,
                    83983192084,63985159351,26576519095,947786988,49575056086,1038604958,403993385,44841335048,
                    403993385,8558720983,14250063020,24364397024,60283413042,28630824000
                )
