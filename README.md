# wrs_prefab_parser
"""WRS 2018 (prefab_parser).
This module is designed for Human Navigation in virtual space.This module is
composed of functions allowing to parse a unity scene (prefab file)
and retrieve the graspable objects and the different pieces of furniture
This parser has been validated only on Human navigation environments.
Modification might be required for Interactive Cleanup and handyMan environments.
Latest update: 04/04/18
Authors: A. Magassouba


The environment and target object can be  edited directly from message.txt

example:  "task_info":[{"environment":environment_file_name,"target":object_id,"destination":destination_id}]

launch: python3 prefab_parser.py 

Expected ouptut:
----Target Object----

petbottle_500ml_empty_01

Unity id:1634081557793908

target position: {'x': 4.277, 'z': 2.1549997, 'y': 0.57827115}

----Graspable Objects----

name: petbottle_500ml_empty_01, position: {'x': 4.277, 'z': 2.1549997, 'y': 0.57827115}

name: petbottle_2l_full_01, position: {'x': 4.29, 'z': 1.8599998, 'y': 0.5782712}

name: petbottle_500ml_full_01, position: {'x': 4.29, 'z': 2.4479997, 'y': 0.57827115}

-----Pieces of furniture----

name: trashbox_01, position: {'x': 0, 'z': 0, 'y': 0}

name: trashbox_01, position: {'x': 4.5683002, 'z': 0.6308999, 'y': 0}



pylint score: 9.20
