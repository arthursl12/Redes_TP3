from common import listByteDecoder, listByteEncoder, msgId, messageList

"""
Mensagens e seus códigos:
Hello       1
Get         4
Chunk_info  3
Query       2
"""
def hello_encode(lst):
    """
    Cria e retorna uma mensagem do tipo Hello: 
        2 bytes, representando o 1 (código da mensagem)
        2 bytes, representando quantas chunks na lista lst
        2 bytes * len(lst), representando a lista em bytearray
    """
    return messageList(1,lst)

def hello_decode(msg):
    """
    Decodifica uma mensagem em binário do tipo Hello.
    Verifica seu id e tamanho, levanta uma exceção se houver algo errado
    Retorna a lista contida na mensagem
    """
    assert msgId(msg) == 1
    return listByteDecoder(msg[2:])

def get_encode(lst):
    """
    Cria e retorna uma mensagem do tipo Get: 
        2 bytes, representando o 4 (código da mensagem)
        2 bytes, representando quantas chunks na lista lst
        2 bytes * len(lst), representando a lista em bytearray
    """
    return messageList(4,lst)

def get_decode(msg):
    """
    Decodifica uma mensagem em binário do tipo Get.
    Verifica seu id e tamanho, levanta uma exceção se houver algo errado
    Retorna a lista contida na mensagem
    """
    assert msgId(msg) == 4
    return listByteDecoder(msg[2:])

def chunk_info_encode(lst):
    """
    Cria e retorna uma mensagem do tipo Chunk_info: 
        2 bytes, representando o 3 (código da mensagem)
        2 bytes, representando quantas chunks na lista lst
        2 bytes * len(lst), representando a lista em bytearray
    """
    return messageList(3,lst)

def chunk_info_decode(msg):
    """
    Decodifica uma mensagem em binário do tipo Chunk_info.
    Verifica seu id e tamanho, levanta uma exceção se houver algo errado
    Retorna a lista contida na mensagem
    """
    assert msgId(msg) == 3
    return listByteDecoder(msg[2:])

def query_encode():
    pass

def query_decode():
    pass

def response_encode():
    pass

def response_decode():
    pass
