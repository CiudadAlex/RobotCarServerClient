from threading import Thread
import socket
import struct
import traceback
import sys


class AbstractStreamClient(Thread):

    def __init__(self, host, port, debug=False):
        super().__init__()
        self.host = host
        self.port = port
        self.debug = debug
        self.active = True

    def stop(self):
        self.active = False

    def run(self):

        while self.active:

            # Protection against socket error
            try:
                self.connect_and_receive()
            except Exception:
                traceback.print_exc(file=sys.stdout)

    def connect_and_receive(self):
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        print(f"Connecting to = {self.host}:{self.port}")
        client_socket.connect((self.host, self.port))

        while self.active:

            metadata_size = struct.unpack('>I', client_socket.recv(4))[0]
            item_metadata = self.get_item_bytes(client_socket, metadata_size, metadata_size)
            self.debug_print(f"metadata_size = {metadata_size} = {len(item_metadata)}")

            item_size = struct.unpack('>I', client_socket.recv(4))[0]
            item_bytes = self.get_item_bytes(client_socket, item_size, 4096)
            self.debug_print(f"item_size = {item_size} = {len(item_bytes)}")

            self.use_item_metadata_and_bytes(item_metadata, item_bytes)

    def debug_print(self, text):
        if self.debug:
            print(text)

    @staticmethod
    def get_item_bytes(client_socket, item_size, initial_buff_size):

        buff_size = initial_buff_size
        reminder = item_size

        item_bytes = b""
        while reminder > 0:
            packet = client_socket.recv(buff_size)
            if not packet:
                break
            item_bytes += packet
            reminder = item_size - len(item_bytes)

            if buff_size > reminder:
                buff_size = reminder

        return item_bytes

    def use_item_metadata_and_bytes(self, item_metadata, item_bytes):
        raise NotImplementedError("The extending class should override the method 'use_item_metadata_and_bytes'")

