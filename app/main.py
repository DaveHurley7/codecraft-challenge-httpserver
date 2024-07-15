# Uncomment this to pass the first stage
import socket
import threading
import sys

def handle_client(c_sk,addr):
    req = c_sk.recv(512).decode()
    startln, *headers = req.split("\r\n")
    req_hdrs = {}
    for hdr in headers:
        if hdr == "":
            continue
        hdr_ln = hdr.split(":",maxsplit=1)
        req_hdrs[hdr_ln[0].strip()] = hdr_ln[1].strip() 
    method, path, httpv = startln.split()
    if path == "/":
        msg = "HTTP/1.1 200 OK\r\n\r\n"
    elif path.startswith("/echo/"):
        text = path[6:]
        tlen = len(text)
        msg = "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: "+str(tlen)+"\r\n\r\n"+text
    elif path.startswith("/user-agent"):
        text = req_hdrs["User-Agent"]
        tlen = len(text)
        msg = "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: "+str(tlen)+"\r\n\r\n"+text
    elif path.startswith("/files/"):
        argv = sys.argv
        argc = len(argv)
        if argc != 3:
            msg = "HTTP/1.1 404 Not Found\r\n\r\n"
        else:
            if argv[1] != "--directory":
                msg = "HTTP/1.1 404 Not Found\r\n\r\n"
            else:
                host_dir = argv[2]
                req_file = path[7:]
                try:
                    print("Attempting to open")
                    fd = open(host_dir+req_file)
                    content = fd.read()
                    fd.close()
                    dlen = len(content)
                    msg = "HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Length: "+str(dlen)+"\r\n\r\n"+content
                except FileNotFoundError:
                    msg = "HTTP/1.1 404 Not Found\r\n\r\n"
                
    else:
        msg = "HTTP/1.1 404 Not Found\r\n\r\n"
    c_sk.send(msg.encode())
    c_sk.close()

def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    #
    sk = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    sk.bind(("localhost", 4221))
    sk.listen(10)
    while True:
        c_sk, addr = sk.accept() # wait for client
        threading.Thread(target=handle_client,args=[c_sk,addr]).start()

if __name__ == "__main__":
    main()
