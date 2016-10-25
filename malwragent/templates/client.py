# import json
# from tabulate import tabulate

from packages.helpers import clienthelper


# make tiny client helper for the actual client
# not all helper functions needed in here

def main():
    client_helper = clienthelper.ClientHelper(name='{CLIENTNAME}', mode='client', debug_level=1)

    # print(tabulate(,headers='keys',tablefmt='orgtbl'))

    # json.dumps replaces None by null
    null = None
    settings = {SETTINGS}

    for item in settings:
        chain = item['chain']
        # _module = item['module'].split('.')[-1]
        # class_name = item['class']
        module = item['module']
        settings = item['settings']

        if chain == 'REG':
            client_helper.reg_add_module(module, {'settings': settings})

        if chain == 'CLIENT':
            client_helper.recv_add_module(module, {'settings': settings})

    # start recv
    client_helper.set_interval(5.0)
    client_helper.start()


if __name__ == '__main__':
    main()
