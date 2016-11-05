#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import

import argparse
import sys
import time

from tabulate import tabulate
from termcolor import colored

from malwragent.packages.helpers.client import Client

# There is at least a client chain to build
__CHAINS_TO_BUILD = ['CLIENT']

# Location where chains are stored
__CHAIN_STORE = './myChains/'


def print_welcome():
    print "#   __   __  _______  ___      _     _  ______    _______  _______  _______  __    _  _______ "
    print "#  |  |_|  ||   _   ||   |    | | _ | ||    _ |  |   _   ||       ||       ||  |  | ||       |"
    print "#  |       ||  |_|  ||   |    | || || ||   | ||  |  |_|  ||    ___||    ___||   |_| ||_     _|"
    print "#  |       ||       ||   |    |       ||   |_||_ |       ||   | __ |   |___ |       |  |   |  "
    print "#  |       ||       ||   |___ |       ||    __  ||       ||   ||  ||    ___||  _    |  |   |  "
    print "#  | ||_|| ||   _   ||       ||   _   ||   |  | ||   _   ||   |_| ||   |___ | | |   |  |   |  "
    print "#  |_|   |_||__| |__||_______||__| |__||___|  |_||__| |__||_______||_______||_|  |__|  |___|  "
    print "#"
    print "#   -- .- .-.. .-- .-. .- --. . -. - "
    print "#"
    print "#  Hello Agent M! Welcome to the MalwrAgency. Use our MalwrAgent to create your "
    print "#  highly flexible and easy to use Malwr. Please go ahead ..."
    print "#"


# TODO do raw_input here
def get_user_input():
    pass


def do_wizard_egress(egress_filename, config_filename, client):

    chain_id = __CHAINS_TO_BUILD[0]
    client.init_chain(chain_id)

    selected_module_name = 'Web'

    with open(egress_filename, 'r') as ulist:
        for url in ulist:
            if url.strip():
                module_args = {
                    'settings': {
                        'function': 'f_http_get',
                        'args': {
                            'url': url.strip()
                        },
                        'ignore_output': True
                    }
                }
                client.add_item(chain_id, selected_module_name, module_args)

    client.save_chain_to_file(config_filename)
    return


def do_wizard(modules, config_filename, client):
    # TODO
    # ask for interval
    # ask for random interval
    # TODO ask for custom chains to build additionally to the standard client chain
    # TODO[30/10/2016][bl4ckw0rm] Make either Y/n to default value
    selection = str(
        raw_input('#  Do you want your client to register with C2-Server? (Y|N) \\> ').strip())
    if selection.upper() == 'Y' or selection.upper() == 'YES':
        # prepend to array
        __CHAINS_TO_BUILD.insert(0, 'REG')

    for chain in __CHAINS_TO_BUILD:
        client.init_chain(chain)

        if chain == 'REG':
            print "#  Choose from our list of modules. How should your client register with the server?"
        if chain == 'CLIENT':
            print "#  Choose from our list of modules. What do you want the client to do?"
        print "#"

        while True:
            # TODO
            # Classify module compatibility
            # do only show compatible modules

            selection = str(
                raw_input('#  ([0-9]{n}|[N for NEXT]|[C for CHAIN]|[M for MODULES]) ' + chain + ' \\> ').strip())

            if selection.upper() == 'N':
                if not client.get_chain_length_by_id(chain):
                    print
                    print colored("Chain must not be emtpy. Add some modules to your chain!", 'red')
                    print
                else:
                    print "#"
                    break
            elif selection.upper() == 'C':
                print
                print client.get_chain_by_id(chain, out_format='table')
                print
            elif selection.upper() == 'M':
                print
                print tabulate(modules, headers='keys', tablefmt='')
                print
            elif selection.isdigit() and isinstance(int(selection), int):
                if int(selection) >= len(modules):
                    print
                    print colored("There is no module " + selection, 'red')
                    print
                    continue

                selected_module = modules[int(selection)]
                selected_module_name = selected_module['module']
                selected_module_function = selected_module['function']

                # TODO define standard structure somewhere more 'global'
                module_args = {
                    'settings': {
                        'function': selected_module_function,
                        'args': None
                    }
                }

                done_add = False
                while not done_add:
                    result = client.add_item(chain, selected_module_name, module_args, mode='interactive')

                    if result:
                        if result['result']:
                            done_add = True
                            print
                            print colored(
                                "Adding function " + selected_module_function + ' from module ' +
                                selected_module_name + " done",
                                'green')
                            print
                        elif not result['result']:
                            # TODO[29/10/2016][bl4ckw0rm] move missing arg check to client.py
                            if result['code'] in [400, 401, 402, 403, 404]:
                                print
                                print colored(result['reason'], 'red')
                                print
                                for missing_arg in result['missing_args']:
                                    # TODO make def for user input
                                    missing_arg_value = str(raw_input('# +[' + missing_arg + '] \\> ').strip())

                                    settings = module_args['settings']
                                    args = settings['args']
                                    if not args:
                                        args = dict()
                                    args[missing_arg] = missing_arg_value
                                    settings['args'] = args
                            elif result['code'] in [405]:
                                print
                                print colored(result['reason'], 'red')
                                print
                                break
                            elif result['code'] in [500]:
                                print
                                print colored(result['reason'], 'red')
                                print
                                break
                    else:
                        break
            else:
                print
                print "# Nowhere to run !?"
                print

    selection = str(
        raw_input('#  Do you want to review your chain? (Y|N) \\> ').strip())
    if selection.upper() == 'Y' or selection.upper() == 'YES':
        print
        print client.get_formatted_chain(out_format='table')
        print

    selection = str(
        raw_input('#  Do you want to save the chain as ' + config_filename + '? (Y|N) \\> ').strip())
    if selection.upper() == 'Y' or selection.upper() == 'YES':
        client.save_chain_to_file(config_filename)

    print
    print "See you then. Use 'malwragent.py -l -c " + config_filename + "' to run your client."
    print

    return 0


