#!/usr/bin/env python3

import argparse
import socket
from common import logexit

def main():
    # cliente <IP:port> <5,6,7>
    parser = argparse.ArgumentParser()
    parser.add_argument("ipporta", help="IP:porta do ponto de contat (IPv4)")
    parser.add_argument("chunks", help="Lista de Chunks a serem baixadas")
    args = parser.parse_args()
    
    # Trata o IP e a porta
    ipPortaLst = args.ipporta.split(":")
    assert len(ipPortaLst) == 2
    ip = socket.inet_ntoa(socket.inet_aton(ipPortaLst[0]))  
    porta = int(ipPortaLst[1])
    print(f"[log] Conectaremos a {ip}:{porta}")

    # Trata a lista de chunks
    chunksStr = ("".join(args.chunks)).split(",")
    chunks = []
    for i in chunksStr:
        chunks.append(int(i))
    print(f"[log] Serão requeridas as chunks: {chunks}")
    
    # Cria soquete UDP
    print(f"[log] Criando soquete UDP")
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # Habilita para conexões
    try:  
        udp_socket.bind(("",0))
    except socket.error as e:
        logexit(str(e))
    infoSock = udp_socket.getsockname()
    print(f"[log] Soquete UDP criado em {infoSock[0]}:{infoSock[1]}")


    
    # Fecha o soquete UDP
    udp_socket.close()

    

if __name__ == "__main__":
    main()
    