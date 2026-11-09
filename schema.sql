CREATE TABLE IF NOT EXISTS monstros_dnd (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    tipo VARCHAR(100),
    nivel_desafio NUMERIC(5, 2),
    cr NUMERIC(5, 2),
    hp INTEGER,
    criado_em TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
