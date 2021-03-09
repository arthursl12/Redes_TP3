def listToBytes(l):
    """
    Dada uma lista (ou outro iterável) de inteiros, 
    retorna um bytearray com os 2 bytes para cada item, na mesma ordem
    """
    ba = bytearray()
    for item in l:
        assert type(item) == int
        ba.extend(item.to_bytes(length=2, byteorder='big'))
    return ba
        

def bytesToList(ba):
    """
    Dado um bytearray, retorna uma lista com os inteiros de 2 em 2 bytes,
    na mesma ordem que estão no bytearray
    """
    lst = []
    size = len(ba)
    assert size % 2 == 0
    for i in range(size//2):
        numb = ba[i*2:i*2+2]
        num = int.from_bytes(numb, "big")
        lst.append(num)
    return lst
        


