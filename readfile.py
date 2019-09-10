import os.path

root_dir ="/Users/fernando.ng/Documents/BitBucket/content_library/Templates"

f = open("tenant1.txt", "r")
var = f.readlines()

print(var)
fullpath = "/fakedirectory/"
image_list = []
for itm in var:
    data = itm.strip().replace("\n","")
    file = os.path.join(root_dir, data)
    image_list.append(data)
    if os.path.exists(file):
        print("found - ", file)
    else:
        print("not found - ", file)

print(image_list)
# fruits = ["apple", "banana", "cherry"]
# for x in fruits:
#   print(x)