import socket
import pickle


class Network:
    def __init__(self, player, HOST, user_type="CLIENT", PORT=5555):
        self.player = player
        self.type = user_type
        self.HOST = HOST
        self.PORT = PORT
        self.new_connection()

    def new_connection(self):
        if self.type == "SERVER":
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind((self.HOST, self.PORT))
            s.listen()
            while True:
                print("Ожидание подключения")
                self.client_s, addr = s.accept()
                print(f"Соединение установлено с {addr}")
                break
        elif self.type == "CLIENT":
            self.clent_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.clent_s.connect((self.HOST, self.PORT))
            print("Соединение установлено")
        else:
            raise Exception("Invalid user type")

    def update(self):
        self.client_s.sendall(pickle.dumps(self.player.pos))
        data = pickle.loads(self.client_s.recv(512))
        if data:
            self.player.set_coords_to_2(data)