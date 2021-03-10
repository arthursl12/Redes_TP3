#!/usr/bin/env python3

import argparse
import socket

# cliente <IP:port> <5,6,7>

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("ipporta", help="IP:porta do ponto de contat (IPv4)")
    parser.add_argument("chunks", help="Lista de Chunks a serem baixadas")
    args = parser.parse_args()
    
    print(f"IP:porta = {args.ipporta}")
    # Trata o IP e a porta
    ipPortaLst = args.ipporta.split(":")
    assert len(ipPortaLst) == 2
    ip = socket.inet_ntoa(socket.inet_aton(ipPortaLst[0]))  
    porta = int(ipPortaLst[1])
    print(f"IP={ip}, porta={porta}")

    # Trata a lista de chunks
    chunksStr = ("".join(args.chunks)).split(",")
    chunks = []
    for i in chunksStr:
        chunks.append(int(i))
    print(chunks)
    
    
    udp_socket = connectUDP(args.ip, infoServer[0])

    
    udp_socket.close()

    

if __name__ == "__main__":
    main()
    