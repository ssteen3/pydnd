from database import *
from ui_characteristics import *
import socket

class ClientPlayer:
    """Player class used by Client."""
    def __init__(self, n):
        self.id = n

class Client:
    """pydnd client

    The client manages a player's game state. It sends messages to and handles
    messages from the server, interacting with its stored database
    appropriately. 

    Much of this class was again taken from the dc-rts project.
    """
    def __init__(self, hostname, port, game):
        """Creates a client that attempts to connect to a server at the given
        hostname and port."""
        self.players = list()
        self.msg = 0 # message buffer
        self._connect(hostname, port)
        self.connected = False
        self.id = 0 # client's corresponding player id
        self.game = game
        self.database = self.game.database

    def tick(self):
        """Handles all networking and simulation for one communications frame."""
        while True:
            if not self._next_msg():
                break
            self._lookup_msg()

    def _add_player(self, m):
        """Adds a new ClientPlayer to self.players"""
        self.players.append(ClientPlayer(m[1]))
        print "New Client Player", m[1]

    def _connect(self, host, port):
        """Requests a connection from the specified server.
        
        Sending an empty message with user_id -1 prompts the server to respond
        with a new player for the connecting client.
        """
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setblocking(0)
        self.sock.connect((host, port))
        self._send([-1])

    def _lookup_msg(self):
        """Calls the function mapped to the key contained in the buffered
        message.
        
        Disconnected clients will only parse messages regarding the player list,
        and the sync message (used to sync the client's communications message
        counter with the server)
        """
        if self.connected:
            msg_lu = {"database": self._queue_msg, "graphical": self._queue_scr, "add_player": self._add_player}
        else:
            msg_lu = {"add_player": self._add_player, "is_you": self._set_id,
                "sync": self._sync}
        try:
            msg_lu[self.msg[2]](self.msg)
        except KeyError:
            print "Warning: Key", self.msg[1], "in message", \
                self.msg, "not recognized."

    def _next_msg(self):
        """Attempts to read next message from socket into self.msg.

        Returns True on success, False on failure.
        """
        try:
            data = self.sock.recv(4096)
            self.msg = eval(data, {"__builtins__":None}, {}) # eval data safely
            return True
        except socket.error, e: # no more data
            return False

    def _queue_msg(self, m):
        """Sends messages from the server to the DB queue"""
        self.database.queue(m)

    def _queue_msg(self, m):
        """Sends messages from the server to the SCR queue"""
        self.game.queue(m)

    def _send(self, m):
        """Sends message to server"""
        self.sock.send(repr(m))

    def _set_id(self, m):
        """Sets client's player id."""
        self.id = m[1]
        print "Client is player", m[1]

    def _sync(self, m):
        """Synchronizes client communications frame counter with server, and
        mark client as connected."""
        self.connected = True
        self.database = CLDatabase(m[3],m[4],m[5])
