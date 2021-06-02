#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações distribuídas - Projeto 3 - ServerFlask.py
Grupo: 3 
Membros: Francisco Pimenta 54973, Pedro Quintão 54971 
"""
# Zona para fazer importação
import sqlite3
from os.path import isfile
from flask import Flask, request, make_response, g, jsonify, redirect, url_for
import requests
import DatabaseSQL as sql
import ssl
from requests_oauthlib import OAuth2Session
import os

#connection to spotify 
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def spotify(id, type):

    base_url = 'https://api.spotify.com/v1/'

    if type == 'artist':
        artist_id = id
        r = spotify_oauth.get(base_url + 'artists/' + artist_id)
        r = r.json()

        return r['name']
    else: 
        album_id = id
        r = spotify_oauth.get(base_url + 'albums/' + album_id)
        r = r.json()

        return [r['artists'][0]['id'], r['name']] 


DATABASE = "data.db"

sql.connect_db(DATABASE)

app = Flask(__name__)

client_id = 'd8f6037313284ec5a922cdb3b7e19919'
client_secret = '3ef9981a2bb1456a8430f499b0a297af'
redirect_uri = 'https://localhost:5000/callback'
spotify_oauth = OAuth2Session(client_id, redirect_uri=redirect_uri)


@app.route('/login', methods = ['GET'])
def login():
    authorization_base_url = 'https://accounts.spotify.com/authorize'
    authorization_url, state = spotify_oauth.authorization_url(authorization_base_url)
    return redirect(authorization_url)

@app.route('/callback', methods = ['GET'])
def callback():

    token_url = 'https://accounts.spotify.com/api/token'
    url_response = request.url
    spotify_oauth.fetch_token(token_url, client_secret=client_secret, authorization_response= url_response)    
    return "Autorizado"

@app.route('/utilizadores', methods = ["POST", "GET", "DELETE"])
def utilizadores():

    if request.method == "GET":
        # Ler dados dos utilizadores na base de dados
        cur = get_db().execute('SELECT * FROM utilizadores')
        rv = cur.fetchall()
        cur.close()

        if len(rv) > 0:
            resposta = ""
        
            for e in rv:
                resposta += f"ID: {e[0]}     NOME: {e[1]}     SENHA: {e[2]} \n"

            r = make_response(str(resposta))
            r.status_code = 200

            return r
        else:
            r = make_response()
            r.status_code = 404
            r.headers['Error'] = 'Não existem utilizadores na base de dados'

            return r

    if request.method == "POST":
        #Adicionar os dados de um utilizador
        data = request.get_json()
        nome = data['nome']
        senha = data['senha']
        cur = get_db().execute('INSERT INTO utilizadores VALUES (?,?,?)', (None, nome, senha))
        get_db().commit()
        cur = get_db().execute('SELECT * FROM utilizadores WHERE nome = "%s" AND senha = "%s"' % (nome, senha))
        rv = cur.fetchone()
        cur.close()

        r = make_response('Utilizador %s criado com sucesso' % nome)
        r.status_code = 201
        r.headers['location'] = '/utilizadores/%d' % rv[0]
        return r

    if request.method == "DELETE":
        #Apagar os dados de todos os utilizadores
        cur = get_db().execute('SELECT * FROM utilizadores')
        rv = cur.fetchall()
        cur.close()

        if len(rv) > 0:

            cur = get_db().execute('DELETE FROM utilizadores')
            get_db().commit()
            cur.close()
        
            r = make_response('Dados de todos os utilizadores apagados com sucesso')
            r.status_code = 200
        else:
            r = make_response()
            r.status_code = 204
            r.headers['Error'] = 'Não existem dados a apagar'
        
        return r

@app.route('/utilizadores/<int:id_user>', methods = ["GET", "DELETE", "PUT"])
def utilizadores_id(id_user):

    if request.method == "GET":
        #Ler dados de um utilizador na base de dados
        cur = get_db().execute('SELECT * FROM utilizadores WHERE id = %d' % id_user)
        rv = cur.fetchone()
        cur.close()

        if len(rv) > 0:
            resposta = f"ID: {rv[0]}     NOME: {rv[1]}     SENHA: {rv[2]}"

            r = make_response(str(resposta))
            r.status_code = 200
        else:
            r = make_response()
            r.status_code = 404
            r.headers['Error'] = "Não foi encontrado nenhum utilizador com o id %d" % id_user

        return r

    if request.method == "PUT":
        #Atualizar a senha de um utilizador
        data = request.get_json()
        password = data['password']

        cur = get_db().execute('SELECT * FROM utilizadores WHERE id = %d' % id_user)
        uti = cur.fetchone()
        cur.close()

        if len(uti) > 0:
            cur = get_db().execute('UPDATE utilizadores SET senha = "%s" WHERE id = %d' % (password, id_user))
            cur.close()

            
            r = make_response('Palavra-passe de %s atualizada com sucesso!' % uti[1])
            r.status_code = 200
        else:
            r = make_response()
            r.status_code = 404
            r.headers['Error'] = "Não foi encontrado nenhum utilizador com o id %d" % id_user

        return r


    if request.method == "DELETE":
        #Apagar os dados de um utilizador
        cur = get_db().execute('SELECT * FROM utilizadores WHERE id = %d' % id_user)
        uti = cur.fetchone()
        cur.close()

        if len(uti) > 0:
            cur = get_db().execute('DELETE FROM utilizadores WHERE id = %d' % id_user)
            get_db().commit()
            cur.close()
            
            r = make_response('Dados do utilizador %d apagados com sucesso' % id_user)
            r.status_code = 200
        else:
            r = make_response()
            r.status_code = 404
            r.headers['Error'] = "Não foi encontrado nenhum utilizador com o id %d" % id_user

        return r

@app.route('/utilizadores/<int:id_user>/avaliacoes', methods = ["GET", "DELETE"])
def utilizadores_id_user_avaliacoes(id_user):

    if request.method == "GET":
        #Ler dados de todas os albuns avaliados por um utilizador na base de dados
        cur = get_db().execute('SELECT * FROM listas_albuns WHERE id_user = %d' % id_user)
        rv = cur.fetchall()
        cur.close()
        resposta = ""

        if len(rv) > 0:
            for e in rv:

                cur = get_db().execute('SELECT * FROM albuns WHERE id = %d' % e[1])
                alb = cur.fetchone()
                cur.close()

                cur = get_db().execute('SELECT * FROM avaliacoes WHERE id = %d' % e[2])
                ava = cur.fetchone()
                cur.close()

                resposta += f"ID: {alb[0]}     ID_SPOTIFY: {alb[1]}     NOME: {alb[2]}     ID_ARTISTA: {alb[3]}     AVALIACAO: {ava[2]} \n"

            


            r = make_response(str(resposta))
            r.status_code = 200

        else:
            r = make_response()
            r.status_code = 404
            r.headers['Error'] = "Não foi encontrado nenhum utilizador com o id %d" % id_user

        return r

    if request.method == "DELETE":
        #Apagar todos os albuns avaliados por um utilizador
        cur = get_db().execute('SELECT * FROM utilizadores WHERE id = %d' % id_user)
        uti = cur.fetchone()
        cur.close()

        if len(uti) > 0:
            cur = get_db().execute('DELETE FROM listas_albuns WHERE id_user = %d' % id_user)
            get_db().commit()
            cur.close()
        
            r = make_response('Todas as avaliações do utilizador %d apagados com sucesso' % id_user)
            r.status_code = 200
        else:
            r = make_response()
            r.status_code = 404
            r.headers['Error'] = "Não foi encontrado nenhum utilizador com o id %d" % id_user
        
        return r

@app.route('/utilizadores/<int:id_user>/avaliacoes/<int:id_album>', methods = ["PUT", "POST"])
def utilizadores_id_avaliacoes_album_id(id_user, id_album):
    if request.method == "PUT":
        #Atualizar uma avaliação de um utilizador sobre um album
        cur = get_db().execute('SELECT * FROM albuns WHERE id = %d' % id_album)
        alb = cur.fetchone()
        cur.close()

        if len(alb) > 0:
            data = request.get_json()
            avaliacao = data['avaliacao']

            cur = get_db().execute('SELECT * FROM avaliacoes WHERE sigla = "%s"' % avaliacao)
            rv = cur.fetchone()
            cur.close()

         

            if len(rv) > 0:
                cur = get_db().execute('UPDATE listas_albuns SET id_avaliacao = %d WHERE id_user = %d AND id_album = %d' % (rv[0], id_user, id_album))
                cur.close()

                r = make_response('Avaliacao do album %s atualizada com sucesso' % alb[2])
                r.status_code = 200
            else:
                r = make_response()
                r.status_code = 404
                r.headers['Error'] = "Não foi encontrado nenhuma avaliacao com a sigla " + avaliacao
        else:
            r = make_response()
            r.status_code = 404
            r.headers['Error'] = "Não foi encontrado nenhum album com o id %d" % id_album
            
        return r
    
    if request.method == "POST":
        #Adicionar uma avaliacao de um album por um utilizador
        data = request.get_json()
        avaliacao = data['avaliacao']

        cur = get_db().execute('SELECT * FROM avaliacoes WHERE sigla = "%s"' % avaliacao)
        rv = cur.fetchone()
        cur.close()

        if len(rv) > 0:

            cur = get_db().execute('SELECT * FROM avaliacoes WHERE id = %d' % rv[0])
            ava = cur.fetchone()
            cur.close()

            cur = get_db().execute('SELECT * FROM albuns WHERE id = %d' % id_album)
            alb = cur.fetchone()
            cur.close()     
            
            if len(alb) > 0:
                cur = get_db().execute('INSERT INTO listas_albuns VALUES (?,?,?)', (id_user, id_album, rv[0]))
                get_db().commit()

                r = make_response('Album %s avaliado como %s' % (alb[2], ava[2]))
                r.status_code = 200
                r.headers['location'] = '/utilizadores/%d/avaliacoes' % id_user
            else:
                r = make_response()
                r.status_code = 404
                r.headers['Error'] = "Não foi encontrado nenhum album com o id %d" % id_album

        else:
            r = make_response()
            r.status_code = 404
            r.headers['Error'] = "Não foi encontrado nenhuma avaliacao com a sigla " + avaliacao
        
        return r



@app.route('/artistas', methods = ["POST", "GET", "DELETE"])
def artistas():

    if request.method == "GET":
        # Ler dados dos artistas na base de dados
        cur = get_db().execute('SELECT * FROM artistas')
        rv = cur.fetchall()
        cur.close()
        resposta = ""
        if len(rv) > 0:
            for e in rv:
                resposta += f"ID : {e[0]}     ID_SPOTIFY: {e[1]}     NOME: {e[2]} \n"
            
            r = make_response(str(resposta))
            r.status_code = 200
        else:
            r = make_response()
            r.status_code = 404
            r.headers['Error'] = 'Não existem artistas na base de dados'

        return r

    if request.method == "DELETE":
        #Apagar todos os artistas da base de dados
        cur = get_db().execute('SELECT * FROM artistas')
        rv = cur.fetchall()
        cur.close()

        if len(rv) > 0:
            cur = get_db().execute('DELETE FROM artistas')
            get_db().commit()
            cur.close()
            r = make_response('Todos os dados de artistas apagados com sucesso!')
            r.status_code = 200
        else:   
            r = make_response()
            r.status_code = 204
            r.headers['Error'] = 'Não existem dados a apagar'

        return r

    if request.method == "POST":
        #Adicionar os dados de um artista
        data = request.get_json()
        id_spotify = data['id_spotify']
        dado = spotify(id_spotify, 'artist')

        cur = get_db().execute('INSERT INTO artistas VALUES (?,?,?)', (None, id_spotify, dado))
        get_db().commit()
        cur.close()

        cur = get_db().execute('SELECT * FROM artistas WHERE id_spotify = "%s"' % id_spotify)
        rv = cur.fetchone()
        cur.close()

        r = make_response('Artista %s adicionado com sucesso' % dado)
        r.status_code = 200
        r.headers['location'] = '/artistas/%d' % rv[0]
        
        return r
    
@app.route('/artistas/<int:id_artista>', methods = ["GET", "DELETE"])
def artistas_id_artista(id_artista):

    if request.method == "GET":
        # Ler dados de um artista na base de dados
        cur = get_db().execute('SELECT * FROM artistas WHERE id = %d' % id_artista)
        rv = cur.fetchone()
        cur.close()

        if len(rv) > 0:
            resposta = f"ID: {rv[0]}     ID_SPOTIFY: {rv[1]}     NOME: {rv[2]}"

            r = make_response(str(resposta))
            r.status_code = 200
        else:
            r = make_response()
            r.status_code = 404
            r.headers['Error'] = "Não foi encontrado nenhum artista com o id %d" % id_artista

            
        return r
    
    if request.method == "DELETE":
        #Apagar um artista da base de dados
        cur = get_db().execute('SELECT * FROM artistas WHERE id = %d' % id_artista)
        rv = cur.fetchone()
        cur.close()

        if len(rv) > 0:
            cur = get_db().execute('DELETE FROM artistas WHERE id = %d' % id_artista)
            get_db().commit()
            cur.close()

            r = make_response('Todos os dados de %s apagados com sucesso!' % rv[2])
            r.status_code = 200
        else:
            r = make_response()
            r.status_code = 204
            r.headers['Error'] = 'Não existe nenhum artista com id = %d' % id_artista

        return r

@app.route('/artistas/<int:id_artista>/albuns', methods = ["GET", "DELETE"])
def artistas_id_artista_albuns(id_artista):

    if request.method == "GET":
        # Ler dados de todos os albuns feitos por um artista 
        cur = get_db().execute('SELECT * FROM albuns WHERE id_artista = %d' % id_artista)
        rv = cur.fetchall()
        cur.close()
        resposta = ""

        if len(rv) > 0:
            for e in rv:
                resposta += f"{e[0]}: {e[2]} \n"

            r = make_response(str(resposta))
            r.status_code = 200
        else:
            r = make_response()
            r.status_code = 404
            r.headers['Error'] = "Não foi encontrado nenhum artista com o id %d" % id_artista


        return r

    if request.method == "DELETE":
        #Apagar os albuns de um artista da base de dados
        cur = get_db().execute('SELECT * FROM albuns WHERE id_artista = %d' % id_artista)
        rv = cur.fetchall()
        cur.close()

        if len(rv) > 0:
            cur = get_db().execute('DELETE FROM albuns WHERE id_artista = %d' % id_artista)
            get_db().commit()
            cur.close()

            r = make_response('Todos os albuns do artista apagados com sucesso!')
            r.status_code = 200
        else:
            r = make_response()
            r.status_code = 404
            r.headers['Error'] = "Não foi encontrado nenhum artista com o id %d" % id_artista
        
        return r
    
@app.route('/albuns', methods = ["POST", "GET", "DELETE"])
def albuns():
    if request.method == "GET":
        # Ler dados dos albuns na base de dados
        cur = get_db().execute('SELECT * FROM albuns')
        rv = cur.fetchall()
        cur.close()
        print(rv)
        resposta = ""

        if len(rv) > 0: 
            for e in rv:
                resposta += f"ID: {e[0]}     ID_SPOTIFY: {e[1]}     NOME: {e[2]}     ID_ARTISTA: {e[3]} \n"

            r = make_response(str(resposta))
            r.status_code = 200
        else:
            r = make_response()
            r.status_code = 404
            r.headers['Error'] = 'Não existem albuns na base de dados'

        return r

    if request.method == "DELETE":
        #Apagar todos os albuns da base de dados
        cur = get_db().execute('SELECT * FROM albuns')
        art = cur.fetchall()
        cur.close()

        if len(art) > 0:
            cur = get_db().execute('DELETE FROM albuns')
            get_db().commit()
            cur.close()

            r = make_response('Todos os dados de albuns apagados com sucesso!')
            r.status_code = 200
        else:
            r = make_response()
            r.status_code = 404
            r.headers['Error'] = 'Não existe nenhum album para apagar'

        return r

    if request.method == "POST":
        #Adicionar os dados de um album
        data = request.get_json()
        id_spotify = data['id_spotify']
        dados = spotify(id_spotify, 'albuns')

        cur = get_db().execute('SELECT * FROM artistas WHERE id_spotify = "%s"' % dados[0])
        rv = cur.fetchone()
        cur.close()

        if rv != None:
            cur = get_db().execute('INSERT INTO albuns VALUES (?,?,?,?)', (None, id_spotify, dados[1], rv[0]))
            get_db().commit()
            cur.close()

        else:
            dados_artist = spotify(dados[0], 'artist')
            
            cur = get_db().execute('INSERT INTO artistas VALUES (?,?,?)', (None, dados[0], dados_artist))
            get_db().commit()
            cur.close() 

            cur = get_db().execute('SELECT * FROM artistas WHERE id_spotify = "%s"' % dados[0])
            rv = cur.fetchone()
            cur.close()

            cur = get_db().execute('INSERT INTO albuns VALUES (?,?,?, ?)', (None, id_spotify, dados[1], rv[0]))
            get_db().commit()
            cur.close()

        cur = get_db().execute('SELECT * FROM albuns WHERE id_spotify = "%s"' % id_spotify)
        rv = cur.fetchone()
        cur.close()

        r = make_response('Album %s adicionado com sucesso' % dados[1])
        r.status_code = 200
        r.headers['location'] = '/albuns/%d' % rv[0]
        return r

@app.route('/albuns/<int:id_album>', methods = ["GET", "DELETE"])
def albuns_id_album(id_album):

    if request.method == "GET":
        # Ler dados de um album na base de dados
        cur = get_db().execute('SELECT * FROM albuns WHERE id = %d' % id_album)
        rv = cur.fetchone()
        cur.close()

        if len(rv) > 0:
            resposta = f"ID: {rv[0]}     ID_SPOTIFY: {rv[1]}     NOME: {rv[2]}     ID_ARTISTA: {rv[3]}"

            r = make_response(str(resposta))
            r.status_code = 200
        else:
            r = make_response()
            r.status_code = 404
            r.headers['Error'] = 'Não existe esse album na base de dados'

        return r

    if request.method == "DELETE":
        #Apagar um album da base de dados
        cur = get_db().execute('SELECT * FROM albuns WHERE id = %d' % id_album)
        alb = cur.fetchone()
        cur.close()

        if len(alb) < 0:
            cur = get_db().execute('DELETE FROM albuns WHERE id = %d' % id_album)
            get_db().commit()
            cur.close()

            r = make_response('Todos os dados do album %s apagados com sucesso!' % alb[2])
            r.status_code = 200
        else:
            r = make_response()
            r.status_code = 404
            r.headers['Error'] = 'Não foi encontrado nenhum album com id %d na base de dados' % id_album

        return r

@app.route('/albuns/avaliacoes', methods = ["GET", "DELETE"])
def albuns_avaliacoes():

    if request.method == "GET":
        # Ler dados de todos os albuns com uma certa classificação
        data = request.get_json()
        avaliacao = data['avaliacao']

        cur = get_db().execute('SELECT * FROM avaliacoes WHERE sigla = "%s"' % avaliacao)
        rv = cur.fetchone()
        cur.close()

        if len(rv) > 0:

            cur = get_db().execute('SELECT * FROM listas_albuns WHERE id_avaliacao = %d' % rv[0])
            rv = cur.fetchall()
            cur.close()
            print(rv)
            if len(rv) > 0:
                
                resposta = ""
                for e in rv:
                    resposta += f"ID: {e[0]}     ID_SPOTIFY: {e[1]}     NOME: {e[2]}     ID_ARTISTA: {e[3]} \n"

                r = make_response(str(resposta))
                r.status_code = 200
            else:
                r = make_response()
                r.status_code = 404
                r.headers['Error'] = "Não foi encontrado nenhum album com avaliacao " + avaliacao

        else:
            r = make_response()
            r.status_code = 404
            r.headers['Error'] = "Não foi encontrado nenhuma avaliacao com a sigla " + avaliacao

        return r

    if request.method == "DELETE":
        #Apagar todos os albuns com uma certa classificação da base de dados
        data = request.get_json()
        avaliacao = data['avaliacao']

        cur = get_db().execute('SELECT * FROM avaliacoes WHERE sigla = "%s"' % avaliacao)
        rv = cur.fetchone()
        cur.close()

        if len(rv) > 0:
            cur = get_db().execute('SELECT * FROM listas_albuns WHERE id_avaliacao = "%s"' % avaliacao)
            rv = cur.fetchone()
            cur.close()

            if len(rv) > 0:
                cur = get_db().execute('DELETE FROM listas_albuns WHERE id_avaliacao = %d' % rv[0])
                get_db().commit()
                cur.close()

                r = make_response('Todos os albuns com classificação %s apagados com sucesso!') % avaliacao
                r.status_code = 200
            else:
                r = make_response()
                r.status_code = 404
                r.headers['Error'] = "Não foi encontrado nenhuma album com avaliacao " + avaliacao

        else:
            r = make_response()
            r.status_code = 404
            r.headers['Error'] = "Não foi encontrado nenhuma avaliacao com a sigla " + avaliacao

        return r

if __name__ == '__main__':
    certs = "C:\\Users\\Pimentas\\Documents\GitHub\Projeto_ADis\Projeto 4\certs"
    server = "C:\\Users\\Pimentas\\Documents\GitHub\Projeto_ADis\Projeto 4\server"
    context = ssl.SSLContext(protocol=ssl.PROTOCOL_TLS_SERVER)
    context.verify_mode = ssl.CERT_REQUIRED
    context.load_verify_locations(cafile= certs + '\\root.pem')
    context.load_cert_chain(certfile= certs + '\\serv.crt',keyfile= server + '\\serv.key')
    app.run('localhost', ssl_context=context, debug = True)

