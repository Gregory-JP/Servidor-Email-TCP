from menu import *
from client import Client

client = Client('127.0.0.1', 3000) # cria um cliente

print(f'\033[;1m{"-"*30 + "Bem vindo ao server" + "-"*30 + "":^50}\033[m') # imprime o cabeçalho do menu

# codigo:email:password:id_mensagem:assunto:corpo:destinatario

while True:
    MenuLogin()
    operation = str(input('\033[1;96mDigite a opção desejada: \033[m'))

    # login
    if operation == '1':

        user = str(input('Digite o seu login: ')).lower() # pega o login do usuario
        password = str(input('Digite a sua senha: ')) # pega a senha do usuario
        response = client.send(f'2:{user}:{password}:false:false:false:false')
        expected = '\033[1;32mLogin realizado com sucesso!\033[m'

        if response == expected: # se o login foi realizado com sucesso
            print(response)
            print(f'\033[1;33m{"-"*33 + f"Bem vind@ {user}" + "-"*32 + "":^50}\033[m')

            while True:
                # menu de opções
                MenuMaster()
                operation_master = str(input('\033[1;96mDigite a opção desejada: \033[m'))
                
                if operation_master == '1': # caixa de entrada
                    print(f'\033[1;33m{"-"*30 + "Caixa de entrada" + "-"*30 + "":^50}\033[m')
                    print(client.send(f'4:{user}:false:false:false:false:false')) # envia a mensagem para o servidor
                    print('\033[1;33m-'*76 + '\033[m')

                elif operation_master == '2': # ver mensagem
                    print(f'\033[1;33m{"-"*33 + "Ver mensagens" + "-"*32 + "":^50}\033[m')
                    response = client.send(f'4:{user}:false:false:false:false:false') 
                    unexpected = '\033[;1m\033[1;31mVocê não tem mensagens\033[m' # mensagem de erro
                    print(response)

                    # se a resposta do servidor não for a mensagem esperada
                    if(response != unexpected):
                        id_msg = int(input('\033[1;96mDigite a posição da mensagem: \033[m'))
                        print(client.send(f'5:{user}:false:{id_msg-1}:false:false:false'))
                    
                    print('\033[1;33m-'*70 + '\033[m') # fim do menu de ver mensagem

                elif operation_master == '3': # enviar mensagem
                    print(f'\033[1;33m{"-"*33 + "Enviar mensagem" + "-"*32 + "":^50}\033[m')
                    
                    receiver = str(input('\033[1;96mDigite o email do destinatário: \033[m')).lower() # email do destinatário
                    subject = str(input('\033[1;96mDigite o assunto: \033[m')) # assunto
                    body = str(input('\033[1;96mDigite o corpo: \033[m')) # corpo
                    
                    if len(receiver) == 0 or '@' not in receiver: # se o email do destinatário não for válido
                        print('\033[;1m\033[1;31mVocê não informou um destinatario válido!\033[m')
                    elif len(subject) == 0:
                        print('\033[;1m\033[1;31mVocê não informou nenhum assunto!\033[m') # se o assunto não for válido
                    elif len(body) == 0:
                        print('\033[;1m\033[1;31mVocê não informou nenhuma mensagem!\033[m') # se a mensagem não for válida
                    else:
                        print(client.send(f'8:{user}:false:false:{subject}:{body}:{receiver}')) # envia a mensagem para o servidor
                    print('\033[1;33m-'*76 + '\033[m')

                elif operation_master == '4': # deletar mensagem
                    print(f'\033[1;33m{"-"*33 + "Deletar mensagens" + "-"*30 + "":^50}\033[m')
                    print(client.send(f'4:{user}:false:false:false:false:false')) # envia a mensagem para o servidor

                    id_msg = int(input('\033[1;96mDigite a posição da mensagem: \033[m'))
                    print(client.send(f'6:{user}:false:{id_msg-1}:false:false:false'))
                    print('\033[1;33m-'*76 + '\033[m')
       
                elif operation_master == '5': # limpar caixa de entrada
                    print(f'\033[1;33m{"-"*30 + "Limpar caixa de entrada" + "-"*30 + "":^50}\033[m')
                    print(client.send(f'7:{user}:false:false:false:false:false')) # envia a mensagem para o servidor
                    print('\033[1;33m-'*76 + '\033[m')

                elif operation_master == '6': # logout
                    print(client.send(f'3:{user}:false:false:false:false:false'))
                    break

                else:
                    # se a opção for inválida
                    print('\033[;1m\033[1;31mDigite uma opção válida!\033[m')

        else:
            # se o login não foi realizado com sucesso
            print('\033[;1m\033[1;31mLogin ou senha incorretos!\033[m')

    # register
    elif operation == '2':
        user = str(input('Digite o seu usuário: ')).lower().split('@') # email do usuário
        password = str(input('Digite a sua senha: ')) # recebe a senha

        if password == user:
            print('\033[;1m\033[1;31mSenha não pode ser igual ao login!\033[m') # se a senha for igual ao login
        else:
            print(client.send(f'1:{user[0]}:{password}:false:false:false:false')) # envia a mensagem para o servidor
