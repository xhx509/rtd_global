#!/usr/bin/env python3

import time
import os
from pathlib import Path
from bluepy import btle
from mat.ble.bluepy.moana_logger_controller import LoggerControllerMoana


def just_delete_file_n_time_sync():
    print('reaching moana to time sync {}...'.format(mac))
    lc = LoggerControllerMoana(mac)
    if not lc.open():
        print('connection error')
        return

    lc.auth()
    if not lc.time_sync():
        print('error time sync')
    if not lc.file_clear():
        print('error file_clear')
    lc.close()


def full_demo(fol, mac):
    #print('reaching moana {}...'.format(mac))
    lc = LoggerControllerMoana(mac)
    if not lc.open():
        #print('connection error')
        return

    lc.auth()

    name_csv_moana = lc.file_info()
    
    g = open('/home/pi/rtd_global/status.txt', 'w')
    g.write('0')
    g.close()

    print('downloading file {}...'.format(name_csv_moana))
    data = lc.file_get()

    name_bin_local = lc.file_save(data)
    if name_bin_local:
        print('saved as {}'.format(name_bin_local))

        name_csv_local = lc.file_cnv(name_bin_local, fol, len(data))

        if name_csv_local:
            print('conversion OK')
            p = '{}/{}'.format(fol, name_csv_local)
            print('output files -> {}*'.format(p))
        else:
            print('conversion error')

    # we are doing OK
    lc.time_sync()

    # comment next 2 -> repetitive download tests
    # uncomment them -> re-run logger
    #time.sleep(1)
    #if not lc.file_clear():
    #    print('error file_clear')

    lc.close()
    

def main():
    waiting_interval = 120
    mac = 'D5:E8:6D:A0:FC:9D'
    print('reaching moana {}...'.format(mac))
    while 1:
        files_fol = str(Path.home()) + '/rtd_global/moana_demo'
        try:
            os.mkdir(files_fol)
        except OSError as error:
            pass

        full_demo(files_fol, mac)
        time.sleep(waiting_interval)
        # just_delete_file_n_time_sync()

if __name__ == '__main__':
    main()

# aixo crees un fitxer unit service que apunti en aquest codi
# i fas que el systemctl l'arranqui

