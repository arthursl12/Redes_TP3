#!/usr/bin/env python3

import argparse
import socket
from common import logexit, ipPortaSplit, msgId, createUDP
from messages import chunk_info_decode, hello_encode

def parseArguments():
    # Parsing dos argumentos
    parser = argparse.ArgumentParser()
    parser.add_argument("ipporta", help="IP:porta do ponto de contat (IPv4)")
    parser.add_argument("chunks", help="Lista de Chunks a serem baixadas")
    args = parser.parse_args()
    
    # Trata o IP e a porta
    ip, porta = ipPortaSplit(args.ipporta)
    print(f"[log] Conectaremos a {ip}:{porta}")

    # Trata a lista de chunks
    chunksStr = ("".join(args.chunks)).split(",")
    chunks = []
    for i in chunksStr:
        chunks.append(int(i))
    print(f"[log] Serão requeridas as chunks: {chunks}")
    return ip, porta, chunks

def main():
    # cliente <IP:port> <5,6,7>
    ip, porta, chunks = parseArguments()
    udp_socket = createUDP("",0)
    
    # Envia HELLO para peer de contato
    print(f"[log] Enviando hello")
    msg = hello_encode(chunks)
    udp_socket.sendto(msg, (ip,porta))
    
    # Aguarda chunk_infos, com timeout de 5s após a última mensagem recebida
    print(f"[log] Aguardando chunk_info's")
    hasTimedOut = False
    while (not hasTimedOut):
        msg,addr = udp_socket.recvfrom(1024)
        msg = bytearray(msg)
        if (msgId(msg) == 3):
            peer_chnks = chunk_info_decode(msg)
            print(f"[log] Recebido chunk_info de {addr[0]}:{addr[1]}, "+
                  f"disponibilizando as chunks {peer_chnks}")
    

    
    # Fecha o soquete UDP
    udp_socket.close()

    

if __name__ == "__main__":
    main()
    