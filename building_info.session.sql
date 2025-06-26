-- 1. Création de la table vide (structure identique)
CREATE TABLE dpe_equilibree_30k (LIKE tablefull INCLUDING ALL);

-- 2. Pour la classe 'A'
INSERT INTO dpe_equilibree_30k
SELECT * FROM tablefull
WHERE etiquette_dpe = 'A' AND numero_dpe IN (
    SELECT numero_dpe FROM tablefull
    WHERE etiquette_dpe = 'A'
    ORDER BY RANDOM()
    LIMIT 4500
);

-- 3. Idem pour 'B'
INSERT INTO dpe_equilibree_30k
SELECT * FROM tablefull
WHERE etiquette_dpe = 'B' AND numero_dpe IN (
    SELECT numero_dpe FROM tablefull
    WHERE etiquette_dpe = 'B'
    ORDER BY RANDOM()
    LIMIT 4500
);
INSERT INTO dpe_equilibree_30k
SELECT * FROM tablefull
WHERE etiquette_dpe = 'C' AND numero_dpe IN (
    SELECT numero_dpe FROM tablefull
    WHERE etiquette_dpe = 'C'
    ORDER BY RANDOM()
    LIMIT 4500
);
INSERT INTO dpe_equilibree_30k
SELECT * FROM tablefull
WHERE etiquette_dpe = 'D' AND numero_dpe IN (
    SELECT numero_dpe FROM tablefull
    WHERE etiquette_dpe = 'D'
    ORDER BY RANDOM()
    LIMIT 4500
);
INSERT INTO dpe_equilibree_30k
SELECT * FROM tablefull
WHERE etiquette_dpe = 'E' AND numero_dpe IN (
    SELECT numero_dpe FROM tablefull
    WHERE etiquette_dpe = 'E'
    ORDER BY RANDOM()
    LIMIT 4500
);
INSERT INTO dpe_equilibree_30k
SELECT * FROM tablefull
WHERE etiquette_dpe = 'F' AND numero_dpe IN (
    SELECT numero_dpe FROM tablefull
    WHERE etiquette_dpe = 'F'
    ORDER BY RANDOM()
    LIMIT 4500
);
INSERT INTO dpe_equilibree_30k
SELECT * FROM tablefull
WHERE etiquette_dpe = 'G' AND numero_dpe IN (
    SELECT numero_dpe FROM tablefull
    WHERE etiquette_dpe = 'G'
    ORDER BY RANDOM()
    LIMIT 4500
);

select etiquette_dpe, COUNT(*) from tablefull
GROUP BY etiquette_dpe

DROP TABLE dpe_equilibree_30k
DROP TABLE dpe_equilibree_30k_less_than_10p

SELECT COUNT(*)
FROM INFORMATION_SCHEMA.COLUMNS
WHERE table_name = 'tablefull'

SELECT COLUMN_NAME
FROM INFORMATION_SCHEMA.COLUMNS
WHERE table_name = 'tablefull'

