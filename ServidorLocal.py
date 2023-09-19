"""
Nome: Ramon Oliveira de Azevedo
DRE: 120023419
Ciência da Computação
8° Período
REDES DE COMPUTADORES I
"""

import socket
import math
import re
import os
from Request import Request
from Response import Response

class ServidorLocal:
    FORMATO: str = 'UTF-8'
    PATH_PASTA_PUBLIC = 'public'
    PORTA_DO_SERVIDOR = None
    IP_DO_SERVIDOR = None
    TAM_BUFFER: int = 4096
    PATH_DO_SERVIDOR: str = ''

    pathDoServidorVar: str

    def __init__(self) -> None:
        self.pathDoServidorVar = os.path.dirname(__file__)
        self.defineValorDaConstantePathDoServidor()
        pass

    def realizaConexao(self, porta_servidor: int, ip_servidor: str|None = None) -> None:
        self.PORTA_DO_SERVIDOR = porta_servidor

        if ip_servidor is None:
            self.IP_DO_SERVIDOR = socket.gethostbyname(socket.gethostname())
        else:
            self.IP_DO_SERVIDOR = ip_servidor

        self.SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.SERVER.bind((self.IP_DO_SERVIDOR, self.PORTA_DO_SERVIDOR))

        print("Servidor está sendo inicializado...")
        self.SERVER.listen(1)

        while True:
            print(f"O servidor está no endereço {self.IP_DO_SERVIDOR}:{self.PORTA_DO_SERVIDOR}")

            conexaoDoSocket, addr = self.SERVER.accept()
            print(f"A nova conexão {addr} foi conectada.")

            try:
                linhaDaMensagemRetornada = conexaoDoSocket.recv(self.TAM_BUFFER)

                if not len(linhaDaMensagemRetornada):
                    conexaoDoSocket.close()
                    continue

                mensagemRecebida = linhaDaMensagemRetornada.decode(self.FORMATO)

                request = Request(mensagemRecebida)

                response = self.trataMetodo(request)

                self.enviaResposta(conexaoDoSocket, response)
                conexaoDoSocket.close()
            except IOError:
                response = Response().retornouNotFound()
                
                self.enviaResposta(conexaoDoSocket, response)
                conexaoDoSocket.close()

    def enviaResposta(self, conexaoDoSocket: socket.socket, response: Response) -> None:
        resultado: str = response.HEADERS['PROTOCOL'] + ' ' + response.HEADERS['STATUS_CODE'] + ' ' + response.HEADERS['STATUS_MESSAGE'] + '\r\n'
        
        for header, value in response.HEADERS.items():
            if header == 'PROTOCOL' or header == 'STATUS_CODE' or header == 'STATUS_MESSAGE' or header == 'body':
                continue

            resultado += header + ': ' + value + '\r\n'
        resultado += '\r\n'

        conexaoDoSocket.send(resultado.encode(self.FORMATO))

        if response.BODY is None:
            if response.HEADERS['STATUS_CODE'] == '404':
                pathDoArquivo = os.path.join(self.PATH_DO_SERVIDOR, self.PATH_PASTA_PUBLIC, '404.html')
                response.Content(pathDoArquivo, '.html', self.FORMATO)
            elif response.HEADERS['STATUS_CODE'] == '401':
                pathDoArquivo = os.path.join(self.PATH_DO_SERVIDOR, self.PATH_PASTA_PUBLIC, '401.html')
                response.Content(pathDoArquivo, '.html', self.FORMATO)

        if response.BODY is not None:
            bodyDaPagina = response.BODY.encode(self.FORMATO)
            pacotes = math.ceil(len(bodyDaPagina) / self.TAM_BUFFER)

            for pacote in range(pacotes):
                comeco = pacote * self.TAM_BUFFER
                fim = comeco + self.TAM_BUFFER
                conexaoDoSocket.send(bodyDaPagina[comeco: fim])

    def trataMetodo(self, request: Request) -> Response:
        if request.HEADERS['METHOD'] == 'GET':
            return self.resolveMetodoGET(request)
        elif request.HEADERS['METHOD'] == 'POST':
            return self.resolveMetodoPOST(request)
        return None
    
    def resolveMetodoGET(self, request: Request) -> Response:
        _, extensaoDoArquivo = os.path.splitext(request.HEADERS['PATH'])
        objetoValido = re.search('\.(html|js|css|ico|svg)', extensaoDoArquivo)
        paths = request.HEADERS['PATH'].split('/')

        if objetoValido == None:
            if os.path.isdir(paths[len(paths) - 1]) or request.HEADERS['PATH'] == '/':
                filePath = os.path.join(self.PATH_DO_SERVIDOR, self.PATH_PASTA_PUBLIC, *request.HEADERS['PATH'].split('/'), 'index.html')
                if os.path.exists(filePath):
                    response = Response()
                    response = response.retornouComSucesso()
                    response = response.Content(filePath, '.html', self.FORMATO)
                    return response
                else:
                    response = Response()
                    return response.retornouNotFound()
            else:
                response = Response()
                return response.retornouNotFound()
        
        caminhoDoArquivo = os.path.join(self.PATH_DO_SERVIDOR, self.PATH_PASTA_PUBLIC, *paths)
        
        if os.path.exists(caminhoDoArquivo):
            return Response().retornouComSucesso().Content(caminhoDoArquivo, extensaoDoArquivo, self.FORMATO)
        else:
            return Response().retornouNotFound()           
    
    def resolveMetodoPOST(self, request: Request) -> Response:
        if request.HEADERS['PATH'] == '/submit':
            if request.BODY['nome'] == 'Ramon' and request.BODY['senha'] == '12345':
                return Response().retornouRedirecionamento(to='pagina.html')
            else:
                return Response().retornouNaoAutorizado()
    
    def defineValorDaConstantePathDoServidor(self):
        self.PATH_DO_SERVIDOR = os.path.dirname(__file__)

    def setPathDoServidorVar(self, pathDoServidorVar):
        self.pathDoServidorVar = pathDoServidorVar
    
    def getPathDoServidorVar(self):
        return self.pathDoServidorVar