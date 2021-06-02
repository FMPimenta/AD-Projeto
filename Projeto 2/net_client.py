# -*- coding: utf-8 -*-
"""
Aplicações distribuídas - Projeto 1 - net_client.py
Grupo: 3 
Membros: Francisco Pimenta 54973, Pedro Quintão 54971 
"""

# zona para fazer importação
import pickle, struct, time, sock_utils
 
class server:
    """
    Abstrai uma ligação a um servidor TCP. Implementa métodos para: estabelecer 
    a ligação; envio de um comando e receção da resposta; terminar a ligação.
    """
    def __init__(self, address, port):
        """
        Inicializa a classe com parâmetros para funcionamento futuro.
        """
        self.address = address
        self.port = port
        self.sock = sock_utils.create_tcp_client_socket(address, port)

    def send_receive(self, data):
        """
        Envia os dados contidos em data para a socket da ligação, e retorna
        a resposta recebida pela mesma socket.
        """
        
        msg_bytes = pickle.dumps(data, -1)
        size_bytes = struct.pack('i', len(msg_bytes))
  
        print(data)
        
        if size_bytes != 0:
            self.sock.sendall(size_bytes)
            self.sock.sendall(msg_bytes)
        
            size_bytes = sock_utils.receive_all(self.sock, 4)
            size = struct.unpack('i', size_bytes)[0]

            msg_bytes = sock_utils.receive_all(self.sock, size)
            msg = pickle.loads(msg_bytes)

            print(msg)
        

    def close(self):
        """
        Termina a ligação ao servidor.
        """

        self.sock.close()

    def sleep(self, sleepTime):

        time.sleep(sleepTime)
