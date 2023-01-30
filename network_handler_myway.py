
import threading
import socket
import time
import json


#Kode er rewritet, mange linjer er slettet og noen ting er byttet fra den
#originale delen.

# Er en Network klasse om representere en connection, Klassen har en init metoden
# som initialize flere parametere som blir brukt senere.
class Network:
    def __init__(self, is_server=False, bind_addr="127.0.0.1", port=6900, connect_addr="127.0.0.1"):
        self.is_server = is_server
        self.bind_addr = bind_addr
        self.connect_addr = connect_addr
        self.port = port
        self.conn = None
        self.running = True
        self.timeout = 0.4
        self._init_socket()
        self._start_threads()
# Initialize ein ny socket med en  reuseaddr (noe som er innebygd i socket.)
# Lagde egen funksjon for holde styr på hva som gjør hva.

    def _init_socket(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Samme opplegg som socket funksjonen, men her blir to threads startet.
# Det som skjer her er at en heartbeat packets sender informasjon i JSON string format
# over socket via regelmessige intervaller
# Tar en if check som sjekker om connection er established, hvis ikkje prøver
# den å finne connection
    def _start_threads(self):
        self.heartbeat_thread = threading.Thread(
            target=self._send_heartbeat, daemon=True)
        self.heartbeat_thread.start()
        if self.is_server:
            self._wait_for_connection()
        else:
            self._try_connect()

# Send_hearbeat funksjonen er der sjølve heartbeat packet blir sendt,
# man kan se at packets blir send med en intervall på 0.3 sekund.
    def _send_heartbeat(self):
        while self.running:
            heartbeat_packet = json.dumps({"type": "heartbeat"})
            self.send(heartbeat_packet)
            time.sleep(0.3)

# Try_connect funksjonen forsøker å established connection mellom addressen og
# porten som blei definert i starten i _init_ metoden.
# Sette en timeourt på 20sekund itilfelle connection ikkje blir funnet
# Så lenge en exception ikkje blir raised så blir connection establisha
# og packet'en går gjennom den connection
    def _try_connect(self):
        while True:
            try:
                self.socket.settimeout(20)
                self.socket.connect((self.connect_addr, self.port))
            except ConnectionRefusedError:
                print("Connection refused. Retrying in 500ms")
                time.sleep(0.5)
                continue
            except TimeoutError:
                print("Connection timed out. Retrying")
                continue
            else:
                self.conn = self.socket
                print("Connection established with client")
                break
        self.socket.settimeout(self.timeout)

# Til slutt har vi en wait for connection metoden som blir brukt når vi starte
# threads. Hvis connection blei establisha så får vi en melding med connection
# addressen.
    def _wait_for_connection(self):
        self.socket.bind((self.bind_addr, self.port))
        self.socket.listen()
        print("Server waiting for connection")
        temp_conn, addr = self.socket.accept()
        self.conn = temp_conn
        print(f"New connection from {addr}")
