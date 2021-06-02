#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações distribuídas - Projeto 1 - lock_client.py
Grupo: 3 
Membros: Francisco Pimenta 54973, Pedro Quintão 54971 
"""
# Zona para fazer importação
import sys, lock_stub

# Programa principal

port_exist = False
id_client_exist = False

def is_int(number):
    try: 
        int(number)
        return True
    except ValueError:
        return False

if (len(sys.argv) == 4) :

    try:
        id_client = int(sys.argv[1])
        id_client_exist = True

    except ValueError as v:
        print("Id de cliente tem de ser um número inteiro positivo.")
        print(v)

    address = sys.argv[2]

    try:
        port = int(sys.argv[3])
        port_exist = True

    except ValueError as v:
        print("O porto tem de ser um numero inteiro positivo.")        
        print(v)

    if port_exist == True and id_client_exist == True:
    
        cliente = lock_stub.Lock_stub(address, port)
    
        while True:
            comandoInicial = input('comando > ')

            comando = comandoInicial.split()

            comandosPossiveis = ['LOCK', 'UNLOCK', 'STATUS', 'STATS', 'PRINT', 'SLEEP', 'EXIT']
            
            if len(comando) != 0:
                comandoPedido = comando[0]
            else: 
                comandoPedido = ''

            if comandoPedido in comandosPossiveis:
                
                if comandoPedido == 'LOCK':
                    if len(comando) < 3:
                        if len(comando) == 1:
                            print('MISSING ARGUMENTS')
                        elif comando[1].isalpha():
                            print("UNKNOW COMMAND")
                        else:
                            print('MISSING ARGUMENTS')
                    elif len(comando) > 3 or (is_int(comando[1]) \
                        and is_int(comando[2])) == False:
                        print("UNKNOW COMMAND")
                    else:
                        cliente.lock(int(comando[1]) , int(comando[2]), int(id_client))

                elif comandoPedido == 'UNLOCK':
                    if len(comando) < 2:
                        print('MISSING ARGUMENTS')

                    elif is_int(comando[1]) == False or len(comando) > 2:
                        print("UNKNOW COMMAND")
                    
                    else:
                        cliente.unlock(int(comando[1]), int(id_client))

                elif comandoPedido == 'STATUS':
                    if len(comando) == 3:
                        if comando[1] not in ['R', 'K'] or is_int(comando[2]) == False:
                            print("UNKNOW COMMAND")
                        else:
                            cliente.status(comando[1], int(comando[2])) 
                            
                    elif len(comando) == 2:
                        if comando[1] not in ['R', 'K']:
                            print("UNKNOW COMMAND") 
                        else:
                            print("MISSING ARGUMENTS")
                    elif len(comando) < 2 or len(comando) > 3:
                        print('UNKNOW COMMAND')
                
                elif comandoPedido == 'STATS':
                    if len(comando) == 2:
                        if comando[1] in ['Y', 'N', 'D']:
                            cliente.stats(comando[1])
                        else:
                            print("UNKNOW COMMAND")
                    else:
                        print("UNKNOW COMMAND")
                elif comandoPedido == 'PRINT':
                    cliente.printState()

                elif comandoPedido == 'SLEEP':
                    if len(comando) == 1:
                        print("MISSING ARGUMENTS")
                    if len(comando) == 2:
                        if is_int(comando[1]) == True:
                            if int(comando[1]) < 0:
                                print("UNKNOW COMMAND")
                            else:  
                                cliente.sleep(int(comando[1]))
                        else: 
                            print("UNKNOW COMMAND") 
                    if len(comando) > 2:
                        print("UNKNOW COMMAND")
                
                elif comandoPedido == 'EXIT':
                    cliente.disconnect()
                    break
            else:
                print('UNKNOWN COMMAND')
            

elif len(sys.argv) > 4: 
    print('Argumentos a mais')
    
else:
    print('Faltam argumentos.')

