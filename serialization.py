import pickle
def serialize(file, item):
    with open(file, 'wb+') as f:
        pickle.dump(item, f)

def deserialize(file):
    try:
        with open(file, 'rb+') as f:
            items = pickle.load(f)
    except:
        print(error)
