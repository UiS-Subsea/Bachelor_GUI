import network_handler

network = network_handler.Network(True)




if __name__ == "__main__":
    while True:
        print(network.receive())