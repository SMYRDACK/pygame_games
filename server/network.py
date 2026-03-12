import socket, pygame


class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.1.57"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.data = self.connect()
        self.metadane = ["0 pozycja_x", "1 pozycja_y", "2 skin_code_x", "3 skin_code_y", "4 frame_direction"\
            ,"5 frame_index" ,"6 K_q", "7 healf", "8 gun_angle", "9 shoot"]

        self.position = pygame.math.Vector2(self.data[0], self.data[1]) #pozycja oczywiscie na mapie
        self.skin_code = pygame.math.Vector2(self.data[2], self.data[3])
        self.frame_data = (self.data[4], self.data[5])
        self.preesd_key = pygame.key.get_pressed()
        self.preesd_key[pygame.K_q] = self.data[6]
        self.healf = self.data[7]
        self.gun_angle = self.data[8]
        self.shoot = self.data[9]

    def connect(self):
        try:
            self.client.connect(self.addr)
            return eval(f"[{self.client.recv(2048).decode()}]")
        except:
            pass

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return self.client.recv(2048).decode()
        except socket.error as e:
            print(e)
