USE Dra_Amanda

--DROP TABLE plano
--DROP TABLE procedimento
--DROP TABLE user
--DROP TABLE paciente
--DROP TABLE consulta

SELECT * FROM [Dra_Amanda].[dbo].[user]
SELECT * FROM paciente
SELECT * FROM consulta
SELECT * FROM plano
SELECT * FROM procedimento

DELETE FROM paciente
DELETE FROM consulta
DELETE FROM plano
DELETE FROM procedimento

INSERT INTO plano VALUES ('Coopercon'),('Goodlife'),('Fundafemg')
INSERT INTO procedimento VALUES ('Consulta'),('Teste')
INSERT INTO paciente VALUES ('Zenix','1992/03/19','1')


SELECT	*
FROM paciente a
INNER JOIN plano b
ON a.plano_id=b.id