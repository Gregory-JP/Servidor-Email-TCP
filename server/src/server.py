import threading
import socket
from .response import Response
from .main import Main
from .client import Client
import json

class Server():
    def __init__(self, host='127.0.0.1', port=3000, domain='@admin.com'):
        self._HOST = host
        self._PORT = port
        self._DOMAIN = domain
        self.__server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__server.bind((host, port))
        self.__DNS = {}
        self.__loggedIn = []
        self.__read_dns()

    def __read_dns(self):
        """
        Função para ler o arquivo de servidores e registrar no contrutor do server os servidores conhecidos
        Nesta função é necessario informar o caminho do arquivo. Cuidar para que todos os servidores 
        tenha o mesmo arquivo, pois ainda n temos um servidor DNS, se desse tempo seria implmentado :/
        """
        try:
            with open(f'PATH/redes/server/database/servers.json', 'r') as f:
                if not f:
                    f.create_file()
                self.__DNS = json.load(f)
        except FileNotFoundError as Error:
            return print(Error)

    def __save_dns(self):
        """
        Essa função serve para salvar um novo servidor no arquivo de DNS, 
        que é chamada sempre que um server é iniciado
        """
        self.__DNS[self._DOMAIN] = {"host": self._HOST, "port": self._PORT, "domain": self._DOMAIN}
        with open('PATH/redes/server/database/servers.json', 'w') as file:
            json.dump(self.__DNS, file)

    def __verify_domain(self,domain):
        """
        Essa função diz se o dominio do servidor é igual ao dominio recebido
        """
        return self._DOMAIN == domain

    def __verify_dns(self, domain):
        return domain in self.__DNS

    def __verify_login(self,user):
        """
        Essa função diz se o user percente a lista de usuarios logados
        """
        return user in self.__loggedIn

    def start(self):
        """
        Função responsável por abrir a comunicação, deixar o servidor ouvindo
        ela usa de Thread para que possa se comunicar com usuários diferentes de forma simultânea
        """
        self.__save_dns()
        self.__server.listen()
        print(f'Server ouvindo em {self._HOST} na porta {self._PORT}')
        
        while True: # loop infinito para ouvir os clientes
            conn, addr = self.__server.accept()
            thread = threading.Thread(target=self.__connect(conn, addr))
            thread.start()

    def __connect(self, conn, addr):
        """
        Função principal, a que responde a uma conexão
        o server irá receber uma mensagem e baseado nos codigos faz determinada operação
        a comunicação possui um padrao, que você pode analisar no arquivo de anotacoes.txt
        """
        while True:
            print(f'Conetado com {addr}')
            msg = conn.recv(2048)
            if not msg:
                break
            
            msg = msg.decode()
            msg = msg.split(':')

            code = msg[0]
            email = msg[1]
            password = msg[2]
            id_msg = msg[3]
            subject = msg[4]
            body = msg[5]
            receiver = msg[6]
            
            print(f'Operação para o codigo: {code}')

            if code == '1': # register
                response = Main(self._DOMAIN.replace("@","")).register(email, password) # chama a função de registro
                response = Response(response.type, response.message).value().encode()
                conn.send(response)
                break

            elif code == '2': # login
                response = Main(self._DOMAIN.replace("@","")).login(email, password) # chama a função de login
                
                if response.type == "Sucess":
                    self.__loggedIn.append(email)

                response = Response(response.type, response.message).value().encode()
                conn.send(response)
                break
                
            elif code == '3': # logout
                if self.__verify_login(email):
                    self.__loggedIn.remove(email)
                    response = Response('Sucess','Deslogado com sucesso!').value().encode()
                else:
                     response = Response('Error','Erro ao deslogar, user não estava logado!').value().encode()
                conn.send(response)
                break

            elif code == '4': # caixa de entrada
                response = Main(self._DOMAIN.replace("@","")).see_messages(email) # chama a função de caixa de entrada
                if self.__verify_login(email):
                    if response.type == "Sucess":
                        response = Response('Sucess', response.data).value().encode()
                    else:
                        response = Response('Error', response.message).value().encode()
                else:
                    response = Response('Error','User não estava logado!').value().encode()
                conn.send(response)
                break

            elif code == '5': # ver mensagens
                response = Main(self._DOMAIN.replace("@","")).full_message(email, id_msg) # chama a função de ver mensagem
                if self.__verify_login(email):
                    if response.type == 'Sucess':
                        response = Response('Sucess', response.data).value().encode()
                    else:
                        response = Response('Error', response.message).value().encode()
                else:
                    response = Response('Error','User não estava logado!').value().encode()
                conn.send(response)
                break

            elif code == '6': # deletar mensagem
                if self.__verify_login(email):
                    response = Main(self._DOMAIN.replace("@","")).delete_message(email, id_msg).value().encode() # chama a função de deletar mensagem
                else:
                    response = Response('Error','User não estava logado!').value().encode()
                conn.send(response)
                break

            elif code == '7': # limpar caixa de entrada
                if self.__verify_login(email):
                    response = Main(self._DOMAIN.replace("@","")).clear_messages(email).value().encode() # chama a função de limpar caixa de entrada
                else:
                    response = Response('Error','User não estava logado!').value().encode()
                conn.send(response)
                break

            elif code == '8': # enviar mensagem
                domain = '@'+ receiver.split("@")[1]

                # sevidor não registrado
                if not self.__verify_dns(domain):
                    response = Main(self._DOMAIN.replace("@","")).send_message('System', email, 'Erro ao enviar!', 'Destinatário não existe!')
                    response = Response('Error', 'Verifique sua caixa de entrada!').value().encode()
                    conn.send(response)
                    break
                
                # quando o usuário logado pertence ao servidor de origem
                elif self.__verify_domain(domain):
                        receiver = receiver.split("@")[0] # pega o nome do usuário
                        response = Main(self._DOMAIN.replace("@","")).send_message(email, receiver, subject, body)

                        # quando os dois usuários estão no mesmo servidor, porém o usuário de destino não existe
                        if response.type == 'Error' and response.message == 'O destinatário não está cadastrado!':
                            response = Main(self._DOMAIN.replace("@","")).send_message('System', email, 'Erro ao enviar!', 'Destinatário não existe!')
                            response = Response('Error', 'Verifique sua caixa de entrada!').value().encode()
                            conn.send(response)
                            break
                        
                        # usuário logado não existe porque vem de outro sevidor
                        elif response.type == 'Error' and response.message == 'Você não está cadastrado!':
                            conn.send('Verifique sua caixa de entrada!'.encode()) # envia mensagem de erro
                            break
                            
                        else:
                            conn.send(response.value().encode()) # envia a resposta
                            break
                
                # quando o destino é um servidor estrangeiro
                else:
                        msg = f'8:{email}:false:false:{subject}:{body}:{receiver}'
                        server =  self.__DNS[domain] # pega o servidor do destino
                        print(f'Mensagem encaminhada para o servidor {server["domain"].replace("@","")}')
                        client = Client(server["host"], server["port"])
                        
                        # mensagem do servidor
                        print(client.send(msg)) 

                        if client.send(msg) == '\033[;1m\033[1;31mVerifique sua caixa de entrada!\033[m': 
                            Main(self._DOMAIN.replace("@","")).send_message('System', email, 'Erro ao enviar!', 'Destinatário não existe!')
                            conn.send(Response('Error', 'Verifique sua caixa de entrada!').value().encode()) # envia mensagem de erro
                            break

                        else:
                            # caso tudo ocorra da maneira correta, a mensagem é enviada
                            conn.send(Response('Sucess', 'Mensagem enviada com sucesso!').value().encode())
                            break

        print(f'Desconectado de {addr}')
        conn.close() # encerra a conexão
