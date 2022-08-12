class Response:
    def __init__(self, type, message, data=False):
        self.type = type
        self.message = message
        self.data = data

    def __convert(self):
        """
        Tratamento de erros e formatação da mensagem
        """
        if self.type == 'Error':
            self.message = '\033[;1m\033[1;31m' + self.message + '\033[m' # formatação de error
        else:
            self.message = '\033[1;32m' + self.message + '\033[m' # formatação de success

    def value(self):
        """
        Chama a função de conversão e retorna a mensagem
        """
        self.__convert()
        return self.message
