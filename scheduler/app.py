import time
import schedule
import configparser

import localUtils
from roundRobin_classic import roundRobin2 as roundRobin

config = configparser.ConfigParser()
config.read('conf.cfg')
scheduleTime = int(config['schedule-settings']['TIME_LAPSE_MINUTES'])

def job():
    
        rutinasTot=localUtils.selectRecordTable('RutinasDisponibles')
        for rutina in rutinasTot:
            if rutina["esActivado"]==1 and rutina["idAlgoritmo"]==1:
                roundRobin(rutina["id"])

def main():
    # inicia la primera iteración
    job()

    # luego inicia el loop de revisiones según tiempo fijado "TIME_LAPSE_MINUTES"
    schedule.every(scheduleTime).minutes.do(job)
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()