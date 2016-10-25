import argparse
import json
import os
import sys

from packages.helpers import clienthelper


# TODO
# make tiny client helper for the actual client
# not all helper functions needed in here


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--configfile", help="file where configuration will be loaded from, default: config.json",
                        type=str, default='config.json')
    # parser.add_argument("-v", "--verbose", help="increase output verbosity", type=int, default=0, choices=[0, 1, 2])
    args = parser.parse_args()

    config_filename = args.configfile
    if not config_filename.endswith('.json'):
        config_filename += '.json'

    filename = 'malwrAgent_' + config_filename.replace('.json', '') + '.py'
    clientname = config_filename.replace('.json', '')

    client_helper = clienthelper.ClientHelper(name='myGenClient', mode='client', debug_level=1)
    settings = json.dumps(client_helper.load_config_from_file(inFile=config_filename))

    with open('templates/client.py') as template:
        source = template.read()
        source = source.replace("{SETTINGS}", settings)
        source = source.replace("{CLIENTNAME}", clientname)

    # datetime.datetime.fromtimestamp(time.time()).strftime('%Y%m%d%H%M%S')
    # ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(6))
    if os.path.isfile(filename):
        print "File", filename, 'already exists'
        print "malwrAgent not saved to file"
    else:
        with open(filename, 'w') as outfile:
            outfile.write(source)


if __name__ == '__main__':
    try:
        main()
    except (KeyboardInterrupt, SystemExit):
        # print 'Interrupted'
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
        # except # catch all other errors
