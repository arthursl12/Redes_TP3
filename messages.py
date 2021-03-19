import os
from socket import inet_aton, inet_ntoa

from common import listByteDecoder, listByteEncoder, messageList, msgId

MAX_PAYLOAD_SIZE = 1024

"""
Mensagens e seus códigos:
Hello       1
Get         4
Chunk_info  3
Query       2
Response    5
"""
def hello_encode(lst):
    """
    Cria e retorna uma mensagem do tipo Hello: 
        2 bytes, representando o 1 (código da mensagem); 
        2 bytes, representando quantas chunks na lista lst; 
        2 bytes * len(lst), representando a lista em bytearray; 
    """
    return messageList(1,lst)

def hello_decode(msg):
    """
    Decodifica uma mensagem em binário do tipo Hello.
    Verifica seu id e tamanho, levanta uma exceção se houver algo errado. 
    Retorna a lista contida na mensagem.
    """
    assert msgId(msg) == 1
    return listByteDecoder(msg[2:])

def get_encode(lst):
    """
    Cria e retorna uma mensagem do tipo Get: 
        2 bytes, representando o 4 (código da mensagem); 
        2 bytes, representando quantas chunks na lista lst; 
        2 bytes * len(lst), representando a lista em bytearray.
    """
    return messageList(4,lst)

def get_decode(msg):
    """
    Decodifica uma mensagem em binário do tipo Get.
    Verifica seu id e tamanho, levanta uma exceção se houver algo errado. 
    Retorna a lista contida na mensagem.
    """
    assert msgId(msg) == 4
    return listByteDecoder(msg[2:])

def chunk_info_encode(lst):
    """
    Cria e retorna uma mensagem do tipo Chunk_info: 
        2 bytes, representando o 3 (código da mensagem); 
        2 bytes, representando quantas chunks na lista lst; 
        2 bytes * len(lst), representando a lista em bytearray.
    """
    return messageList(3,lst)

def chunk_info_decode(msg):
    """
    Decodifica uma mensagem em binário do tipo Chunk_info.
    Verifica seu id e tamanho, levanta uma exceção se houver algo errado. 
    Retorna a lista contida na mensagem. 
    """
    assert msgId(msg) == 3
    return listByteDecoder(msg[2:])

def query_encode(infoSocket, TTL, lst):
    """
    Cria e retorna uma mensagem do tipo Query: 
        2 bytes, representando o 2 (código da mensagem); 
        4 bytes, representando IP do socket passado; 
        2 bytes, representando o porto do socket passado; 
        2 bytes, representando o TTL a ser enviado; 
        2 bytes, representando quantas chunks na lista; 
        2 bytes * len(lst), representando a lista em bytearray.
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
    Verifica seu id, levanta uma exceção se houver algo errado. 
    Retorna uma tupla: (IP, porto, TTL, lista).
    """
    assert msgId(msg) == 2
    ip = inet_ntoa(msg[2:6])
    porto = int.from_bytes(msg[6:8], "big")
    ttl = int.from_bytes(msg[8:10], "big")
    lst = listByteDecoder(msg[10:])
    return (ip, porto, ttl, lst)

def response_encode(chunk_id, chunk_size, filename, file_extension):
    """
    Cria e retorna uma mensagem binária do tipo Response: 
        2 bytes, representando o 5 (código da mensagem); 
        2 bytes, representando o id da chunk a ser enviada; 
        2 bytes, representando o tamanho da chunk a ser enviada (<= 1024); 
        n bytes, a chunk em si (<= 1024 bytes).
    """
    assert chunk_size <= MAX_PAYLOAD_SIZE
    
    ba = bytearray()
    ba.extend((5).to_bytes(length=2, byteorder='big'))          # id
    ba.extend(chunk_id.to_bytes(length=2, byteorder='big'))     # chunk_id
    ba.extend(chunk_size.to_bytes(length=2, byteorder='big'))   # chunk_size
    
    # Carrega a chunk do arquivo
    with open(f"{filename}_{chunk_id}.{file_extension}",'rb') as file:
        pl = file.read(chunk_size)
    pl = bytearray(pl)
    ba.extend(pl)
    
    return ba

def response_decode(msg, outputFolder="", filename="chunk"):
    """
    Decodifica uma mensagem em binário do tipo Response. 
    Verifica seu id e tamanho, levanta uma exceção se houver algo errado. 
    Já escreve o arquivo com payload da chunk na pasta raiz por padrão.
    Retorna o id do chunk escrito e se a operação teve sucesso (booleano).  
    """
    assert msgId(msg) == 5
    chunk_id = int.from_bytes(msg[2:4], "big")
    chunk_size = int.from_bytes(msg[4:6], "big")
    if len(outputFolder)>0 and not os.path.exists(outputFolder):
        os.makedirs(outputFolder)
    with open(f"{outputFolder}/{filename}{chunk_id}.m4s", "wb") as file:
        pl = bytearray(msg[6:])
        file.write(pl)
    return (chunk_id, True)
