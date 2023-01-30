import network_handler

network = network_handler.Network(False)




if __name__ == "__main__":
    while True:
        string_to_send = network.string_to_bytes(input("send message: "))
        network.send(string_to_send)