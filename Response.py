"""
Nome: Ramon Oliveira de Azevedo
DRE: 120023419
Ciência da Computação
8° Período
REDES DE COMPUTADORES I
"""

from typing import Self

class Response:
    HEADERS: dict = {}
    BODY: str|None = None

    def __init__(self) -> None:
        self.HEADERS['PROTOCOL'] = 'HTTP/1.1'
        self.HEADERS['Connection'] = "close"
    
    def retornouComSucesso(self) -> Self:
        self.HEADERS['STATUS_CODE'] = '200'
        self.HEADERS['STATUS_MESSAGE'] = 'OK'
        return self
    
    def retornouRedirecionamento(self, to: str) -> Self:
        self.HEADERS['STATUS_CODE'] = '301'
        self.HEADERS['STATUS_MESSAGE'] = 'Moved Permanently'
        self.HEADERS['Location'] = to
        return self
    
    def retornouNaoAutorizado(self) -> Self:
        self.HEADERS['STATUS_CODE'] = '401'
        self.HEADERS['STATUS_MESSAGE'] = 'Unauthorized'
        return self    
    
    def retornouAcessoProibido(self) -> Self:
        self.HEADERS['STATUS_CODE'] = '403'
        self.HEADERS['STATUS_MESSAGE'] = 'Forbidden'
        return self
    
    def retornouNotFound(self) -> Self:
        self.HEADERS['STATUS_CODE'] = '404'
        self.HEADERS['STATUS_MESSAGE'] = 'Not Found'
        return self
    
    def tempoDeRequisicaoFoiEsgotado(self) -> Self:
        self.HEADERS['STATUS_CODE'] = '408'
        self.HEADERS['STATUS_MESSAGE'] = 'Request Timeout'
        return self
    
    def retornouErroInternoDoServidor(self, to: str) -> Self:
        self.HEADERS['STATUS_CODE'] = '500'
        self.HEADERS['STATUS_MESSAGE'] = 'Internal Server Error'
        return self

    def Content(self, caminhoDoArquivo: str, extensao: str, formato: str) -> Self:
        body = open(caminhoDoArquivo, encoding=formato).read()

        self.HEADERS['Content-Length'] = str(len(body.encode(formato)))

        if extensao == '.js':
            self.HEADERS['Content-Type'] = 'text/javascript; charset=' + formato
        elif extensao == '.css':
            self.HEADERS['Content-Type'] = 'text/css; charset=' + formato
        elif extensao == '.html':
            self.HEADERS['Content-Type'] = 'text/html; charset=' + formato
        elif extensao == '.svg':
            self.HEADERS['Content-Type'] = 'image/svg+xml; charset=' + formato
        elif extensao == '.png':
            self.HEADERS['Content-Type'] = 'image/png+xml; charset=' + formato
        elif extensao == '.jpg':
            self.HEADERS['Content-Type'] = 'image/jpg+xml; charset=' + formato
        elif extensao == '.jpeg':
            self.HEADERS['Content-Type'] = 'image/jpeg+xml; charset=' + formato
        
        self.BODY = body
        
        return self
    