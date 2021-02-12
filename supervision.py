"""Supervision

Copyright (c) 2021 Nicolas MAURICE
All Rights Reserved.
Released under the MIT license

"""
import time
import mysql.connector
import psutil
from psutil._common import bytes2human
import datetime


host = "localhost"

def get_net_io_counters():
    """Get the net I/O counters
    """
    return psutil.net_io_counters(
            pernic=True,
            nowrap=True,
    )


def data_treatment_net_io(time):
    """
    Treats the net io data and writes it to textfile and mariadb
    """
    counters = get_net_io_counters()
    for nic_name in counters:
        bytes_sent = counters[nic_name].bytes_sent
        readable_sent = bytes2human(bytes_sent)
        bytes_received = counters[nic_name].bytes_recv
        readable_received = bytes2human(bytes_received)
        sqlstatement = f"INSERT INTO " \
                       f"net_io_counter" \
                       f"(" \
                       f"host," \
                       f"nic, " \
                       f"bytes_sent, " \
                       f"bytes_received, " \
                       f"readable_sent," \
                       f"readable_received" \
                       f") " \
                       f"VALUES (" \
                       f" '{host}'," \
                       f" '{nic_name}', " \
                       f" '{bytes_sent}', " \
                       f" '{bytes_received}', " \
                       f" '{readable_sent}', " \
                       f" '{readable_received}')"
        if len(nic_name) < 6:
            file_line = f"{time} NIC : {nic_name}\t \t reception : " \
                        f"{readable_received}\t sending : {readable_received}"
        else:
            file_line = f"{time} NIC : {nic_name}\t reception : " \
                        f"{readable_received}\t sending : {readable_received}"
        write_to_file(file_line)
        write_to_db(sqlstatement)


def get_disk_usage(path):
    """Get disk usage
    """
    return psutil.disk_usage(path)


def data_treatment_disk(time, parts):
    """
    Treats the disk usage and writes it to textfile and mariadb
    """
    for disk in parts:
        disk_name = disk[0]
        disk_path = disk[1]
        disk_usage = get_disk_usage(disk_path)
        total_space = disk_usage.total
        readable_total_space = bytes2human(total_space)
        used_space = disk_usage.used
        readable_used_space = bytes2human(used_space)
        percent_space = disk_usage.percent
        sqlstatement = f"INSERT INTO " \
                       f"disk_usage" \
                       f"(" \
                       f"disk_path," \
                       f"disk_name," \
                       f"disk_total, " \
                       f"disk_used, " \
                       f"readable_total, " \
                       f"readable_used, " \
                       f"percent_used " \
                       f") " \
                       f"VALUES (" \
                       f"'{disk_path}'," \
                       f"'{disk_name}'," \
                       f" '{total_space}', " \
                       f" '{used_space}', " \
                       f" '{readable_total_space}', " \
                       f" '{readable_used_space}', " \
                       f"'{percent_space}')"
        write_to_db(sqlstatement)
        file_line = f"{time} Disk mount :\t {disk_name}\t Space used : " \
                    f"{readable_used_space}({percent_space}%) of {readable_total_space}"
        write_to_file(file_line)


def get_cpu_usage():
    """Get the CPU % usage
    """
    return psutil.cpu_percent(interval=None)


def data_treatment_cpu(time):
    """
    Treats the cpu data and writes it to textfile and mariadb
    """
    cpu_usage = get_cpu_usage()
    sqlstatement = f"INSERT INTO " \
                   f"cpu_usage" \
                   f"(" \
                   f"cpu_percent " \
                   f") " \
                   f"VALUES (" \
                   f"'{cpu_usage}')"
    write_to_db(sqlstatement)
    file_line = f"{time} CPU percent :\t {cpu_usage} %"
    write_to_file(file_line)


def get_memory_usage():
    """Get stats about memory
    """
    return psutil.virtual_memory()


def calculate_memory_usage():
    """Calculates % of used memory
    """
    p_total = psutil.virtual_memory().total
    p_used = psutil.virtual_memory().used
    p_percent = (p_used / p_total) * 100
    p_percent = format(p_percent, '.1f')
    return p_percent


def data_treatment_memory(time):
    """
    Treats the memory usage data and writes it to textfile and mariadb
    """
    memory_usage = get_memory_usage()
    memory_total = memory_usage.total
    readable_total = bytes2human(memory_total)
    memory_used = memory_usage.used
    readable_used = bytes2human(memory_used)
    memory_percent = calculate_memory_usage()
    sqlstatement = f"INSERT INTO " \
                   f"memory_usage" \
                   f"(" \
                   f"total_memory, " \
                   f"used_memory, " \
                   f"memory_total_read, " \
                   f"memory_used_read, " \
                   f"percent_used " \
                   f") " \
                   f"VALUES (" \
                   f"'{memory_total}'," \
                   f" '{memory_used}', " \
                   f" '{readable_total}', " \
                   f" '{readable_used}', " \
                   f"'{memory_percent}')"
    write_to_db(sqlstatement)
    file_line = f"{time} Memory usage :\t {memory_percent} % of {readable_total}"
    write_to_file(file_line)


def write_to_db(sqlstatement):
    """Write to MariaDB
    """
    try:
        conn = mysql.connector.connect(
                user="root",
                password="admin",
                host="127.0.0.1",
                port=3306,
                database="supervision"
        )
    except mysql.connector.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        return
    cur = conn.cursor()
    cur.execute(sqlstatement)
    conn.commit()
    conn.close()
    print(sqlstatement)


def write_to_file(text):
    """
    Writes collected data to a textfile
    """
    with open("data_log.txt", "a") as file:
        file.write(text + "\n")


def main():
    """The main function"""
    #
    # We start by getting and defining the disk mounts, before iterating our functions periodically
    #
    disks_partitions = psutil.disk_partitions(all=False)
    print(disks_partitions)
    while True:
        try:
            time.sleep(10)
            now = datetime.datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            file_line = f"-------------------------------------------------------------------------------"
            write_to_file(file_line)
            data_treatment_disk(dt_string, disks_partitions)
            data_treatment_memory(dt_string)
            data_treatment_cpu(dt_string)
            data_treatment_net_io(dt_string)
        except KeyboardInterrupt:
            break


if __name__ == '__main__':
    main()
