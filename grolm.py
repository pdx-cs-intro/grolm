# GROLM: A GROcery List Manager
# Bart Massey 2021

class GroceryListItem:
    def __init__(self, name, quantity):
        assert quantity > 0
        self.name = name
        self.quantity = quantity

    def repr(self):
        if self.quantity == 1:
            return self.name
        return f"{self.name} ({self.quantity}×)"

def read_item(repr):
    if '(' in repr:
        qstart = repr.rindex('(')
        qend = repr.rindex('×')
        # XXX This uses python's substring slicing, which
        # is sort of an advanced topic.
        name = repr[:qstart]
        quantity = int(repr[qstart + 1:qend])
    else:
        name = repr
        quantity = 1
    name = name.strip()
    assert name != ""
    return GroceryListItem(name, quantity)

class GroceryList:
    def __init__(self):
        self.items = []
        self.filename = None
    
    def set_filename(self, filename):
        self.filename = filename

    def add(self, item):
        self.items.append(item)

    def show(self):
        for item in self.items:
            print(item.repr())

    def save(self):
        assert self.filename != None
        f = open(self.filename, "w")
        for item in self.items:
            print(item.repr(), file=f)
        f.close()

    def load(self):
        assert self.filename != None
        f = open(self.filename, "r")
        for repr in f:
            item = read_item(repr)
            self.items.append(item)

groceries = GroceryList()

while True:
    command = input("> ")
    words = command.split()
    nwords = len(words)
    if nwords == 0:
        continue
    elif words[0] == "quit" and nwords == 1:
        break
    elif words[0] == "add" and nwords >= 2:
        quantity = 1
        if len(words) >= 3:
            maybe_quantity = words[len(words) - 1]
            if maybe_quantity.isdigit():
                quantity = int(maybe_quantity)
                words.pop()
        name = ' '.join(words[1:])
        item = GroceryListItem(name, quantity)
        groceries.add(item)
    elif words[0] == "show" and nwords == 1:
        groceries.show()
    elif words[0] == "file" and nwords == 2:
        groceries.set_filename(words[1])
    elif words[0] == "load" and nwords == 1:
        groceries.load()
    elif words[0] == "save" and nwords == 1:
        groceries.save()
    else:
        print("unknown command")
