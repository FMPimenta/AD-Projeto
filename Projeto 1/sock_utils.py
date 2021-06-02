"""
Aplicações distribuídas - Projeto 1 - sock_utils.py
Grupo: 3 
Membros: Francisco Pimenta 54973, Pedro Quintão 54971 
"""
import socket as s

def create_tcp_server_socket(adress, port, queue_size):
    sock = s.socket(s.AF_INET, s.SOCK_STREAM)
    sock.bind((adress,port))
    sock.listen(queue_size)

    return sock

def create_tcp_client_socket(adress, port):
    sock = s.socket(s.AF_INET, s.SOCK_STREAM)
    sock.connect((adress, port))

    return sock
