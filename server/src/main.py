import json
from .response import Response

class Main:
    """
    contrutor da main
    """
    def __init__(self,server):
        self.users = {}
        self.__server = server
        self.__load_users()

    def __load_users(self):
        """
        Carrega os usuários do arquivo json
        """
        try:
            
            # tenta abrir o arquivo para leitura
            with open(f'PATH/redes/server/database/{self.__server}/users.json', 'r') as f:
                if not f:
                    f.create_file()
                self.users = json.load(f)
        except FileNotFoundError as Error:
            return print(Error)

    def __save_users(self):
        """
        Salva os usuários no arquivo json
        """

        # abre o arquivo para escrita
        with open(f'PATH/redes/server/database/{self.__server}/users.json', 'w') as f:
            json.dump(self.users, f)

    def register(self, login, password):
        """
        Registra um novo usuário
        """
        try:
            if login not in self.users[login]:
                return Response('Error','Já existe um usuário com esse login!')
        
        except KeyError:
            self.users[login] = {'Password': password, 'Messages' : []} # cria um novo usuário
            self.__save_users()
            return Response('Sucess','Registro realizado com sucesso!')
    
    def login(self, login, password):
        """
        Login do usuário
        """
        if login not in self.users: # se o usuário não estiver cadastrado
            return Response(type='Error', message='Usuário não cadastrado!')
            
        elif password != self.users[login]['Password']: # se a senha não for correta
            return Response(type='Error', message='Senha Incorreta!')

        elif password == self.users[login]['Password']: # se a senha for correta
            return Response(type='Sucess', message='Login realizado com sucesso!')

        else: # se não for nenhum dos casos acima
            return Response(type='Error', message='Não foi possível realizar o login!')
    
    def see_messages(self, login):
        """
        Ver mensagens do usuário
        """
        if login not in self.users: # se o usuário não estiver cadastrado
            return Response(type='Error', message='Você não está cadastrado!')

        elif self.users[login]['Messages'] == []: # se o usuário não tiver mensagens
            return Response(type='Error', message='Você não tem mensagens!')

        else: # se o usuário tiver mensagens
            data = ''

            for i in range(len(self.users[login]['Messages'])): # percorre todas as mensagens
                data += (f'{i + 1} - Assunto: {self.users[login]["Messages"][i]["Subject"]}\n')

            return Response(type='Sucess', message='', data=data) # retorna os dados da mensagem

    def full_message(self, login, id_message):
        """
        Ver mensagem completa
        """
        if login not in self.users: # se o usuário não estiver cadastrado
            return Response(type='Error', message='Você não está cadastrado!')	

        elif not self.users[login]['Messages']: # se o usuário não tiver mensagens
            return Response(type='Error', message='Você não tem mensagens!')
        
        else:
            # percorre todas as mensagens
            return Response(type='Sucess', message='', data=
            f'De: {self.users[login]["Messages"][int(id_message)]["From"]}\n'
            f'Assunto: {self.users[login]["Messages"][int(id_message)]["Subject"]}\n'
            f'Mensagem: {self.users[login]["Messages"][int(id_message)]["Body"]}')

    def clear_messages(self, login):
        """
        Apaga todas as mensagens do usuário
        """
        if login not in self.users: # se o usuário não estiver cadastrado
            return Response(type='Error', message='Você não está cadastrado!')	

        elif not self.users[login]['Messages']: # se o usuário não tiver mensagens
            return Response(type='Error', message='Você não tem mensagens!')

        else: # se o usuário tiver mensagens, apaga todas
            self.users[login]['Messages'] = []
            self.__save_users()
            return Response(type='Sucess', message='Mensagens apagadas!')

    def send_message(self, sender, receiver, subject, body):
        """
        Envia uma mensagem
        """
        if receiver not in self.users: # se o destinatário não estiver cadastrado
            return Response(type='Error', message='O destinatário não está cadastrado!')

        else: # se o destinatário estiver cadastrado e o remetente também estiver cadastrado, envia a mensagem
            self.users[receiver]['Messages'].append({'From': str(sender), 'Subject': str(subject), 'Body': str(body)})
            self.__save_users()
            return Response(type='Sucess', message='Mensagem enviada com sucesso!')

    def delete_message(self, login, id_message):
        """
        Deleta uma mensagem
        """
        if login not in self.users: # se o usuário não estiver cadastrado
            return Response(type='Error', message='Você não está cadastrado!')	

        elif not self.users[login]['Messages']: # se o usuário não tiver mensagens
            return Response(type='Error', message='Você não tem mensagens!')
        
        else: # se o usuário tiver mensagens, deleta a mensagem selecionada pelo usuário
            self.users[login]['Messages'].pop(int(id_message))
            self.__save_users()
            return Response(type='Sucess', message='Mensagem apagada!')