#!/usr/bin/env python3

import argparse
from messages import chunk_info_encode, hello_decode, hello_encode
import socket
from common import logexit, ipPortaSplit, msgId, createUDP

def handleHello(udp_socket, msg, addr, chunks):
    """
    Função Auxiliar para o Peer decodificar uma mensagem Hello do cliente.
    Envia para o mesmo cliente a mensagem Chunk_Info com as chunks disponíveis
    neste peer.
    """
    clnt_chnks = hello_decode(msg)
    print(f"[log] Recebido hello de {addr[0]}:{addr[1]}, "+
            f"requisitando as chunks {clnt_chnks}")
    
    # Acha os chunks requisitados pelo cliente que o peer possui
    validos = []
    for key in chunks:
        if (key in clnt_chnks):
            validos.append(key)
            
    # Retorna chunk_info para o cliente
    chk_info = chunk_info_encode(validos)
    udp_socket.sendto(chk_info, addr)

def parseArguments():
    # Parsing dos argumentos
    parser = argparse.ArgumentParser()
    parser.add_argument("ip_porta", help="IP:porta do ponto de contat (IPv4)")
    parser.add_argument("keyValues", help="Arquivo keyvalues a ser usado")
    parser.add_argument("neighbours", help="Lista de vizinhos do peer", nargs='+')
    args = parser.parse_args()

    # Trata o IP e a porta
    ip, porta = ipPortaSplit(args.ip_porta)
    print(f"[log] Conectaremos a {ip}, no porto {porta}")

    # Forma a lista de peers vizinhos
    vizinhos = []   # Lista de tuplas (ip,porta) dos vizinhos
    for neigh in args.neighbours:
        ip1, porta1 = ipPortaSplit(neigh)
        vizinhos.append((ip1, porta1))
    print(f"[log] Vizinhos carregados: {vizinhos}")
    
    # Obtém as chunks que possui do arquivo passado
    chunks = {}     # Dict de tuplas (id,nome) dos vizinhos
    with open(args.keyValues) as f:
        line = f.readline()
        line = "".join(line.split())    # Remove espaços
        pairLst = line.split(":")       # Separa no ":"
        assert len(pairLst) == 2
        chunks[int(pairLst[0])] = pairLst[1]
    print(f"[log] Chunks carregados: {chunks}")
    return ip, porta, chunks

def main():
    # peer <IP:port> <key-values-files_peer[id]> <ip1:port1> ... <ipN:portN>
    ip, porta, chunks = parseArguments()
    udp_socket = createUDP(ip, porta)
    
    while(True):
        msg,addr = udp_socket.recvfrom(1024)
        msg = bytearray(msg)
        if (msgId(msg) == 1):
            handleHello(udp_socket, msg, addr, chunks)
            
        pass

    # Fecha o soquete UDP
    udp_socket.close()

    

if __name__ == "__main__":
    main()
    