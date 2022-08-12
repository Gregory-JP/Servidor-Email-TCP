import socket

class Client():
    """
    Construtor do cliente
    """
    def __init__(self, host, port):
        self._HOST = host
        self._PORT = port
        
    def send(self, msg):
        """
        Conexão do cliente com o servidor, envia mensagem para o servidor
        """
        self.__client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__client.connect((self._HOST, self._PORT))
        message = msg.encode()
        self.__client.send(message) # envia mensagem para o servidor
        response = self.__client.recv(2048).decode()
        self.__client.close() # fecha a conexão
        return response # retorna a resposta
