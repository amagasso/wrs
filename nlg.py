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


def get_instance_id(loaded_file, index):
    """Get the target object ID from the task_info message

    :param loaded_file:

    """
    inst_id = loaded_file["task_info"][index]["target"]
    return inst_id


def get_target_pos(loaded_file, index):
    """Get the target object position from the task_info message

    :param loaded_file:

    """
    pos = loaded_file["task_info"][index]["position"]
    return pos


def load_dict(loaded_file):
    """Load a dictionary

    :param loaded_file:

    """
    with open(loaded_file, encoding='utf-8') as data_file:
        loaded_dict = json.loads(data_file.read())
    return loaded_dict


def id_to_class(inst_id):
    """Transform the instance ID to the corresponding class

    :param inst_id:

    """
    id_class = inst_id.split('_', 1)[0]
    return id_class


def id_to_part_id(inst_id):
    """Retrieve the partial information id from the instance ID

    :param inst_id:

    """
    descr_list = inst_id.split('_')
    obj_descr = []
    for i in range(1, len(descr_list)-1):
        obj_descr.append(descr_list[i])
    return obj_descr


def load_key_value(key, loaded_dict):
    """Get the value of a key from a given dictionary

    :param key:
    :param loaded_dict:

    """
    if key in loaded_dict:
        return loaded_dict[key]
    else:
        return "not found"


def id_to_target_name_by_class(ins_id, loaded_dict):
    """Get the name of the target object from the instance ID

    :param ins_id:
    :param loaded_dict:

    """
    id_class = id_to_class(ins_id)
    return load_key_value(id_class, loaded_dict)


def pos_to_room_id(env, pos):
    """Get the room corresponding to a given position
    :param env:
    :param pos:
    """
    for item in env:
        if(pos["x"] > item["tl_x"] and pos["x"] < item["br_x"] and
           pos["y"] > item["tl_y"] and pos["y"] < item["br_y"]):
            return item["id"]
    return None


def pos_to_furniture_id(furniture, pos):
    """Get the piece of furniture in which is positioned the target object

    :param furniture:
    :param target_x:
    :param target_y:
    :param target_z:

    """
    for item in furniture:
        if(pos["x"] > item["x_c"]-item["d_x"]/2. and pos["x"] < item["x_c"] +
           item["d_x"]/2. and pos["y"] > item["y_c"]-item["d_y"]/2. and
           pos["y"] < item["y_c"]+item["d_y"]/2.):
            return item["id"]
    return None


def get_fur_name(fur_id, loaded_dict):
    """Get the piece of furniture name from it's id

    :param fur_id:
    :param loaded_dict:

    """
    id_class = id_to_class(fur_id)
    if id_class in loaded_dict:
        return loaded_dict[id_class]
    else:
        return "not found"


def room_name_to_command(room_name):
    """Return the command instruction to go in the appropriate room

    :param room_name:

    """
    return "Go to the " + room_name


def furniture_name_to_command(furniture_name):
    """Return the command instruction to find the appropriate piece of furniture

    :param furniture_name:

    """
    return "Find the " + furniture_name


def obj_name_to_command(furniture_name, rel_name, obj_name):
    """Return the command instruction to take the correct object

    :param furniture_name:
    :param rel_name:
    :param obj_name:

    """
    return "Take the " + obj_name + " " + rel_name + " the " + furniture_name


def relationship_descr(relationship_dict, room_name, fur_name):
    """Get the relationship between the target object and piece of furniture
       or location. This function will be updated with more complex
       relationships

    :param relationship_dict:
    :param room_name:
    :param fur_name:

    """
    if fur_name != "not found":
        relationship = load_key_value(fur_name, relationship_dict)
    else:
        relationship = load_key_value(room_name, relationship_dict)
    return relationship


if __name__ == '__main__':
    # get name of the object from the instance ID
    # (unity->)message #json
    TASK_INFO = load_dict('message.txt')
    INS_ID = get_instance_id(TASK_INFO, 1)
    OBJ_DICT = load_dict('obj_class.dict')
    OBJ_NAME_BY_CLASS = id_to_target_name_by_class(INS_ID, OBJ_DICT)
    print('object: ' + OBJ_NAME_BY_CLASS)

    # get landmark description
    ENV = load_dict('map.dat')
    FUR = load_dict('furniture.dat')
    FUR_DICT = load_dict('fur.dict')
    TARGET_POS = get_target_pos(TASK_INFO, 1)
    ROOM_NAME = pos_to_room_id(ENV, TARGET_POS)
    FUR_ID = pos_to_furniture_id(FUR, TARGET_POS)
    FUR_NAME = get_fur_name(FUR_ID, FUR_DICT)
    print('room name: ' + ROOM_NAME)
    print('piece of furniture: ' + FUR_NAME)

    # get relationship description
    REL_DICT = load_dict('relationship.list')
    REL = relationship_descr(REL_DICT, ROOM_NAME, FUR_NAME)
    print('relation: ' + REL)

    # final sentences
    # PHRASE = "The " + OBJ_NAME_BY_CLASS + " is " + REL + " the " + ROOM_NAME
    # if FUR_NAME is not None:
    #    PHRASE = PHRASE + " " + FUR_NAME
    # print('generated sentence: ' + PHRASE)
    print(room_name_to_command(ROOM_NAME))
    print(furniture_name_to_command(FUR_NAME))
    print(obj_name_to_command(FUR_NAME, REL, OBJ_NAME_BY_CLASS))
