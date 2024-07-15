# Uncomment this to pass the first stage
import socket
import threading

def handle_client(c_sk):
    print("Handling client",c_sk)
    #c_sk.setblocking(0)
    req = c_sk.recv(512)
    req = req.decode()
    print("Have request")
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
    else:
        msg = "HTTP/1.1 404 Not Found\r\n\r\n"
    c_sk.send(msg.encode())
    c_sk.close()

def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    #
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    c_sk, addr = server_socket.accept() # wait for client
    c_sk.setblocking(0)
    t = threading.Thread(target=handle_client,args=[c_sk])
    t.start()

if __name__ == "__main__":
    main()
