import socket

# for purpose of testing socket communication and port availability

HOST = socket.gethostbyname(socket.gethostname()) # get address based on host name
PORT = 6000 # port to open

count = 1 # connection attempt

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s: # open socket
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept() # connect
    with conn:
        print("Connected by {}".format(addr)) # connected with addr
        while True: # repeat
            data = conn.recv(2048) # receive data of 2048 bytes
            if not data: # data doesn't exist
                break # quit connection
            conn.sendall(data) # send data

            # save recieved data as a file
            f = open(str(count)+".txt", "wb")
            f.write(data)
            f.close()

