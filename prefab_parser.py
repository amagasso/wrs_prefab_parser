#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""WRS 2018.
This module is designed for Human Navigation in virtual space.
This module is composed of functions allowing to generate a sentence to
describe the position of a target object.

Latest update: 04/03/18
Authors: A. Magassouba

"""

import json
import yaml


def remove_unity_tag_alias(filepath):
    """
    Inspired and adapted from:
    https://stackoverflow.com/questions/21473076/pyyaml-and-unusual-tags

    Name:               remove_unity_tag_alias()

    Description:        Loads a file object from a Unity textual scene file,
                        which is in a pseudo YAML style, and strips the
                        parts that are not YAML 1.1 compliant. Then returns a
                        string as a stream, which can be passed to PyYAML.
                        Essentially removes the "!u!" tag directive, class
                        type and the "&" file ID directive. PyYAML seems to
                        handle rest just fine after that.

    Returns:                String (YAML stream as string)


    """
    result = str()
    source_file = open(filepath, 'r')
    cpt = 0
    for line_number, line in enumerate(source_file.readlines()):
        if line.startswith('%'):
            result += line
        else:
            if line.startswith('--- !u!'):
                # create a new id tag
                m_id = '  m_Id: ' + line.split('&')[1] + '\n'
                cpt = 0
                result += '---' + '\n'
            else:
                # add on the second line of the class the id
                if cpt == 2:
                    result += m_id
                    cpt = cpt+1
                else:
                    # Just copy the contents...
                    result += line
                    cpt = cpt+1

    source_file.close()
    return result


def load_prefab(prefab_file):
    """Load the scene from a yaml file

    :param prefab_file:

    """
    env = []
    data_loaded = yaml.load_all(prefab_file)
    for data in data_loaded:
        env.append(data)
    return env


def get_unity_id(prefab_env, ins_id):
    """Get the object unity ID from it's instance id

    :param prefab_env:
    :param unity_id:

    """
    for node in prefab_env:
        if 'GameObject' in node.keys():
            if node['GameObject']['m_Name'] == ins_id:
                return node['GameObject']['m_Id']
    return -1


def get_obj_id_from_unity_id(prefab_env, unity_id):
    """Get the object instance id from it's unity ID

    :param prefab_env:
    :param unity_id:

    """
    for node in prefab_env:
        if 'GameObject' in node.keys():
            if node['GameObject']['m_Id'] == unity_id:
                return node['GameObject']['m_Name']
    return "unknown id"


def get_object_position(prefab_env, unity_id):
    """Get the 3d position of an object from it's unity ID

    :param prefab_env:
    :param unity_id:

    """
    for node in prefab_env:
        if 'Transform' in node.keys():
            if node['Transform']['m_GameObject']['fileID'] == unity_id:
                return node['Transform']['m_LocalPosition']

    return {}


def get_all_graspable_object_id(prefab_env):
    """Get all graspable objects unity ID in the environment

    :param prefab_env:

    """
    id_list = []
    for node in prefab_env:
        if 'GameObject' in node.keys():
            if node['GameObject']['m_TagString'] == 'Graspables':
                id_list.append(node['GameObject']['m_Id'])
    return id_list


def get_furniture_id(prefab_env):
    """Get all pieces of furniture unity ID in the environment

    :param prefab_env:

    """
    fur = []
    for node in prefab_env:
        if 'GameObject' in node.keys():
            if node['GameObject']['m_TagString'] == "Destination":
                fur.append(node['GameObject']['m_Id'])
    return fur


def get_instance_id(loaded_file):
    """Get the target object ID from the task_info message

    :param loaded_file:

    """
    inst_id = loaded_file["task_info"][0]["target"]
    return inst_id


def get_env_id(loaded_file):
    """Get the env ID from the task_info message

    :param loaded_file:

    """
    env_id = loaded_file["task_info"][0]["environment"]
    return env_id


def load_dict(loaded_file):
    """Load a dictionary

    :param loaded_file:

    """
    with open(loaded_file, encoding='utf-8') as data_file:
        loaded_dict = json.loads(data_file.read())
    return loaded_dict

if __name__ == '__main__':
    # get target  instance ID from task info
    # (unity->)message #json

    # get target position in the scene
    print("----Target Object----")
    TASK_INFO = load_dict('message.txt')
    INS_ID = get_instance_id(TASK_INFO)
    print(INS_ID)
    UNITY_ENV = get_env_id(TASK_INFO)+".prefab"
    NO_TAG_YAML = remove_unity_tag_alias(UNITY_ENV)
    ENV = load_prefab(NO_TAG_YAML)
    U_ID = get_unity_id(ENV, INS_ID)
    print('Unity id:' + str(U_ID))
    TARGET_POS = get_object_position(ENV, U_ID)
    print('target position: ' + str(TARGET_POS))

    # get all graspable objects and their positions
    GRASP = get_all_graspable_object_id(ENV)
    print("----Graspable Objects----")
    for U_ID in GRASP:
        print('name: ' + get_obj_id_from_unity_id(ENV, U_ID) + ', position: ' +
              str(get_object_position(ENV, U_ID)))

    # get all piece of furniture and their positions
    DEST = get_furniture_id(ENV)
    print("-----Pieces of furniture----")
    for F_ID in DEST:
        print('name: ' + get_obj_id_from_unity_id(ENV, F_ID) + ', position: ' +
              str(get_object_position(ENV, F_ID)))
