# Make Content Library Script

###Requirement:
Intall boto3
pip install boto3 -y


$ python make_vcsp_2018.py -n fake_library -t local -p Templates/
$ python make_vcsp_2018.py -n fake_library -t local -p /Users/fernando.ng/Documents/BitBucket/content_library/Templates/


## Trouble Shooting
If you see error message:
```
Traceback (most recent call last):
  File "make_vcsp_2018.py", line 578, in <module>
    main()
  File "make_vcsp_2018.py", line 573, in main
    make_vcsp(lib_name, lib_path, md5_enabled)
  File "make_vcsp_2018.py", line 298, in make_vcsp
    item_json = _dir2item(p, item_path, md5_enabled, "urn:uuid:%s" % lib_id)
  File "make_vcsp_2018.py", line 163, in _dir2item
    return _make_item(name, vcsp_type, name, files_items, identifier = uuid.uuid4(), library_id=lib_id, is_vapp_template=is_vapp)
UnboundLocalError: local variable 'is_vapp' referenced before assignment
```
Most likely there is an issue with the template files. Experienced this when OVF file was missing.