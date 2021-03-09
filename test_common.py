import pytest
import binascii

from common import listToBytes, bytesToList

"""
Possíveis testes de msgs:
- Teste comum
- Uma chunk única em um único peer
- Uma chunk única em cada peer
- Alguns peers vazios
- Só um peer possui tudo
- Todos os peers vazios
"""

class Test_listToBytes:
    def test_simples(self):
        ba = bytearray()
        i = 1
        ba.extend(i.to_bytes(length=2, byteorder='big'))
        i = 6
        ba.extend(i.to_bytes(length=2, byteorder='big'))
        i = 8
        ba.extend(i.to_bytes(length=2, byteorder='big'))
        i = 5
        ba.extend(i.to_bytes(length=2, byteorder='big'))
        assert ba == listToBytes([1,6,8,5])
        assert len(ba) == 8
        
    def test_um(self):
        ba = bytearray()
        i = 10
        ba.extend(i.to_bytes(length=2, byteorder='big'))
        assert ba == listToBytes([10])
        assert len(ba) == 2
    
    def test_vazio(self):
        ba = bytearray()
        assert ba == listToBytes([])
        assert len(ba) == 0

class Test_bytesToList:
    def test_simples(self):
        ba = bytearray()
        i = 1
        ba.extend(i.to_bytes(length=2, byteorder='big'))
        i = 6
        ba.extend(i.to_bytes(length=2, byteorder='big'))
        i = 8
        ba.extend(i.to_bytes(length=2, byteorder='big'))
        i = 5
        ba.extend(i.to_bytes(length=2, byteorder='big'))
        assert bytesToList(ba) == [1,6,8,5]
        
    def test_um(self):
        ba = bytearray()
        i = 10
        ba.extend(i.to_bytes(length=2, byteorder='big'))
        assert bytesToList(ba) == [10]
    
    def test_vazio(self):
        ba = bytearray()
        assert bytesToList(ba) == []