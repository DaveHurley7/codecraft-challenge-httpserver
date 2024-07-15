# Uncomment this to pass the first stage
import socket


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    #
    server_socket = socket.create_server(("localhost", 4221), reuse_port=True)
    c_sk, addr = server_socket.accept() # wait for client
    req = c_sk.recv(1024).decode()
    startln, *headers = req.split("\r\n")
    req_hdrs = {}
    for hdr in headers:
        if hdr == "\r\n":
            continue
        hdr_ln = hdr.split(":")
        hdr[hdr_ln[0].strip()] = hdr_ln[1].strip() 
    method, path, httpv = startln.split()
    if path == "/":
        msg = "HTTP/1.1 200 OK\r\n\r\n"
    elif path.startswith("/echo/"):
        text = path[6:]
        tlen = len(text)
        msg = "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: "+str(tlen)+"\r\n\r\n"+text
    elif path.startswith("/useragent"):
        text = req_hdrs["User-Agent"]
        tlen = len(text)
        msg = "HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nContent-Length: "+str(tlen)+"\r\n\r\n"+text
    else:
        msg = "HTTP/1.1 404 Not Found\r\n\r\n"
    c_sk.send(msg.encode())
    


if __name__ == "__main__":
    main()
