#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações distribuídas - Projeto 1 - lock_server.py
Grupo: 3 
Membros: Francisco Pimenta 54973, Pedro Quintão 54971 
"""

# Zona para fazer importação
import socket as s, sys, struct, pickle, select as sel, lock_skeleton, sock_utils

###############################################################################

# código do programa principal

if (len(sys.argv) == 6) :

    serverIP = sys.argv[1]

    try:
        serverPort = int(sys.argv[2])
    
    except ValueError as v:
        print("Porto tem de ser um número inteiro positivo.")
        print(v)
        
    try:
        numberResources = int(sys.argv[3])
    
    except ValueError as v:
        print("Número de recursos tem de ser um número inteiro positivo.")
        print(v)

    try:
        resourceBlocks = int(sys.argv[4])
    
    except ValueError as v:
        print("Número de bloqueios permitidos tem de ser um número inteiro positivo.")
        print(v)

    try:
        totalResourcesBlocked = int(sys.argv[5])

    except ValueError as v:
        print("Número permitido de recursos bloqueados num dado momento \
             tem de ser um número inteiro positivo.")
        print(v)

    listenSock = sock_utils.create_tcp_server_socket(serverIP, serverPort, 1)
    
    skel = lock_skeleton.lock_skeleton(numberResources, resourceBlocks, totalResourcesBlocked)

    SocketList = [listenSock]

    while True:
        
        R, W, X = sel.select(SocketList, [], [])

        for sock in R:
            if sock is listenSock: 
                conn_sock, (addr, port) = listenSock.accept()
                print('Novo cliente ligado desde %s:%d' % (addr, port))
                SocketList.append(conn_sock)

            else:

                try: 
                    size_bytes = sock_utils.receive_all(sock, 4)
                    if size_bytes:     
                        size = struct.unpack('i', size_bytes)[0]

                        msg_bytes = sock_utils.receive_all(sock, size)

                        ans = skel.processMessage(msg_bytes)
                        
                        print(ans)
                        
                        ans_bytes = pickle.dumps(ans, -1)
                        size_bytes = struct.pack('i',len(ans_bytes))

                        sock.sendall(size_bytes)
                        sock.sendall(ans_bytes)

                    else: 
                        sock.close() 
                        SocketList.remove(sock)
                        print('Cliente fechou ligação')

                except:
                    print("Servidor configurado para receber 4 bytes.")

                

else:
    print("MISSING ARGUMENTS")