def main():
    """
       by default, _CHAIN_STORE + config.json is loaded and run

    """
    parser = argparse.ArgumentParser()
    parser.add_argument("-l", "--load",
                        help="load and run chain from a configuration file.",
                        action="store_true")
    parser.add_argument("-w", "--wizard",
                        help="create and save a chain to configuration file",
                        action="store_true")
    parser.add_argument("-c", "--configfile",
                        help="configuration file name, default: config.json",
                        type=str,
                        default=__CHAIN_STORE + 'config.json')
    parser.add_argument("-i", "--interval",
                        help="interval for periodic chain execution, default: 10 seconds",
                        type=int,
                        default=10)
    parser.add_argument("-e", "--egress",
                        help="load file with URLs and build configuration for egress testing",
                        type=str)
    parser.add_argument("--log",
                        help="increase logging output verbosity",
                        type=int,
                        default=0,
                        choices=[1, 2, 3, 4])
    parser.add_argument('-V', '--version',
                        action='version',
                        version='%(prog)s (version 0.4)')

    args = parser.parse_args()

    # TODO[01/11/2016][bl4ckw0rm] validate all parsed arguments

    config_filename = args.configfile
    if not config_filename.endswith('.json'):
        config_filename += '.json'
    client_name = config_filename.replace('.json', '')

    if args.log > 3:
        print "Config filename", config_filename

    # TODO[04/11/2016][bl4ckw0rm] init config_filename at init
    # TODO create multiple client objects for multiple concurrent running clients
    client = Client(logging_level=args.log)
    client.set_client_name(client_name)

    if args.load:
        # TODO allow multiple config files

        try:
            client.load_chain_from_file(filename=config_filename)
            if client.get_chain_length_by_id('CLIENT') < 1:
                print
                print colored('Chain Emtpy ... ?', 'red')
                print
                return 1
        except IOError as err:
            if args.log > 3:
                print
                print colored(err, 'red')
                print
            if err.errno == 2:
                print
                print colored('Create a chain first!', 'red')
                print
            return 1

        # This is the single sign of execution, when --log LEVEL is not provided
        print "Autopilot takes over in"
        count = 3
        while count > 0:
            print "  ", count
            count -= 1
            time.sleep(1)

        client.set_client_interval(args.interval)
        client.run_agent()
    elif args.egress:
        # TODO[04/11/2016][bl4ckw0rm] validate url list / format
        return do_wizard_egress(args.egress, config_filename, client)
    elif args.wizard:
        print_welcome()
        all_modules_list = client.get_module_list(out_format='select')
        return do_wizard(all_modules_list, config_filename, client)
    else:
        parser.print_help()

    return 0

if __name__ == '__main__':
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print
        print colored('Bye, Bye', 'green')
        sys.exit(0)
