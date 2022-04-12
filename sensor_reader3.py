import os
import time
from pathlib import Path
from bluepy import btle
from mat.ble.bluepy.moana_logger_controller import LoggerControllerMoana

# mac = 'cc:67:b3:bf:d3:66'
macs = ['D5:E8:6D:A0:FC:9D']


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
    lc = LoggerControllerMoana(mac)
    if not lc.open():
        # print('connection error')
        return

    lc.auth()

    name_csv_moana = lc.file_info()

    print('Status file changed to 0')

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
    time.sleep(1)
    if not lc.file_clear():
        print('error file_clear')

    time.sleep(20)
    g = open('/home/pi/rtd_global/status.txt', 'w')
    g.write('1')
    g.close()
    print('Status file changed to 1')
    lc.close()


# scanner = btle.Scanner().withDelegate(LCBLEMoanaDelegate())
# devices = scanner.scan(10
# the name that the scan searches for
scanName = "ZT-MOANA"
print('reaching moana {}...'.format(mac))

while True:
    files_fol = str(Path.home()) + '/rtd_global/moana_demo'
    try:
        os.mkdir(files_fol)
    except OSError as error:
        pass

    for mac in macs:
        full_demo(files_fol, mac)
        time.sleep(5)


