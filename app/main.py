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
    method, path, httpv = startln.split()
    #if path == "/":
    text = path[6:]
    tlen = len(text)
    c_sk.send("HTTP/1.1 200 OK\r\nContent-Type: application/text-plain\r\nContent-Length: "+str(tlen)+"\r\n\r\n"+text.encode())
    #else:
     #   c_sk.send("HTTP/1.1 404 Not Found\r\n\r\n".encode())
    


if __name__ == "__main__":
    main()
