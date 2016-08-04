def serialize(self, file, item):
    with open(file, 'wb+') as f:
        pickle.dump(item, f)
    with open(file, 'rb') as f:
        items = f.read()

def deserialize(self, file):
    try:
        with open(file, 'rb+') as f:
            items = pickle.load(f)
    except:
        print(error)
