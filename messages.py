from socket import inet_aton, inet_ntoa
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

def query_encode(infoSocket, TTL, lst):
    """
    Cria e retorna uma mensagem do tipo Query: 
        2 bytes, representando o 2 (código da mensagem)
        4 bytes, representando IP do socket passado
        2 bytes, representando o porto do socket passado
        2 bytes, representando o TTL a ser enviado
        2 bytes, representando quantas chunks na lista
        2 bytes * len(lst), representando a lista em bytearray
    """
    ba = bytearray()
    ba.extend((2).to_bytes(length=2, byteorder='big'))
    ba.extend(inet_aton(infoSocket[0]))
    ba.extend(infoSocket[1].to_bytes(length=2, byteorder='big'))
    ba.extend(TTL.to_bytes(length=2, byteorder='big'))
    ba.extend(listByteEncoder(lst))
    return ba

def query_decode(msg):
    """
    Decodifica uma mensagem em binário do tipo Query.
    Verifica seu id, levanta uma exceção se houver algo errado
    Retorna uma tupla: (IP, porto, TTL, lista)
    """
    assert msgId(msg) == 2
    ip = inet_ntoa(msg[2:6])
    porto = int.from_bytes(msg[6:8], "big")
    ttl = int.from_bytes(msg[8:10], "big")
    lst = listByteDecoder(msg[10:])
    return (ip, porto, ttl, lst)

def response_encode():
    pass

def response_decode():
    pass
