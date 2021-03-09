from common import listByteDecoder, listByteEncoder, msgId


def hello_encode(lst):
    """
    Cria e retorna uma mensagem do tipo Hello: 
        2 bytes, representando o 1 (código da mensagem)
        2 bytes, representando quantas chunks na lista lst
        2 bytes * len(lst), representando a lista em bytearray
    """
    ba = bytearray()
    ba.extend((1).to_bytes(length=2, byteorder='big'))
    ba.extend(listByteEncoder(lst))
    return ba

def hello_decode(msg):
    """
    Decodifica uma mensagem em binário do tipo Hello.
    Verifica seu id e tamanho, levanta uma exceção se houver algo errado
    Retorna a lista contida na mensagem
    """
    assert msgId(msg) == 1
    return listByteDecoder(msg[2:])

def get_encode():
    pass

def get_decode():
    pass

def query_encode():
    pass

def query_decode():
    pass

def chunk_info_encode():
    pass

def chunk_info_decode():
    pass

def response_encode():
    pass

def response_decode():
    pass
