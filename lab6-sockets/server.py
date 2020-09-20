import socket
from threading import Thread
import os
import tqdm

SEP = '<SEP>'
BUF_S = 1024

clients = []

class ClientListener(Thread):
    # creating socket
    def __init__(self, name, sock):
        super().__init__(daemon=True)
        self.sock = sock
        self.name = name

    # close connection
    def _close(self):
        clients.remove(self.sock)
        self.sock.close()
        print(self.name + ' disconnected')

    def run(self):
        # receiving metadata
        metadata = self.sock.recv(BUF_S).decode().split(SEP)
        fname_initial = metadata[0]
        fsize = metadata[1]

        # resolving filenames
        fname = fname_initial
        if os.path.exists(fname):
            k = 1
            fname = fname_initial + '_copy' + str(k)
            while os.path.exists(fname):
                k += 1
                fname = fname_initial + '_copy' + str(k)

        # receiving file contents and writing to file
        file = open(fname, 'wb')
        data = self.sock.recv(BUF_S)
        while data:
            file.write(data)
            data = self.sock.recv(BUF_S)

        # closing connection
        self._close()
        print('file transmitted')
        return      


def main():
    next_name = 1

    # socket creation
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # reuse address
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('0.0.0.0', 8800))
    sock.listen()
    print('listening on port 8800')
    
    # client connection
    while True:
        con, addr = sock.accept()
        clients.append(con)
        name = 'u' + str(next_name)
        next_name += 1
        print(str(addr) + ' connected as ' + name)
        ClientListener(name, con).start()

if __name__ == '__main__':
    main()