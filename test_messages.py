from common import listToBytes, msgId
import pytest
import binascii
import messages

            
class TestId:
    def test_msgId(self):
        assert msgId(messages.hello_encode([1,2,3])) == 1
        assert msgId(messages.get_encode([1])) == 4
        assert msgId(messages.info_file_encode("teste1.txt",135)) == 3
        assert msgId(messages.ok_encode()) == 4
        assert msgId(messages.fim_encode()) == 5
        assert msgId(messages.ack_encode(0)) == 7

class TestHelloEncode:
    def test_hello_msg_varios(self):
        ba = bytearray()
        ba.extend((1).to_bytes(length=2, byteorder='big'))
        ba.extend((3).to_bytes(length=2, byteorder='big'))
        ba.extend(listToBytes([3,1,2]))
        assert ba == messages.hello_encode([3,1,2])
    
    def test_hello_msg_unico(self):
        ba = bytearray()
        ba.extend((1).to_bytes(length=2, byteorder='big'))
        ba.extend((1).to_bytes(length=2, byteorder='big'))
        ba.extend(listToBytes([3]))
        assert ba == messages.hello_encode([3])
    
    def test_hello_msg_vazio(self):
        ba = bytearray()
        ba.extend((1).to_bytes(length=2, byteorder='big'))
        ba.extend((0).to_bytes(length=2, byteorder='big'))
        assert ba == messages.hello_encode([])
    
    def test_hello_decode(self):
        lst = messages.hello_decode(messages.hello_encode([3,1,2]))
        assert lst == [3,1,2]
        
        lst = messages.hello_decode(messages.hello_encode([3]))
        assert lst == [3]
        
        lst = messages.hello_decode(messages.hello_encode([]))
        assert lst == []

class TestGetEncode:
    def test_hello_msg_varios(self):
        ba = bytearray()
        ba.extend((4).to_bytes(length=2, byteorder='big'))
        ba.extend((3).to_bytes(length=2, byteorder='big'))
        ba.extend(listToBytes([3,1,2]))
        assert ba == messages.get_encode([3,1,2])
    
    def test_hello_msg_unico(self):
        ba = bytearray()
        ba.extend((4).to_bytes(length=2, byteorder='big'))
        ba.extend((1).to_bytes(length=2, byteorder='big'))
        ba.extend(listToBytes([3]))
        assert ba == messages.get_encode([3])
    
    def test_hello_msg_vazio(self):
        ba = bytearray()
        ba.extend((4).to_bytes(length=2, byteorder='big'))
        ba.extend((0).to_bytes(length=2, byteorder='big'))
        assert ba == messages.get_encode([])
    
    def test_hello_decode(self):
        lst = messages.get_decode(messages.get_encode([3,1,2]))
        assert lst == [3,1,2]
        
        lst = messages.get_decode(messages.get_encode([3]))
        assert lst == [3]
        
        lst = messages.get_decode(messages.get_encode([]))
        assert lst == []
    
# class TestOk:
#     def test_ok_msg(self):
#         ba = bytearray()
#         i = 4
#         ba.extend(i.to_bytes(length=2, byteorder='big'))
#         assert ba == messages.ok_encode()
    
#     def test_ok_decode(self):
#         messages.ok_decode(messages.ok_encode())
#         with pytest.raises(Exception) as e_info:
#             ba = bytearray()
#             i = 80
#             ba.extend(i.to_bytes(length=2, byteorder='big'))
#             messages.ok_decode(ba)

# class TestFim:
#     def test_fim_msg(self):
#         ba = bytearray()
#         i = 5
#         ba.extend(i.to_bytes(length=2, byteorder='big'))
#         assert ba == messages.fim_encode()
    
#     def test_fim_decode(self):
#         messages.fim_decode(messages.fim_encode())
#         with pytest.raises(Exception) as e_info:
#             ba = bytearray()
#             i = 80
#             ba.extend(i.to_bytes(length=2, byteorder='big'))
#             messages.fim_decode(ba)

# class TestAck:
#     def test_ack_msg(self):
#         ba = bytearray()
#         i = 7
#         ba.extend(i.to_bytes(length=2, byteorder='big'))
#         i = 10
#         ba.extend(i.to_bytes(length=4, byteorder='big'))
#         assert ba == messages.ack_encode(10)
    
#     def test_ack_decode(self):
#         assert messages.ack_decode(messages.ack_encode(10)) == 10
#         with pytest.raises(Exception) as e_info:
#             ba = bytearray()
#             i = 80
#             ba.extend(i.to_bytes(length=2, byteorder='big'))
#             i = 10
#             ba.extend(i.to_bytes(length=4, byteorder='big'))
#             messages.ack_decode(ba)
# class TestConnection:
#     def test_connection_msg(self):
#         ba = bytearray()
#         i = 2
#         ba.extend(i.to_bytes(length=2, byteorder='big'))
#         i = 40214
#         ba.extend(i.to_bytes(length=4, byteorder='big'))
#         assert ba == messages.connection_encode(40214)
    
#     def test_connection_msg_error(self):
#         with pytest.raises(Exception) as e_info:
#             messages.connection_encode(-20)
    
#     def test_connection_decode(self):
#         msg = messages.connection_encode(40214)
#         assert messages.connection_decode(msg) == 40214

# class TestInfoFile:
#     def test_info_file_encode(self):
#         # Id da mensagem
#         ba = bytearray()
#         i = 3
#         ba.extend(i.to_bytes(length=2, byteorder='big'))
        
#         # Nome do arquivo (máximo 15 bytes)
#         string = "teste1.txt"
#         b_str = string.encode("ascii")
#         print (len(b_str))
        
#         # Completa com zeros até 15 bytes
#         filler = bytearray(messages.MAX_FILENAME_SIZE - len(b_str))
#         ba.extend(filler)
#         ba.extend(b_str)
        
#         # Coloca o tamanho do arquivo
#         tam = 135
#         ba.extend(tam.to_bytes(length=8, byteorder='big'))
        
#         # print(len(ba))
#         # print(binascii.hexlify(ba,","))
#         assert ba == messages.info_file_encode("teste1.txt",135)
    
#     def test_info_file_encode_without_filler(self):
#         # Id da mensagem
#         ba = bytearray()
#         i = 3
#         ba.extend(i.to_bytes(length=2, byteorder='big'))
        
#         # Nome do arquivo (máximo 15 bytes)
#         string = "nomemtlongo.txt"
#         b_str = string.encode("ascii")
#         print (len(b_str))
        
#         # Completa com zeros até 15 bytes
#         # filler = bytearray(messages.MAX_FILENAME_SIZE - len(b_str))
#         # ba.extend(filler)
#         ba.extend(b_str)
        
#         # Coloca o tamanho do arquivo
#         tam = 2200
#         ba.extend(tam.to_bytes(length=8, byteorder='big'))
                
#         # print(len(ba))
#         # print(binascii.hexlify(ba,","))
#         assert ba == messages.info_file_encode("nomemtlongo.txt",2200)
    
#     def test_info_file_encode_name_too_big(self):
#         with pytest.raises(Exception) as e_info:
#             messages.info_file_encode("nomemtlongo1.txt",2200)
    
#     def test_info_file_decode(self):
#         assert messages.info_file_decode(
#                     messages.info_file_encode("teste1.txt",135)
#                 ) \
#                 == ("teste1.txt",135)
#         assert messages.info_file_decode(
#                     messages.info_file_encode("nomemtlongo.txt",2200)
#                 ) \
#                 == ("nomemtlongo.txt",2200)
        