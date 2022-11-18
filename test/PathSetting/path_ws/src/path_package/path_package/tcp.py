import socket

HOST = socket.gethostbyname(socket.gethostname())
PORT = 6000

count = 1

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print("Connected by {}".format(addr))
        while True:
            data = conn.recv(2048)
            if not data:
                break
            conn.sendall(data)

            f = open(str(count)+".txt", "wb")
            f.write(data)
            f.close()

