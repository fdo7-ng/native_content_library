"""
Generates a custom library ready to be used as a VCSP endpoint for content library 2016 (vsphere 6.5).
This modifies original content library lib and item generated by make_vcsp_2018.py
"""

import argparse
import json
import os
import sys
import random
import string
import logging



def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

def searchItem(item, item_list):
    
    for itm in item_list:
        if itm == item:
            return True
    return False

def parse_options():
    """
    Parse command line options
    """
    parser = argparse.ArgumentParser(usage=usage())

    # Run options
    parser.add_argument('-n', '--name', dest='name',
                        help="library name")
    parser.add_argument('-path', '--path', dest='path',
                        help="library path on storage")
    parser.add_argument('-s','--short_name', dest='short_name',
                        default='true', help="tenant short name")
    parser.add_argument('-i','--imagefile', dest='imagefile',
                        default='true', help="image list file")
    args = parser.parse_args()

    if args.name is None or args.path is None:
        parser.print_help()
        sys.exit(1)

    return args

def usage():
    '''
    The usage message for the argument parser.
    '''
    return """Usage: python custom_vcsp.py -n <library-name> -p <library-storage-path> --imagefile <image list file> 
                                            --short_name <short base name>  
                                            --skip-cert <true or fale, default true>

"""

def main():

    logging.basicConfig(level=logging.DEBUG, format='%(name)s - %(levelname)s - %(message)s')
    logging.debug('Debug mode enabled')

    args = parse_options()

    lib_name = args.name
    lib_path = args.path
    short_name = args.short_name
    image_file = args.imagefile
    
    # short_name = "tenant1"
    root_dir = lib_path
    libfile = os.path.join(lib_path, "lib.json")
    random_key = randomString()
    new_lib_file = "lib_"+ short_name + "_" + random_key +".json"
    new_item_file = "items_" + random_key + ".json"


    # Extract Image List
    if os.path.exists(image_file):
        logging.info("Image file found - " + image_file)
        f = open(image_file, "r")
        data = f.readlines()
        image_list = []
        for line in data:
            image_list.append( line.strip().replace("\n","") )
        logging.debug(image_list)
    else:
        # print("Image file not found - ", image_file)
        # print("script aborted..")
        logging.warning("Image not found - " + image_file)
        logging.critical("script aborted..")
        sys.exit(1)

    # Open lib.json
    if os.path.exists(libfile):
        logging.info("lib.json found - " + libfile)

        with open(libfile) as json_file:
            data = json.load(json_file)
            lib_name = data['name']
            itemref = data['itemsHref']
            logging.debug ('Library name: '+ lib_name)
            logging.debug('itemref: '+ itemref)
            items_filename =  itemref

        data['itemsHref'] = new_item_file
        # Create New Lib File lib_[short_name]_[randomstring].json
        with open( os.path.join(root_dir, new_lib_file), 'w') as outfile:
            json.dump(data, outfile, indent=4)
    else:
        print("lib.json - Not Found")
        print("script aborted..")
        sys.exit(1)

    #Processing items.json file
    if os.path.exists( os.path.join(root_dir, items_filename) ):
        logging.debug("items file found: "+ items_filename )

        with open( os.path.join(root_dir, items_filename) ) as json_file:
            json_data = json.load(json_file)
            logging.debug( json.dumps(data, indent=4))
            items =  json_data['items']

        new_items_list = []
        for x in range(len(items)):
            logging.debug(  ' item - ' + items[x]['name'])
            found = searchItem(items[x]['name'], image_list)
            logging.debug(found)

            if( found ):
                new_items_list.append(items[x])
                #temp = items[x].name
                #logging.debug("Adding image to list: " +  temp)

        json_data['items'] = new_items_list

        with open( os.path.join(root_dir, new_item_file) , 'w') as outfile:
            json.dump(json_data, outfile, indent=4)

        logging.info(" - Script Finished")

if __name__ == "__main__":
    main()
