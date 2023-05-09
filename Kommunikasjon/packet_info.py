from datetime import datetime
import datetime
import logging
import os

# Lagger en classe som skal "logge" informasjonen til packets på en seperat fil
# Kan bruke logger klassen til å finne ut om forskjellige errors, warnings og critical messages.


class Logger:
    def __init__(self):
        self.packet_folder = "packet_logger/"
        if not os.path.exists(self.packet_folder):
            os.mkdir(self.packet_folder)

        packet_date = datetime.datetime.now().strftime("%Y-%m-%d %H.%M.%S")

        # Bruker INFO level som er høyere enn DEBUG for å få mer detaljert informasjon,
        # men under warning, error og critical levelene som indikerer alvorlighetsgraden.
        log_format = logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s')

        # logging.Formatter is a class that is used to specify the format of log messages.
        # logging.basicConfig is a convenience function that sets up a basic configuration
        # for the logging system.
        data_handler = logging.FileHandler(
            f"{self.packet_folder}{packet_date} data.log")
        data_handler.setFormatter(log_format)

        # can potentially use error_filehandler.setFormatter(packet_date) to test errors/warnings
        self.data_logger = logging.getLogger(
            "data_logger")  # Logger sensor informasjonen

        self.data_logger.addHandler(data_handler)
        self.data_logger.setLevel(logging.INFO)

        #id_135_handler = logging.FileHandler(
        #    f"{self.packet_folder}{packet_date} id_135.log")
        #id_136_handler = logging.FileHandler(
        #    f"{self.packet_folder}{packet_date} id_136.log")
        #id_137_handler = logging.FileHandler(
        #    f"{self.packet_folder}{packet_date} id_137.log")
        
        id_139_handler = logging.FileHandler(
            f"{self.packet_folder}{packet_date} id_139.log")
        id_138_handler = logging.FileHandler(
            f"{self.packet_folder}{packet_date} id_138.log")
        id_34_handler = logging.FileHandler(
            f"{self.packet_folder}{packet_date} id_34.log")
        id_33_handler = logging.FileHandler(
            f"{self.packet_folder}{packet_date} id_33.log")
        

        id_42_handler = logging.FileHandler(
            f"{self.packet_folder}{packet_date} id_42.log")
        id_32_handler = logging.FileHandler(
            f"{self.packet_folder}{packet_date} id_32.log")


        #id_135_handler.setFormatter(log_format)
        #id_136_handler.setFormatter(log_format)
        #id_137_handler.setFormatter(log_format)
        id_138_handler.setFormatter(log_format)
        id_139_handler.setFormatter(log_format)
        id_34_handler.setFormatter(log_format)
        id_33_handler.setFormatter(log_format)
        id_32_handler.setFormatter(log_format)
        id_42_handler.setFormatter(log_format)



        #self.id_135_logger = logging.getLogger("id_135_logger")
        #self.id_136_logger = logging.getLogger("id_136_logger")
        #self.id_137_logger = logging.getLogger("id_137_logger")
        self.id_138_logger = logging.getLogger("id_138_logger")
        self.id_139_logger = logging.getLogger("id_139_logger")
        self.id_34_logger = logging.getLogger("id_34_logger")
        self.id_33_logger = logging.getLogger("id_33_logger")
        self.id_32_logger = logging.getLogger("id_32_logger")
        self.id_42_logger = logging.getLogger("id_42_logger")





        #self.id_135_logger.addHandler(id_135_handler)
        #self.id_136_logger.addHandler(id_136_handler)
        #self.id_137_logger.addHandler(id_137_handler)
        self.id_138_logger.addHandler(id_138_handler)
        self.id_139_logger.addHandler(id_139_handler)
        self.id_34_logger.addHandler(id_34_handler)
        self.id_33_logger.addHandler(id_33_handler)
        self.id_32_logger.addHandler(id_32_handler)
        self.id_42_logger.addHandler(id_42_handler)



#        self.id_135_logger.setLevel(logging.INFO)
#        self.id_136_logger.setLevel(logging.INFO)
#        self.id_137_logger.setLevel(logging.INFO)

        self.id_138_logger.setLevel(logging.INFO)
        self.id_139_logger.setLevel(logging.INFO)
        self.id_34_logger.setLevel(logging.INFO)
        self.id_33_logger.setLevel(logging.INFO)
        self.id_32_logger.setLevel(logging.INFO)
        self.id_42_logger.setLevel(logging.INFO)




if __name__ == "__main__":

    logger = Logger()
    # Can potentially add debug, info and critical messages here.
    #logger.debug("Debug message")
    #logger.info("info message")
    #logger.critical("critical message")
    #logger.id_135_logger.info("Data for packet with ID 135")
    #logger.id_136_logger.info("Data for packet with ID 136")
    #logger.id_137_logger.info("Data for packet with ID 137")
    logger.id_138_logger.info("Data for packet with ID 138")
    logger.id_139_logger.info("Data for packet with ID 139")
    logger.id_34_logger.info("Data for packet with ID 34")
    logger.id_33_logger.info("Data for packet with ID 33")
    logger.id_32_logger.info("Data for packet with ID 32")
    logger.id_42_logger.info("Data for packet with ID 42")



