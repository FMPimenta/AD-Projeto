/* Aplicações distribuídas - Projeto 3 - sql.py
Grupo: 3 
Membros: Francisco Pimenta 54973, Pedro Quintão 54971  */

PRAGMA foreign_keys = ON;

CREATE TABLE utilizadores ( 
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    senha TEXT
);

CREATE TABLE albuns (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_spotify TEXT,
    nome TEXT,
    id_artista INTEGER,
    FOREIGN KEY(id_artista) REFERENCES artistas(id)
);

CREATE TABLE artistas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    id_spotify TEXT,
    nome TEXT
);

CREATE TABLE avaliacoes (
    id INTEGER PRIMARY KEY ,
    sigla TEXT,
    designacao TEXT
);

CREATE TABLE listas_albuns (
    id_user INTEGER,
    id_album INTEGER,
    id_avaliacao INTEGER,
    PRIMARY KEY (id_user, id_album),
    FOREIGN KEY(id_user) REFERENCES utilizadores(id),
    FOREIGN KEY(id_album) REFERENCES albuns(id),
    FOREIGN KEY(id_avaliacao)REFERENCES avaliacoes(id)
);

INSERT INTO avaliacoes VALUES (1, "M", "Medi­ocre");
INSERT INTO avaliacoes VALUES (2, "m", "Mau");
INSERT INTO avaliacoes VALUES (3, "S", "Suficiente");
INSERT INTO avaliacoes VALUES (4, "B", "Bom");
INSERT INTO avaliacoes VALUES (5, "MB", "Muito Bom");