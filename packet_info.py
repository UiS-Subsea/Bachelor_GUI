from datetime import datetime
import logging
import os

#Lagger en classe som skal "logge" informasjonen til packets på en seperat fil
#Kan bruke logger klassen til å finne ut om forskjellige errors, warnings og critical messages.
class Logger:
    def __init__(self):
        self.packet_folder = "packet_logger/"
        if not os.path.exists(self.packet_folder):
            os.mkdir(self.packet_folder)

        packet_date = datetime.datetime.now().strftime("%Y-%m-%d %H.%M.%S")


        #Bruker INFO level som er høyere enn DEBUG for å få mer detaljert informasjon,
        #men under warning, error og critical levelene som indikerer alvorlighetsgraden.
        log_format = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')

        #logging.Formatter is a class that is used to specify the format of log messages.
        #logging.basicConfig is a convenience function that sets up a basic configuration
        #for the logging system.
        data_handler = logging.FileHandler(f"{self.packet_folder}{packet_date} data.log")

        data_handler.setFormatter(packet_date)
        #can potentially use error_filehandler.setFormatter(packet_date) to test errors/warnings
        
        