#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações distribuídas - Projeto 3 - DatabaseSQL.py
Grupo: 3 
Membros: Francisco Pimenta 54973, Pedro Quintão 54971 
"""
# Zona para fazer importação
import sqlite3
from os.path import isfile

def connect_db(dbname):
    db_is_created = isfile(dbname) # Existe ficheiro da base de dados?
    connection = sqlite3.connect(dbname)
    cursor = connection.cursor()
    if not db_is_created:
        cursor.execute("PRAGMA foreign_keys = ON;")
        connection.commit()
        
        cursor.execute("CREATE TABLE utilizadores ( \
            id INTEGER PRIMARY KEY AUTOINCREMENT,\
            nome TEXT,\
            senha TEXT\
            );")
        connection.commit()
        
        cursor.execute("CREATE TABLE albuns (\
            id INTEGER PRIMARY KEY AUTOINCREMENT,\
            id_spotify TEXT,\
            nome TEXT,\
            id_artista INTEGER,\
            FOREIGN KEY(id_artista) REFERENCES artistas(id)\
            );")
        connection.commit()
        
        cursor.execute("CREATE TABLE artistas (\
            id INTEGER PRIMARY KEY AUTOINCREMENT,\
            id_spotify TEXT,\
            nome TEXT\
            );")
        connection.commit()
        
        cursor.execute("CREATE TABLE avaliacoes (\
            id INTEGER PRIMARY KEY ,\
            sigla TEXT,\
            designacao TEXT\
            );")
        connection.commit()
        
        cursor.execute("CREATE TABLE listas_albuns (\
            id_user INTEGER,\
            id_album INTEGER,\
            id_avaliacao INTEGER,\
            PRIMARY KEY (id_user, id_album),\
            FOREIGN KEY(id_user) REFERENCES utilizadores(id),\
            FOREIGN KEY(id_album) REFERENCES albuns(id)\
            FOREIGN KEY(id_avaliacao)REFERENCES avaliacoes(id)\
            );\
            ")
        connection.commit()

        avaliacoes = [(1, "M", "Medi­ocre"),
                      (2, "m", "Mau"),
                      (3, "S", "Suficiente"),
                      (4, "B", "Bom"),
                      (5, "MB", "Muito Bom")]

        cursor.executemany('INSERT INTO avaliacoes VALUES (?,?,?)', avaliacoes)
        connection.commit()

    return connection, cursor