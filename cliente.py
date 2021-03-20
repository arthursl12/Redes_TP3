#!/usr/bin/env python3

import argparse
import socket
import time

from common import createUDP, ipPortaSplit, logexit, msgId
from messages import (chunk_info_decode, get_encode, hello_encode,
                      response_decode)

TIMEOUT_MAX = 5

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

def handleChunkInfo(udp_socket, msg, addr, chunks, alreadySentGet):
    """
    Função Auxiliar para o Cliente decodificar uma mensagem Chunk_Info.
    Se for o caso, envia para o mesmo peer mensagem(ns) get requisitando chunks
    que esse cliente precisa.
    """
    peer_chnks = chunk_info_decode(msg)
    print(f"[log] Recebido chunk_info de {addr[0]}:{addr[1]}, "+
            f"disponibilizando as chunks {peer_chnks}")

    # Se o peer possui alguma chunk de interesse (e ainda não 
    # requisitamos) envia uma requisição GET
    for id in peer_chnks:
        if (id in chunks and alreadySentGet[id] == False):
            msg = get_encode([id])
            udp_socket.sendto(msg, (addr[0],addr[1]))
            updt_dict = {id:True}
            alreadySentGet.update(updt_dict)
            print(f"[log] Enviando get de {id} para {addr[0]}:{addr[1]}")

def main():
    # cliente <IP:port> <5,6,7>
    ip, porta, chunks = parseArguments()
    udp_socket = createUDP("",0)
    udp_socket.settimeout(TIMEOUT_MAX)
    
    # Envia HELLO para peer de contato
    print(f"[log] Enviando hello")
    msg = hello_encode(chunks)
    udp_socket.sendto(msg, (ip,porta))

    # Limpa arquivo "output-IP.log"
    infoClient = udp_socket.getsockname()
    ipClient = infoClient[0]
    with open(f"output-{ipClient}.log","w") as f:
        pass
    
    
    # Aguarda chunk_infos, com timeout de 5s após a última mensagem recebida
    # Heurística pseudo-aleatória para Get: peer cujo chunk_info chega primeiro
    print(f"[log] Aguardando chunk_info's")
    alreadySentGet = {i:False for i in chunks}
    alreadyGot = {i:False for i in chunks} 
    while (True):
        # Controle das chunks necessárias já recebidas
        if all(alreadyGot[id] == True for id in alreadyGot):
            print("[log] Já recembemos todas as chunks, podemos sair do loop")
            break
        
        # Controle de Timeouts
        try:
            msg,addr = udp_socket.recvfrom(2048)
        except socket.timeout:
            print("[log] TIMEOUT: ou a chunk não está disponível ou não pode ser acessada (muito distante)")
            with open(f"output-{ipClient}.log","a") as f:
                for id in alreadySentGet:
                    if (alreadySentGet[id] == False):
                        f.write(f"0.0.0.0:0 - {id}\n")
            break
    
        # Handle das mensagens recebidas
        msg = bytearray(msg)
        if (msgId(msg) == 3):
            handleChunkInfo(udp_socket, msg, addr, chunks, alreadySentGet)
        elif (msgId(msg) == 5):
            # Handle Response
            id, success = response_decode(msg)
            print(f"[log] Recebido response de {addr[0]}:{addr[1]}, "+
                  f"com a chunk {id}")
            assert success
            print(f"[log] Chunk {id} já disponível em disco")
            updt_dict = {id:True}
            alreadyGot.update(updt_dict)
            with open(f"output-{ipClient}.log","a") as f:
                f.write(f"{addr[0]}:{addr[1]} - {id}\n")
        else:
            logexit("Mensagem com id inválido")
            
    # Fecha o soquete UDP
    udp_socket.close()

    

if __name__ == "__main__":
    main()
    
