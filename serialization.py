import pickle
def serialize(file, item):
    with open(file, 'wb+') as f:
        pickle.dump(item, f)

def deserialize(file):
    stored_obj_dict = dict()
    try:
        with open(file, 'rb+') as f:
            stored_obj_dict = pickle.load(f)
    except:
        stored_dict = {}
    return stored_obj_dict
