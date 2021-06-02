"""
Aplicações distribuídas - Projeto 1 - sock_utils.py
Grupo: 3 
Membros: Francisco Pimenta 54973, Pedro Quintão 54971 
"""
import socket as s, sys

def create_tcp_server_socket(adress, port, queue_size):
    sock = s.socket(s.AF_INET, s.SOCK_STREAM)
    sock.bind((adress,port))
    sock.listen(queue_size)

    return sock

def create_tcp_client_socket(adress, port):
    sock = s.socket(s.AF_INET, s.SOCK_STREAM)
    sock.connect((adress, port))

    return sock

def receive_all(socket, length):
    received = 0
    mensagem = b''

    while (received < length):
        dados = socket.recv(length-received)
        received += sys.getsizeof(dados)
        mensagem += dados

    return mensagem
