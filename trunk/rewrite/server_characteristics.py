from database import *
from client_characteristics import ClientPlayer
import socket

class ServerPlayer(ClientPlayer):
    """Player class used by Server."""
    def __init__(self, n, addr):
        ClientPlayer.__init__(self, n)
        self.addr = addr

class Server:
    """pydnd server

    The server keeps track of players and stores its own database for
    authoritative purposes. Calls to Server.tick() handle all incoming messages
    and deal with current matters.

    Most of this server class was taken from the dc-rts project.
    """
    def __init__(self, hostname, port, x=32, y=24, genfile=0):
        """Creates a server at the given hostname and port.

        Passing a blank hostname will cause the server to bind to all
        interfaces.
        """
        self.players = list()
        self.msg = 0 # message buffer
        self.addr = 0 # address of player whose message is being parsed
        self._connect(hostname, port)
        self.genfile = genfile
        self.database = Database(x,y,genfile,0,0,self)

    def tick(self):
        """Handles all networking and simulation for one communications frame."""
        while True:
            # Exit loop and finish tick if there is no more data.
            if not self._next_msg():
                break
            # Handle message if player is recognized by server.
            # If player is not recognized, _check_player will add him to
            # self.players.
            if self._check_player():
                self._lookup_msg()

    def combat_tick(self):
        self.unit_db.combat_tick(self.weapon_db)
        self.weapon_db.tick()

    def _check_player(self):
        """Reads the message in self.msg to determine whether or not the player
        is in the server's players list, self.players. If the player does not
        exist, the server sends him an ID and adds him to the list.
        
        Returns True if player exists, otherwise False.
        """
        if self.msg[0] == -1:
            if self.players:
                new_id = self.players[-1].id + 1
            else:
                new_id = 0
            self._new_player(new_id)
            return False
        else:
            try:
                self.players[self.msg[0]]
                return True
            except IndexError:
                print "Warning: Player ID", self.msg[0], "in message", \
                    self.msg, "not recognized."
                return False

    def _connect(self, hostname, port):
        """Binds the given UDP port on the interface specified by hostname.

        A blank hostname will create a socket that listens on all interfaces.
        """
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((hostname, port))
        self.sock.setblocking(0)

    def _lookup_msg(self):
        """Calls the function mapped to the key contained in the buffered
        message"""
        msg_lu = {"add": self._queue_msg, "attack": self._queue_msg, "move": self._queue_msg}
        try:
            msg_lu[self.msg[1]](self.msg)
        except KeyError:
            print "Warning: Key", self.msg[1], "in message", \
                    self.msg, "not recognized."

    def _new_player(self, id):
        """Creates a player and notifies clients."""
        # The order here is important! If the new player is added to
        # self.players before notifying all clients, then the new player will
        # get the message twice.
        self._send_all([id, "add_player"])
        self.players.append(ServerPlayer(id, self.addr))
        # tell the new player who the other players are
        for p in self.players:
            self._send_to([p.id, "add_player"], id)
        # tell the new player which one is him
        self._send_to([id, "is_you"], id)
        self._send_to([id, "sync", self.database.area.x,
                    self.database.area.y,self.genfile], id)
        print "New Server Player", id

    def _next_msg(self):
        """Attempts to read next message from socket into self.msg.

        Returns True on success, False on failure.
        """
        try:
            data, self.addr = self.sock.recvfrom(4096)
            self.msg = eval(data, {"__builtins__":None}, {}) # eval data safely
            return True
        except socket.error, e: # no more data
            return False

    def _queue_msg(self, m):
        """Passes off messages to clients and server's own UnitDB instance."""
        self._send_all(m)

    def _send_all(self, m):
        """Sends the given message to all players."""
        for p in self.players:
            self.sock.sendto(repr(m), p.addr)

    def _send_to(self, m, id):
        """Sends the given message to the specified player."""
        self.sock.sendto(repr(m), self.players[id].addr)
    

