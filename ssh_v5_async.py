#!/usr/bin/env python3

import getpass
from cfw import dict_cfw
from switches import *
import argparse
import asyncio, asyncssh
import time



async def run_command(device, uname, pword, inp_fname, command_list, f_open_flag, devices):
    fname = inp_fname + "_" + str(device) + ".txt"

    try:
        client = await asyncio.wait_for(asyncssh.connect(host=devices[device][0], username=uname, password=pword, known_hosts=None), timeout=15)
    except:
        print('Error! Cannot connect to %s' % str(device))
    else:
        print("Connected to %s" % device)
        async with client:
            current_open_flag = f_open_flag

            for command in command_list:
                try:
                    result = await client.run(command, check=True)
                    print("Ran the command %s on %s" % (command, device))
                    with open(fname, current_open_flag) as f:
                        f.write('\n{}> {}\n'.format(device, command))
                        f.write(result.stdout)
                        f.close()
                    current_open_flag = 'a'
                except:
                    print('Error! Something is wrong with %s Cannot run the command or write it to the file %s' % (str(device),fname))

async def run_multiple_clients(devices, uname, pword, inp_fname, command_list, f_open_flag):
    tasks = (run_command(device, uname, pword, inp_fname, command_list, f_open_flag, devices) for device in devices)
    Futures = await asyncio.gather(*tasks, return_exceptions=True)


    for i, Future in enumerate(Futures, 1):
        if isinstance(Future, Exception):
            print('Task %d failed: %s' % (i, str(Future)))
            print(75*'-')


#######################################################################################

def read_args():
    parser = argparse.ArgumentParser(description='------ Great Description To Be Placed Here ------')
    parser.add_argument('-d', '--device_list', action='store', dest='list',
                        help='A file with the dictionary containing the devices')
    parser.add_argument('-c', '--commands', action='store', dest='my_Command_list',
                        help='List of comand to execute separated by comma')
    parser.add_argument('-f', '--file', action='store', dest='fn', help='This name will be part of the output file')
    parser.add_argument('-a', '--append', action='store_true',
                        help='If we need to append the file, not create a new one', default=False)
    parser.add_argument('-u', '--username', action='store', dest='username',
                        help='Username')
    parser.add_argument('-p', '--password', action='store', dest='password',
                        help='Users password')
    args = parser.parse_args()

    if not args.list or not args.fn or not args.my_Command_list:
        print('Not enough arguments. Try "python ssh-vX -h"')
        print(args.list, args.fn, args.my_Command_list)
        exit()

    if args.list.find('cfw') != -1:
        devices = dict_cfw
    elif args.list.find('efw') != -1:
        devices = dict_efw
    elif args.list.find('sw') != -1:
        devices = dict_switches
    elif args.list.find('elf') != -1:
        devices = dict_elf
    elif args.list.find('test') != -1:
        devices = {'My_vSRX_1': ('192.168.1.249',), 'My_vSRX_2': ('192.168.1.249',), 'My_vSRX_3': ('192.168.1.249',),
                   'My_vSRX_4': ('192.168.1.249',), 'My_vSRX_5': ('192.168.1.241',)}
    elif args.list.find('lab') != -1:
        devices = {'LB3_CFW': ('10.225.32.53',), 'LB3_EDGE_1A': ('10.225.32.52',), 'LB3_EDGE_1B': ('10.225.32.116',),
                   'LB3_EFW': ('10.225.32.117',)}
    else:
        print('No corresponding device list found')
        exit()


    if args.append == True:
        f_open_flag = 'a'
    else:
        f_open_flag = 'w'


    if not args.username:
        UN = input("Username: ")
    else:
        UN = args.username

    if not args.password:
        PW = getpass.getpass("Password for %s: " % UN)
    else:
        PW = args.password

    init_data = {'username': UN, 'password': PW, 'fname': args.fn, 'command_list': args.my_Command_list.split(',')}

    return init_data, devices, f_open_flag




def main():
    (init_data, devices, f_open_flag) = read_args()
    start_time = time.time()
    asyncio.get_event_loop().run_until_complete(run_multiple_clients(devices, init_data['username'], init_data['password'], init_data['fname'], init_data['command_list'],f_open_flag))
    print("--- %.2f seconds ---" % (time.time() - start_time))

if __name__ == '__main__':
    main()
