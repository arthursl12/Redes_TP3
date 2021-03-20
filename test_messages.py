from common import listByteEncoder, listToBytes, msgId
import pytest
import os
import messages
import socket
            
class TestId:
    def setup_method(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind(('',0))
        self.infoS = self.s.getsockname()
    
    def teardown_method(self):
        self.s.close()
        
    def test_msgId(self):
        assert msgId(messages.hello_encode([1,2,3])) == 1
        assert msgId(messages.get_encode([1])) == 4
        assert msgId(messages.chunk_info_encode([2,5,3,67,3])) == 3
        assert msgId(messages.query_encode(self.infoS, 3, [1])) == 2
        assert msgId(messages.response_encode(1,1000,"BigBuckBunny","m4s")) == 5

class TestHello:
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

class TestGet:
    def test_get_msg_varios(self):
        ba = bytearray()
        ba.extend((4).to_bytes(length=2, byteorder='big'))
        ba.extend((3).to_bytes(length=2, byteorder='big'))
        ba.extend(listToBytes([3,1,2]))
        assert ba == messages.get_encode([3,1,2])
    
    def test_get_msg_unico(self):
        ba = bytearray()
        ba.extend((4).to_bytes(length=2, byteorder='big'))
        ba.extend((1).to_bytes(length=2, byteorder='big'))
        ba.extend(listToBytes([3]))
        assert ba == messages.get_encode([3])
    
    def test_get_msg_vazio(self):
        ba = bytearray()
        ba.extend((4).to_bytes(length=2, byteorder='big'))
        ba.extend((0).to_bytes(length=2, byteorder='big'))
        assert ba == messages.get_encode([])
    
    def test_get_decode(self):
        lst = messages.get_decode(messages.get_encode([3,1,2]))
        assert lst == [3,1,2]
        
        lst = messages.get_decode(messages.get_encode([3]))
        assert lst == [3]
        
        lst = messages.get_decode(messages.get_encode([]))
        assert lst == []

class TestChunkInfo:
    def test_chunk_info_msg_varios(self):
        ba = bytearray()
        ba.extend((3).to_bytes(length=2, byteorder='big'))
        ba.extend((3).to_bytes(length=2, byteorder='big'))
        ba.extend(listToBytes([3,1,2]))
        assert ba == messages.chunk_info_encode([3,1,2])
    
    def test_chunk_info_msg_unico(self):
        ba = bytearray()
        ba.extend((3).to_bytes(length=2, byteorder='big'))
        ba.extend((1).to_bytes(length=2, byteorder='big'))
        ba.extend(listToBytes([3]))
        assert ba == messages.chunk_info_encode([3])
    
    def test_chunk_info_msg_vazio(self):
        ba = bytearray()
        ba.extend((3).to_bytes(length=2, byteorder='big'))
        ba.extend((0).to_bytes(length=2, byteorder='big'))
        assert ba == messages.chunk_info_encode([])
    
    def test_chunk_info_decode(self):
        lst = messages.chunk_info_decode(messages.chunk_info_encode([3,1,2]))
        assert lst == [3,1,2]
        
        lst = messages.chunk_info_decode(messages.chunk_info_encode([3]))
        assert lst == [3]
        
        lst = messages.chunk_info_decode(messages.chunk_info_encode([]))
        assert lst == []

class TestQuery:
    def setup_method(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind(('',0))
        self.infoS = self.s.getsockname()
    
    def teardown_method(self):
        self.s.close()
    
    def test_query_msg_varios(self):
        ba = bytearray()
        ba.extend((2).to_bytes(length=2, byteorder='big'))  # id
        ba.extend(socket.inet_aton(self.infoS[0]))          # IP
        ba.extend(self.infoS[1].to_bytes(length=2, byteorder='big'))    # Porta
        ba.extend((1).to_bytes(length=2, byteorder='big'))  # TTL
        ba.extend(listByteEncoder([3,1,2]))                     # Lista
        assert ba == messages.query_encode(self.infoS, 1, [3,1,2])
        assert len(ba) == 2+4+2+2+2+6
    
    def test_query_msg_unico(self):
        ba = bytearray()
        ba.extend((2).to_bytes(length=2, byteorder='big'))  # id
        ba.extend(socket.inet_aton(self.infoS[0]))          # IP
        ba.extend(self.infoS[1].to_bytes(length=2, byteorder='big'))    # Porta
        ba.extend((3).to_bytes(length=2, byteorder='big'))  # TTL
        ba.extend(listByteEncoder([3]))                         # Lista
        assert ba == messages.query_encode(self.infoS, 3, [3])
    
    def test_query_msg_vazio(self):
        ba = bytearray()
        ba.extend((2).to_bytes(length=2, byteorder='big'))  # id
        ba.extend(socket.inet_aton(self.infoS[0]))          # IP
        ba.extend(self.infoS[1].to_bytes(length=2, byteorder='big'))    # Porta
        ba.extend((10).to_bytes(length=2, byteorder='big'))  # TTL
        ba.extend(listByteEncoder([]))                          # Lista
        assert ba == messages.query_encode(self.infoS, 10, [])
    
    def test_query_decode(self):
        tuple = messages.query_decode(messages.query_encode(self.infoS, 1, [3,1,2]))
        assert tuple == (self.infoS[0], self.infoS[1], 1, [3,1,2])
        
        tuple = messages.query_decode(messages.query_encode(self.infoS, 3, [3]))
        assert tuple == (self.infoS[0], self.infoS[1], 3, [3])
        
        tuple = messages.query_decode(messages.query_encode(self.infoS, 10, []))
        assert tuple == (self.infoS[0], self.infoS[1], 10, [])

class TestResponseEncode:
    def test_query_uma(self):
        ba = bytearray()
        ba.extend((5).to_bytes(length=2, byteorder='big'))  # id
        ba.extend((8).to_bytes(length=2, byteorder='big'))  # chunk_id
        ba.extend((1024).to_bytes(length=2, byteorder='big'))  # chunk_size in bytes
        
        with open("BigBuckBunny_8.m4s",'rb') as file:
            pl = file.read(1024)
        pl = bytearray(pl)
        ba.extend(pl)
        
        assert ba == messages.response_encode(8,1024,"BigBuckBunny","m4s")
        assert len(ba) == 2+2+2+1024
        assert len(ba) <= 2+2+2+1024
    
    def test_response_todas_chunks(self):
        for i in range(1,10):
            ba = bytearray()
            ba.extend((5).to_bytes(length=2, byteorder='big'))  # id
            ba.extend(i.to_bytes(length=2, byteorder='big'))  # chunk_id
            ba.extend((1024).to_bytes(length=2, byteorder='big'))  # chunk_size in bytes
            
            with open(f"BigBuckBunny_{i}.m4s",'rb') as file:
                pl = file.read(1024)
            pl = bytearray(pl)
            ba.extend(pl)
            
            assert ba == messages.response_encode(i,1024,"BigBuckBunny","m4s")
            assert len(ba) == 2+2+2+1024
            assert len(ba) <= 2+2+2+1024
            
        
    
    def test_response_decode(self):
        for i in range(1,10):
            tuple = messages.response_decode(messages.response_encode(i,1024,"BigBuckBunny","m4s"),outputFolder="output")
            assert tuple == (i, True)
            
            with open(f"BigBuckBunny_{i}.m4s",'rb') as file:
                pl0 = file.read(1024)
            pl0 = bytearray(pl0)
            
            with open(f"output/chunk{i}.m4s",'rb') as file:
                pl1 = file.read(1024)
            pl1 = bytearray(pl1)
            
            assert pl0 == pl1
            os.remove(f"output/chunk{i}.m4s")