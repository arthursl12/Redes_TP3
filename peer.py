#!/usr/bin/env python3

import argparse
from messages import chunk_info_encode, hello_decode, hello_encode
import socket
from common import logexit, ipPortaSplit, msgId


def main():
    # peer <IP:port> <key-values-files_peer[id]> <ip1:port1> ... <ipN:portN>
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
     
    # Cria soquete UDP
    print(f"[log] Criando soquete UDP")
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Habilita para conexões
    try:  
        udp_socket.bind((ip,porta))
    except socket.error as e:
        logexit(str(e))
    infoSock = udp_socket.getsockname()
    print(f"[log] Soquete UDP criado em {infoSock[0]}:{infoSock[1]}")
    print(f"[log] Aguardando mensagens...")
    
    while(True):
        msg,addr = udp_socket.recvfrom(1024)
        msg = bytearray(msg)
        if (msgId(msg) == 1):
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
            
        pass

    # Fecha o soquete UDP
    udp_socket.close()

    

if __name__ == "__main__":
    main()
    