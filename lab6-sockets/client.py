import socket
import tqdm
import os
import argparse

SEP = '<SEP>'
BUF_S = 1024

class Client():

    def __init__(self):
        # creating socket for sending
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def send_file(self, host, port, filename):
        # connecting to server
        self.sock.connect((host, port))
        print(f'connected to {host}:{port}')
        # opening file
        try:
            f = open(filename, 'rb')
            print('start sending')
            t = f.read()
            t_size = t.__sizeof__()
            count = 0
            # send metadata
            self.sock.send(f'{filename}{SEP}{t_size}'.encode())
            
            progress = tqdm.tqdm(range(t_size), f'sending {filename}', unit='B', unit_scale=True, unit_divisor=1024)

            # send file contents
            for i in progress:
                if count < t_size:
                    sent = self.sock.send(t[count:])
                    count += sent
                    progress.update(sent)
                else:
                    break
            
            f.close()
            print('finished sending')
            self.sock.shutdown(socket.SHUT_WR)

        except Exception:
            print('something is wrong with the file')
            print('closing connection')
            self.sock.shutdown(socket.SHUT_WR)



# parsing arguments from command line
parser = argparse.ArgumentParser(description='Transfer files')
parser.add_argument('filename', metavar='fn', type=str, nargs=1, help='filename to pass')
parser.add_argument('serverip', metavar='ip', type=str, nargs=1, help='server ip address')
parser.add_argument('serverport', metavar='port', type=int, nargs=1, help='server port number')
args = parser.parse_args()

# creating client
client = Client()
client.send_file(args.serverip[0], args.serverport[0], args.filename[0])