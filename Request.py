"""
Nome: Ramon Oliveira de Azevedo
DRE: 120023419
Ciência da Computação
8° Período
REDES DE COMPUTADORES I
"""

class Request:
    MENSAGEM: str = ''
    HEADERS: dict = {}
    BODY: dict = {}

    def __init__(self, mensagemRecebida: str) -> None:
        self.MENSAGEM = mensagemRecebida

        linhas = mensagemRecebida.split("\r\n")
        
        fimDosHeaders = self.getRequestHeaders(linhas)
        
        if fimDosHeaders < len(linhas):
            inicioDoBody = fimDosHeaders + 1
            if linhas[inicioDoBody] != '':
                contents = linhas[inicioDoBody].split('&')

                for content in contents:
                    KEY, VALUE = content.split('=')
                    self.BODY[KEY] = VALUE

    def getRequestHeaders(self, linhas: list[str]) -> int:
        METHOD, PATH, PROTOCOL = linhas[0].split()

        self.HEADERS['METHOD'] = METHOD
        self.HEADERS['PATH'] = PATH
        self.HEADERS['PROTOCOL'] = PROTOCOL

        contador = 1
        for linha in linhas[1:]:
            if linha == '':
                break
            
            HEADER, VALUE = linha.split(': ')
            self.HEADERS[HEADER] = VALUE
            contador += 1
        
        return contador
