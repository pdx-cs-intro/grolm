# GROLM: A GROcery List Manager
# Bart Massey 2021

# A single type of grocery, together with its quantity.
class GroceryListItem:
    def __init__(self, name, quantity):
        assert quantity > 0
        self.name = name
        self.quantity = quantity

    # Show this item in viewable form.
    def repr(self):
        if self.quantity == 1:
            return self.name
        return f"{self.name} ({self.quantity}×)"

# Test that we can create and view grocery items.
test_grocery = GroceryListItem("canned peas", 1)
assert test_grocery.repr() == "canned peas"
test_grocery = GroceryListItem("canned peas", 3)
assert test_grocery.repr() == "canned peas (3×)"


# Given a grocery list item description string, return an
# appropriate item.
def read_item(desc):
    # XXX Any left paren in desc is assumed
    # to be the start of a quantity.
    if '(' in desc:
        qstart = desc.rindex('(')
        qend = desc.rindex('×')
        # XXX This uses python's substring slicing, which
        # is sort of an advanced topic.
        name = desc[:qstart]
        quantity_str = desc[qstart + 1:qend]
        assert quantity_str.isdigit()
        quantity = int(quantity_str)
    else:
        name = desc
        quantity = 1
    name = name.strip()
    assert name != ""
    return GroceryListItem(name, quantity)

# Grocery list, a list of items.
class GroceryList:
    def __init__(self):
        self.items = []
        self.filename = None
    
    # Set name of file for load / save.
    def set_filename(self, filename):
        self.filename = filename

    # Add a grocery list item at the end of the list.
    def add(self, item):
        self.items.append(item)

    # Print the current list.
    def show(self):
        for item in self.items:
            print(item.repr())

    # Save list to file given by current filename.
    def save(self):
        assert self.filename != None
        f = open(self.filename, "w")
        for item in self.items:
            print(item.repr(), file=f)
        f.close()

    # Load list from file given by current filename.
    def load(self):
        assert self.filename != None
        f = open(self.filename, "r")
        for desc in f:
            item = read_item(desc)
            self.add(item)
        f.close()

# Test some basic functions of the grocery list.
test_groceries = GroceryList()
test_groceries.add(read_item("canned peas"))
test_groceries.add(GroceryListItem("milk", 2))
assert test_groceries.items[1].quantity == 2

# The grocery list we are managing.
groceries = GroceryList()

# Process grocery list commands.
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
            # Assume a number on the end is a quantity.
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
