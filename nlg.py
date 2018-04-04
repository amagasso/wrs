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


def get_instance_id(loaded_file):
    """Get the target object ID from the task_info message

    :param loaded_file:

    """
    inst_id = loaded_file["task_info"][0]["target"]
    return inst_id


def get_target_pos(loaded_file):
    """Get the target object position from the task_info message

    :param loaded_file:

    """
    pos = loaded_file["task_info"][0]["position"]
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


def pos_to_room_id(env, target_x, target_y, target_z):
    """Get the room in which is positioned the target object

    :param env:
    :param target_x:
    :param target_y:
    :param target_z:

    """
    #unused parameter for now target_z
    for item in env:
        if(target_x > item["tl_x"] and target_x < item["br_x"] and
           target_y > item["tl_y"] and target_y < item["br_y"]):
            return item["id"]
    return None


def pos_to_furniture_id(furniture, target_x, target_y, target_z):
    """Get the piece of furniture in which is positioned the target object

    :param furniture:
    :param target_x:
    :param target_y:
    :param target_z:

    """
    #unused parameter for now target_z
    for item in furniture:
        if(target_x > item["x_c"]-item["d_x"]/2. and target_x < item["x_c"] +
           item["d_x"]/2. and target_y > item["y_c"]-item["d_y"]/2. and
           target_y < item["y_c"]+item["d_y"]/2.):
            return item["id"]


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
    INS_ID = get_instance_id(TASK_INFO)
    OBJ_DICT = load_dict('obj_class.dict')
    OBJ_NAME_BY_CLASS = id_to_target_name_by_class(INS_ID, OBJ_DICT)
    print(OBJ_NAME_BY_CLASS)

    # get landmark description
    ENV = load_dict('map.dat')
    FUR = load_dict('furniture.dat')
    FUR_DICT = load_dict('fur.dict')
    TARGET_POS = get_target_pos(TASK_INFO)
    ROOM_NAME = pos_to_room_id(ENV, TARGET_POS["x"], TARGET_POS["y"],
                               TARGET_POS["z"])
    FUR_ID = pos_to_furniture_id(FUR, TARGET_POS["x"],
                                 TARGET_POS["y"], TARGET_POS["z"])
    FUR_NAME = get_fur_name(FUR_ID, FUR_DICT)
    print(ROOM_NAME)
    print(FUR_NAME)

    # get relationship description
    REL_DICT = load_dict('relationship.list')
    REL = relationship_descr(REL_DICT, ROOM_NAME, FUR_NAME)
    print(REL)

    # final sentence
    PHRASE = "The " + OBJ_NAME_BY_CLASS + " is " + REL + " " + ROOM_NAME
    if FUR_NAME is not None:
        PHRASE = PHRASE + " the " + FUR_NAME
    print(PHRASE)
