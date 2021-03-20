#!/usr/bin/env python3

import argparse
import os

from common import createUDP, ipPortaSplit, logexit, msgId
from messages import (chunk_info_encode, get_decode, hello_decode,
                      query_decode, query_encode, response_encode)


def checkChunks(udp_socket, chunks, clnt_chnks, addr_client):
    """
    Dado os chunks requisitados pelo cliente 'clnt_chnks', acha aqueles que o 
    peer possui e retorna mensagem(ns) chunk_info para o cliente passado caso
    possua algum desses chunks
    """
    # Acha os chunks requisitados pelo cliente que o peer possui
    validos = []
    for key in chunks:
        if (key in clnt_chnks):
            validos.append(key)
            
    # Retorna chunk_info para o cliente
    chk_info = chunk_info_encode(validos)
    udp_socket.sendto(chk_info, addr_client)

def alagamento(udp_socket, vizinhos, addr_client, TTL, clnt_chnks, origin=None):
    """
    Faz o alagamento, isto é, envia uma mensagem Query para seus vizinhos
    (exceto para peer que nos enviou recebemos, se for o caso). 
    Não faz o alagamento se o TTL for 0
    """
    if (TTL == 0):
        print(f"[log] Não haverá alagamento, visto que TTL={TTL}")
        return
    print(f"[log] Alagamento em progresso, TTL={TTL}")
    for pair in vizinhos:
        if (origin is not None and pair == origin):
            print(f"[log] Não enviar Query para {pair}, que mandou a Query")
            continue
        msg = query_encode(addr_client, TTL, clnt_chnks)
        udp_socket.sendto(msg, pair)
        print(f"[log] Enviando Query para {pair}")
    print(f"[log] Fim do alagamento")

def handleHello(udp_socket, msg, addr, chunks, vizinhos):
    """
    Função Auxiliar para o Peer decodificar uma mensagem Hello do cliente.
    Envia para o mesmo cliente a mensagem Chunk_Info com as chunks disponíveis
    neste peer.
    Faz o alagamento para seus vizinhos.
    """
    clnt_chnks = hello_decode(msg)
    print(f"[log] Recebido hello de {addr[0]}:{addr[1]}, "+
            f"requisitando as chunks {clnt_chnks}")

    checkChunks(udp_socket, chunks, clnt_chnks, addr)
    alagamento(udp_socket, vizinhos, addr, 3, clnt_chnks)
    

def handleGet(udp_socket, addr_client, msg_get, filename, extension):
    """
    Função Auxiliar para o Peer montar uma mensagem Response após Get recebido
    do cliente. 
    Envia para o mesmo cliente a mensagem(ns) Response com as chunks que ele 
    pediu. (A chunk com certeza está neste peer, pois a decisão do cliente foi 
    baseada na chunk_info enviada por este peer). 
    """
    # Decodifica a mensagem Get recebida
    req_chnks = get_decode(msg_get)
    print(f"[log] Recebido get de {addr_client[0]}:{addr_client[1]}, "+
            f"requisitando as chunks {req_chnks}")
    
    # Envia Response para cada chunk requisitada
    for chunk_id in req_chnks:
        chunk_size = os.path.getsize(f"BigBuckBunny_{chunk_id}.m4s")
        reponse = response_encode(chunk_id, chunk_size, filename, extension)
        udp_socket.sendto(reponse, addr_client)
        print(f"[log] Response com a chunk {chunk_id} "+
                f"para {addr_client[0]}:{addr_client[1]} enviada")

def parseArguments():
    # Parsing dos argumentos
    parser = argparse.ArgumentParser()
    parser.add_argument("ip_porta", help="IP:porta deste peer")
    parser.add_argument("keyValues", help="Arquivo keyvalues a ser usado")
    parser.add_argument("neighbours", help="Lista de vizinhos deste peer", nargs='*')
    args = parser.parse_args()

    # Trata o IP e a porta recebida
    ip, porta = ipPortaSplit(args.ip_porta)
    print(f"[log] Conectaremos no IP {ip}, porto {porta}")

    # Forma a lista de peers vizinhos
    vizinhos = []   # Lista de tuplas (ip,porta) dos vizinhos
    for neigh in args.neighbours:
        ip1, porta1 = ipPortaSplit(neigh)
        vizinhos.append((ip1, porta1))
    print(f"[log] Vizinhos carregados: {vizinhos}")
    
    # Obtém as chunks que possui do arquivo passado
    chunks = {}     # Dict de tuplas (id,nome) dos vizinhos
    with open(args.keyValues) as f:
        for line in f:
            line = "".join(line.split())    # Remove espaços
            pairLst = line.split(":")       # Separa no ":"
            assert len(pairLst) == 2
            chunks[int(pairLst[0])] = pairLst[1]
    print(f"[log] Chunks carregados: {chunks}")
    return ip, porta, chunks, vizinhos

def fileInfoFromDict(d):
    """
    Dado um dicionário com keys inteiras e um nome de arquivo como valor, 
    retornao nome-base (antes do '_') e a extensão dos arquivos ali guardados. 
    Por exemplo: se guardado {3:'BigBuckBunny_3.m4s'}, retornará 'BigBuckBunny'
    e também 'm4s'
    """
    full = None
    for key in d:
        full = d[key]
        break
    
    # Pega o nome-base das chunks
    pairLst = full.split("_")       # Separa no "_"
    assert len(pairLst) == 2
    filename = pairLst[0]
    
    # Pega a extensão do arquivo das chunks
    pairLst = pairLst[1].split(".") # Separa no "_"
    assert len(pairLst) == 2
    fileextension = pairLst[1]
    return filename, fileextension

def main():
    # peer <IP:port> <key-values-files_peer[id]> <ip1:port1> ... <ipN:portN>
    ip, porta, chunks, vizinhos = parseArguments()
    udp_socket = createUDP(ip, porta)
    
    while(True):
        msg,addr = udp_socket.recvfrom(1024)
        msg = bytearray(msg)
        if (msgId(msg) == 1):
            handleHello(udp_socket, msg, addr, chunks, vizinhos)
        elif (msgId(msg) == 2):
            # Handle Query
            ipC, portoC, TTL, clnt_chnks = query_decode(msg)
            checkChunks(udp_socket, chunks, clnt_chnks, (ipC, portoC))
            alagamento(udp_socket, vizinhos, (ipC, portoC), 
                       TTL-1, clnt_chnks, origin=addr)
        elif (msgId(msg) == 4):
            filename, ext = fileInfoFromDict(chunks)
            handleGet(udp_socket, addr, msg, filename, ext)
        else:
            logexit("Mensagem com id inválido")

    # Fecha o soquete UDP
    udp_socket.close()

    

if __name__ == "__main__":
    main()
    
