def main():
    args = argParse()
    udp_socket = connectUDP(args.ip, infoServer[0])

    
    udp_socket.close()

    

if __name__ == "__main__":
    main()
    