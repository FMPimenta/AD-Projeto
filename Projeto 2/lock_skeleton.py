#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações distribuídas - Projeto 1 - lock_skeleton.py
Grupo: 3 
Membros: Francisco Pimenta 54973, Pedro Quintão 54971 
"""

import lock_pool, pickle

###############################################################################

class lock_skeleton:
    def __init__(self, numberResources, resourceBlocks, totalResourcesBlocked):
        self.resourcePool = lock_pool.lock_pool(numberResources, resourceBlocks, totalResourcesBlocked)

    def processMessage(self, msg_bytes) :
        pedido = pickle.loads(msg_bytes)
        print(pedido)


        try:
            contador = 0
            for i in pedido:
                pedido[contador] = int(i)
                contador += 1

            comandosPossiveis = [10, 20, 30, 40, 50, 60, 70, 80]

            resposta = []

            if len(pedido) > 0 and pedido[0] in comandosPossiveis:
                resposta = [pedido[0]+1]

                lock_allowed = True

                if self.resourcePool.stats("Y") >= self.resourcePool.Y:
                    lock_allowed = False

                self.resourcePool.clear_expired_locks()
                self.resourcePool.disable_resources()

                if pedido[0] == 10:
                    if len(pedido) < 4:
                        if len(pedido) == 1:
                            resposta.append('MISSING ARGUMENTS')
                        elif pedido[1].isalpha() or pedido[2].isalpha() or pedido[3].isalpha():
                            resposta.append("UNKNOW COMMAND")
                        else:
                            resposta.append('MISSING ARGUMENTS')
                    elif len(pedido) > 4:
                        resposta.append("UNKNOW COMMAND")
                    elif lock_allowed:
                        dados = self.resourcePool.lock(pedido[1], int(pedido[3]), int(pedido[2]))
                        resposta.append(dados)
                    elif lock_allowed == False:
                        resposta.append(False)

                elif pedido[0] == 20:

                    if len(pedido) < 3:
                        if is_int(pedido[1]) == False: 
                            resposta.append("UNKNOW COMMAND")
                        else:
                            resposta.append('MISSING ARGUMENTS')

                    elif is_int(pedido[1]) == False or is_int(pedido[2]) == False or len(pedido) > 3:
                        resposta.append("UNKNOW COMMAND")
        
                    else:
                        dados = self.resourcePool.unlock(int(pedido[1]), int(pedido[2]))
                        resposta.append(dados)

                elif pedido[0] in [30,40] :

                    if len(pedido) == 2:
                        if is_int(pedido[1]) == False:
                            resposta.append("UNKNOW COMMAND")
                        else:
                            if pedido[0] == 30:
                                option = "R"
                            else: 
                                option = "K"
                            dados = self.resourcePool.status(option, int(pedido[1]))
                            resposta.append(dados)
                            
                    elif len(pedido) < 2:
                        resposta.append("MISSING ARGUMENTS")

                    elif len(pedido) > 2:
                        resposta.append('UNKNOW COMMAND')

                elif pedido[0] in [50,60,70] and len(pedido) == 1:

                    if pedido[0] == 50:
                        option = "Y"
                    elif pedido[0] == 60:
                        option = "N"
                    else:
                        option = "D"

                    dados = self.resourcePool.stats(option)
                    resposta.append(dados)

                elif pedido[0] == 80 and len(pedido) == 1:
                    dados = str(self.resourcePool)
                    resposta.append(dados)
                    
                else:
                    resposta.append('UNKNOW COMMAND')
            else:
                resposta.append('UNKNOW COMMAND')

            return resposta
        
        except:
            return("UNKNOW COMMAND")
            
        

        

def is_int(number):
    try: 
        int(number)
        return True
    except ValueError:
        return False
    
