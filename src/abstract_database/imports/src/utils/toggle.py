from .imports import *
def get_all_case(objs):
    objs = make_list(objs or [])
    objs_copy = objs.copy()
    new_objs = []
    for i,obj in enumerate(objs):
        new_objs.append(obj)
        if isinstance(obj,str):
            new_objs.append(obj.lower())
            new_objs.append(obj.upper())
    return list(set(new_objs))
def is_true(obj):
    trues = get_all_case([True,'true','tru',1,float(1),'1'])
    if obj in trues:
        return True
    return False
def is_false(obj):
    falses = get_all_case([False,'false','fals',0,float(0),'0'])
    if obj in falses:
        return True
    return False
def toggle_var(obj):
    if is_true(obj):
        return False
    if is_false(obj):
        return True
    if obj:
        return False
    return True
