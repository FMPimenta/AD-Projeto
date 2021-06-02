#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Aplicações distribuídas - Projeto 1 - lock_stub.py
Grupo: 3 
Membros: Francisco Pimenta 54973, Pedro Quintão 54971 
"""

import net_client

class Lock_stub:

    def __init__(self, address, port):
        self.conn_sock = net_client.server(address, port)

    def disconnect(self):
         self.conn_sock.close()

    def sleep(self, duration):
        self.conn_sock.sleep(duration)

    def lock(self, resourceNumber, duration, clientId):
        self.conn_sock.send_receive([10, resourceNumber , duration, clientId])

    def unlock(self, resourceNumber, clientId):
        self.conn_sock.send_receive([20, resourceNumber, clientId])

    def status(self, option, resourceNumber):
        if option == "R":
            self.conn_sock.send_receive([30, resourceNumber])
        else:
            self.conn_sock.send_receive([40, resourceNumber])

    def stats(self, option):
        if option == "Y":
            self.conn_sock.send_receive([50])
        elif option == "N":
            self.conn_sock.send_receive([60])
        else:
            self.conn_sock.send_receive([70])

    def printState(self):
        self.conn_sock.send_receive([80])