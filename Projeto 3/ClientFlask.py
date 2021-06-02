
#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações distribuídas - Projeto 3 - ClientFlask.py
Grupo: 3 
Membros: Francisco Pimenta 54973, Pedro Quintão 54971 
"""
# Zona para fazer importação
import requests
import json

# Programa principal

def is_int(number):
    try: 
        int(number)
        return True
    except ValueError:
        return False

while True:
        
    comandoInicial = input('comando > ')

    comando = comandoInicial.split()

    comandosPossiveis = ['CREATE', 'READ', 'DELETE', 'UPDATE', 'EXIT']
    comandoPedido = comando[0]

    if comandoPedido in comandosPossiveis:
        
        if len(comando) > 1:
            if comandoPedido == 'CREATE':
                if comando[1] == 'UTILIZADOR':
                    if len(comando) == 4:
                        dados = {'nome': comando[2], 'senha': comando[3]}
                        r = requests.post('http://localhost:5000/utilizadores', json = dados)
                        print (r.status_code)
                        print (r.content.decode())
                        print (r.headers)
                        print ('***') 

                    elif len(comando) < 4:
                        print("Argumentos em falta. [CREATE UTILIZADOR <nome> <senha>]")
                    else: 
                        print("Comando desconhecido. [CREATE UTILIZADOR <nome> <senha>]")
                
                elif comando[1] == 'ARTISTA':
                    if len(comando) == 3:
                        r = requests.post('http://localhost:5000/artistas', json = {'id_spotify': comando[2]})
                        print (r.status_code)
                        print (r.content.decode())
                        print (r.headers)
                        print ('***')
                    elif len(comando) < 3:
                        print("Argumentos em falta. [CREATE ARTISTA <id_spotify>]")
                    else: 
                        print("Comando desconhecido. [CREATE ARTISTA <id_spotify>]")

                elif comando[1] == 'ALBUM':
                    if len(comando) == 3:
                        r = requests.post('http://localhost:5000/albuns', json = {'id_spotify': comando[2]})
                        print (r.status_code)
                        print (r.content.decode())
                        print (r.headers)
                        print ('***')
                       
                    elif len(comando) < 3:
                        print("Argumentos em falta. [CREATE ALBUM <id_spotify>]")
                    else: 
                        print("Comando desconhecido. [CREATE ALBUM <id_spotify>]")

                elif is_int(comando[1]):
                    if len(comando) == 4:
                        if is_int(comando[1]) == True and is_int(comando[2]) == True:
                            if comando[3] in ['M', 'm', 'S', 'B', 'MB']:
                                r = requests.post('http://localhost:5000/utilizadores/' + comando[1] + '/avaliacoes/' + comando[2], json = {'avaliacao': comando[3]})
                                print (r.status_code)
                                print (r.content.decode())
                                print (r.headers)
                                print ('***')
                            else: 
                                print('Parâmetro da avaliação incorreto. [M, m, S, B, MB]')
                        else:
                            print("Comando desconhecido. [CREATE <id_user> <id_album> <avaliacao>]")

                    elif len(comando) < 4:
                        print("Argumentos em falta. [CREATE <id_user> <id_album> <avaliacao>]")
                    else: 
                        print("Comando desconhecido. [CREATE <id_user> <id_album> <avaliacao>]")
                else:
                    print("Comando desconhecido. \n[CREATE UTILIZADOR <nome> <senha>]\
                        \n[CREATE ARTISTA <id_spotify>]\
                         \n[CREATE ALBUM <id_spotify>]\
                          \n[CREATE <id_user> <id_album> <avaliacao>]")


            elif comandoPedido in ['READ', 'DELETE']:

                if comandoPedido == 'READ':
                    verificaComando = True
                else: 
                    verificaComando = False

                if comando[1] == 'UTILIZADOR':
                    if len(comando) == 3:
                        if is_int(comando[2]) == True:
                            if verificaComando:
                                r = requests.get('http://localhost:5000/utilizadores/' + comando[2])
                            else:
                                r = requests.delete('http://localhost:5000/utilizadores/' + comando[2])

                            print (r.status_code)
                            print (r.content.decode())
                            print (r.headers)
                            print ('***')
                        else:
                            if verificaComando:
                                print("Comando desconhecido. [READ UTILIZADOR <id_user>]")
                            else: 
                                print("Comando desconhecido. [DELETE UTILIZADOR <id_user>]")

                    elif len(comando) < 3:
                        if verificaComando:
                            print("Argumentos em falta. [READ UTILIZADOR <id_user>]")
                        else: 
                            print("Argumentos em falta. [DELETE UTILIZADOR <id_user>]")

                elif comando[1] == 'ARTISTA':
                    if len(comando) == 3:
                        if is_int(comando[2]) == True:
                            if verificaComando:
                                r = requests.get('http://localhost:5000/artistas/' + comando[2])
                            else:
                                r = requests.delete('http://localhost:5000/artistas/' + comando[2])

                            print (r.status_code)
                            print (r.content.decode())
                            print (r.headers)
                            print ('***')
                        else:
                            if verificaComando:
                                print("Comando desconhecido. [READ ARTISTA <id_artista>]")
                            else: 
                                print("Comando desconhecido. [DELETE ARTISTA <id_artista>]")

                    elif len(comando) < 3:
                        if verificaComando:
                            print("Argumentos em falta. [READ ARTISTA <id_artista>]")
                        else: 
                            print("Argumentos em falta. [DELETE ARTISTA <id_artista>]")

                elif comando[1] == 'ALBUM':
                    if len(comando) == 3:
                        if is_int(comando[2]) == True:
                            if verificaComando:
                                r = requests.get('http://localhost:5000/albuns/' + comando[2])
                            else:
                                r = requests.delete('http://localhost:5000/albuns/' + comando[2])

                            print (r.status_code)
                            print (r.content.decode())
                            print (r.headers)
                            print ('***')
                        else:
                            if verificaComando:
                                print("Comando desconhecido. [READ ALBUNS <id_album>]")
                            else: 
                                print("Comando desconhecido. [DELETE ALBUNS <id_album>]")

                    elif len(comando) < 3:
                        if verificaComando:
                            print("Argumentos em falta. [READ ALBUNS <id_album>]")
                        else: 
                            print("Argumentos em falta. [DELETE ALBUNS <id_album>]")


                elif comando[1] == 'ALL' and len(comando) < 4:
                    verificador = False
                    if len(comando) == 3:
                        if comando[2] == 'UTILIZADORES':
                            verificador = True
                            if verificaComando:
                                r = requests.get('http://localhost:5000/utilizadores')
                            else:
                                r = requests.delete('http://localhost:5000/utilizadores')
                        elif comando[2] == 'ARTISTAS':
                            verificador = True
                            if verificaComando:
                                r = requests.get('http://localhost:5000/artistas')
                            else:
                                r = requests.delete('http://localhost:5000/artistas')
                        elif comando[2] == 'ALBUNS':
                            verificador = True
                            if verificaComando:
                                r = requests.get('http://localhost:5000/albuns')
                            else:
                                r = requests.delete('http://localhost:5000/albuns')
                        
                        if verificador:
                            print (r.status_code)
                            print (r.content.decode())
                            print (r.headers)
                            print ('***')
                        else: 
                            print("Comando desconhecido. \n [READ ALL UTILIZADORES] | [DELETE ALL UTILIZADORES] \
                                 \n [READ ALL ARTISTAS]     | [DELETE ALL ARTISTAS] \n [READ ALL ALBUNS]       | [DELETE ALL ALBUNS]")

                    
                    elif len(comando) < 3:
                        print("Argumentos em falta. \n [READ ALL UTILIZADORES] | [DELETE ALL UTILIZADORES] \
                                 \n [READ ALL ARTISTAS]     | [DELETE ALL ARTISTAS] \n [READ ALL ALBUNS]       | [DELETE ALL ALBUNS]")  
                    else:
                        print("Comando desconhecido. \n [READ ALL UTILIZADORES] | [DELETE ALL UTILIZADORES] \
                                 \n [READ ALL ARTISTAS]     | [DELETE ALL ARTISTAS] \n [READ ALL ALBUNS]       | [DELETE ALL ALBUNS]")



                elif comando[1] == 'ALL' and comando[2] == 'ALBUNS_A':
                    if len(comando) == 4:
                        if is_int(comando[3]) == True:
                            if verificaComando:
                                r = requests.get('http://localhost:5000/artistas/' + comando[3] + '/albuns')
                            else:
                                r = requests.delete('http://localhost:5000/artistas/' + comando[3] + '/albuns')
                            print (r.status_code)
                            print (r.content.decode())
                            print (r.headers)
                            print ('***')

                    elif len(comando) < 4:
                        if verificaComando:
                            print('Argumentos em falta. [READ ALL ALBUNS_A <id_artista>]')  
                        else:
                            print('Argumentos em falta. [DELETE ALL ALBUNS_A <id_artista>]')  

                    else:
                        if verificaComando:
                            print("Comando desconhecido. [READ ALL ALBUNS_A <id_artista>]")
                        else:
                            print("Comando desconhecido. [DELETE ALL ALBUNS_A <id_artista>]")

                elif comando[1] == 'ALL' and comando[2] == 'ALBUNS_U':
                    if len(comando) == 4:
                        if is_int(comando[3]) == True:
                            if verificaComando:
                                r = requests.get('http://localhost:5000/utilizadores/' + comando[3] + '/avaliacoes')
                            else:
                                r = requests.delete('http://localhost:5000/utilizadores/' + comando[3] + '/avaliacoes')
                            print (r.status_code)
                            print (r.content.decode())
                            print (r.headers)
                            print ('***')

                    elif len(comando) < 4:
                        if verificaComando:
                            print('Argumentos em falta. [READ ALL ALBUNS_U <id_artista>]')  
                        else:
                            print('Argumentos em falta. [DELETE ALL ALBUNS_U <id_artista>]')  

                    else:
                        if verificaComando:
                            print("Comando desconhecido. [READ ALL ALBUNS_U <id_artista>]")
                        else:
                            print("Comando desconhecido. [DELETE ALL ALBUNS_U <id_artista>]")
                        
                elif comando[1] == 'ALL' and comando[2] == 'ALBUNS':
                    if len(comando) == 3:
                        if verificaComando:
                            r = requests.get('http://localhost:5000/albuns')
                        else:
                            r = requests.delete('http://localhost:5000/albuns')
                        print (r.status_code)
                        print (r.content.decode())
                        print (r.headers)
                        print ('***')

                    elif len(comando) == 4:
                        if comando[3] in ['M', 'm', 'S', 'B', 'MB']:
                            if verificaComando:
                                r = requests.get('http://localhost:5000/albuns/avaliacoes', json = {'avaliacao': comando[3]})
                            else:
                                r = requests.delete('http://localhost:5000/albuns/avaliacoes', json = {'avaliacao': comando[3]})
                            print (r.status_code)
                            print (r.content.decode())
                            print (r.headers)
                            print ('***')

                        else: 
                            print('Parametro da avaliação incorreto. [M, m, S, B, MB]')
                    elif len(comando) < 3:
                        if verificaComando:
                            print('Argumentos em falta. [READ ALL ALBUNS <avaliacao>]')  
                        else:
                            print('Argumentos em falta. [DELETE ALL ALBUNS <avaliacao>]')  

                    else:
                        if verificaComando:
                            print("Comando desconhecido. [READ ALL ALBUNS <avaliacao>]")
                        else:
                            print("Comando desconhecido. [DELETE ALL ALBUNS <avaliacao>]")

                else:
                    print("Comando desconhecido")

            if comandoPedido == 'UPDATE':
                if comando[1] == 'ALBUM':
                    if len(comando) == 5:
                        if is_int(comando[2]) == True and is_int(comando[4]) == True:
                            if comando[3] in ['M', 'm', 'S', 'B', 'MB']:
    
                                r = requests.put('http://localhost:5000/utilizadores/' + comando[4] + '/avaliacoes/' + comando[2], json = {'avaliacao': comando[3]})
                                print (r.status_code)
                                print (r.content.decode())
                                print (r.headers)
                                print ('***')
                                
                            else: 
                                print('Parametro da avaliação incorreto. [M, m, S, B, MB]')
                        else: 
                            print("Comando desconhecido. [UPDATE ALBUM <id_album> <avaliacao> <id_user>]")
                        
                    elif len(comando) < 5:
                        print('Argumentos em falta. [UPDATE ALBUM <id_album> <avaliacao> <id_user>]')  
                    
                elif comando[1] == 'UTILIZADOR':
                    if len(comando) == 4:
                        if is_int(comando[2]) == True:
                            dados = {'password': comando[3]}
                            r = requests.put('http://localhost:5000/utilizadores/' + comando[2], json = dados)
                            print (r.status_code)
                            print (r.content.decode())
                            print (r.headers)
                            print ('***')
                        else:
                            print("Comando desconhecido. [UPDATE UTILIZADOR <id_user> <password>]")
                    elif len(comando) < 4:
                        print('Argumentos em falta. [UPDATE UTILIZADOR <id_user> <password>]')  
                else:
                    print("Comando desconhecido. [UPDATE UTILIZADOR <id_user> <password>]")

            
        elif comandoPedido == 'EXIT':
            print('Ligação Fechada.')
            break
        
        else:
            print('Comando desconhecido.')
    else:
        print('Comando desconhecido.')
