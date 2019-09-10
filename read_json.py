import json
import os
import sys
import random
import string

def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))

def searchItem(item, item_list):
    
    for itm in item_list:
        if itm == item:
            return True
    return False

short_name = "tenant1"
root_dir = "Templates"
jfile1 = "Templates/lib.json"
image_file = "tenant1.txt"
random_key = randomString()
new_lib_file = "lib_"+ short_name + "_" + random_key +".json"
new_item_file = "items_" + random_key + ".json"

if os.path.exists(image_file):
    print("found - ", image_file)
    f = open("tenant1.txt", "r")
    data = f.readlines()
    image_list = []
    for line in data:
        image_list.append( line.strip().replace("\n","") )
    print(image_list)
else:
    print("Image file not found - ", image_file)
    print("script aborted..")
    sys.exit(1)




with open(jfile1) as json_file:
    data = json.load(json_file)
    lib_name = data['name']
    itemref = data['itemsHref']
    print ('Library name: ', lib_name)
    print ('itemref: ', itemref)
    jfile2 = os.path.join(root_dir, itemref)
# Creating new Lile
#data['name'] =  
data['itemsHref'] = new_item_file

new_lib_file =   os.path.join(root_dir, new_lib_file)
with open(new_lib_file, 'w') as outfile:
    json.dump(data, outfile, indent=4)

# Processing items.json
print(jfile2)
with open(jfile2) as json_file:
    json_data = json.load(json_file)
    # print( json.dumps(data, indent=4))
    items =  json_data['items']

new_items_list = []
for x in range(len(items)):
    print(x, 'item - ', items[x]['name'])
    found = searchItem(items[x]['name'], image_list)
    print(found)

    if( found ):
        new_items_list.append(items[x])

#print(new_items_list)
# print( json.dumps(new_items_list, indent=4))

json_data['items'] = new_items_list

new_item_file = os.path.join(root_dir, new_item_file)
with open(new_item_file, 'w') as outfile:
    json.dump(json_data, outfile, indent=4)



