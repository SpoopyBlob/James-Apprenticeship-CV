class Node:

    def __init__(self, key, value, prev_node = None, next_node = None):
        self.key = key
        self.value = value
        self.prev_node = prev_node
        self.next_node = next_node

    def get_key(self):
        return self.key
    
    def get_value(self):
        return self.value

    def get_next_node(self):
        return self.next_node
    
    def get_prev_node(self):
        return self.prev_node
    
    def set_next_node(self, node):
        self.next_node = node

    def set_prev_node(self, node):
        self.prev_node = node


class LinkedList:

    def __init__(self, head_node = None, tail_node = None):
        self.head_node = head_node
        self.tail_node = tail_node

    def add_node(self, key, value):
        node = Node(key, value)
        self.set_tail_node(node)
    
    def set_tail_node(self, node):
        if self.tail_node == None:
            self.head_node = node
            self.tail_node = node
        else:
            self.tail_node.set_next_node(node)
            node.set_prev_node(self.tail_node)
            self.tail_node = node


    def find_node(self, key):    
        current_node = self.head_node

        if current_node == None:
            return None
    
        if current_node.get_key() == key:
            return current_node
        
        while current_node != None:
            current_node = current_node.get_next_node()
            if current_node == None:
                break
            elif current_node.get_key() == key:
                return current_node

        return None
    
    def remove_node(self, key):
        node = self.find_node(key)
        if node == None:
            return None

        elif self.head_node == node:
            self.head_node = node.get_next_node()
            self.head_node.set_prev_node(None)

        elif self.tail_node == node:
            self.tail_node = node.get_prev_node()
            self.tail_node.set_next_node(None)

        else:
            prev_node = node.get_prev_node()
            next_node = node.get_next_node()

            prev_node.set_next_node(next_node)
            next_node.set_prev_node(prev_node)

        return node  

    def show_list(self):
        current_node = self.head_node
        while current_node != None:
            print(f"Contact {current_node.get_key()} | Number: {current_node.get_value()}")
            current_node = current_node.get_next_node()

class HashMap():
    def __init__(self, size):
        self.array_size = size
        self.array = [LinkedList() for i in range(self.array_size)]

    def hash(self, key, collision = 0):
        key_bytes = key.encode()
        hash_value = sum(key_bytes)

        return hash_value + collision
    
    def compressor(self, hash_value):
        return hash_value % self.array_size
    
    def set(self, key, value):
        hash_value = self.hash(key)
        array_index = self.compressor(hash_value)

        self.array[array_index].add_node(key, value)

    def get(self, key):
        hash_value = self.hash(key)
        array_index = self.compressor(hash_value)

        node = self.array[array_index].find_node(key)

        if node == None:
            print("Contact not found.\n\n")
        else:
            print(f"Contact: {node.get_key()} | Number: {node.get_value()}")
            print(f"Array Index: {array_index}\n\n")

    def remove(self, key):
        hash_value = self.hash(key)
        array_index = self.compressor(hash_value)

        node = self.array[array_index].remove_node(key)
        if node == None:
            print("Error, contact not found")
        else:
            print(f"{key} has been removed")

    def print_contact_list(self):
        for node in self.array:
            node.show_list()
    
contacts = HashMap(5)

contacts.set("James", "07915")
contacts.set("Dude", "0791f5")
contacts.set("Guy", "07w915")
contacts.set("Sheeeee", "0791235")
contacts.set("re", "9387423")
contacts.set("YOOO", "23915")

contacts.get("James")
contacts.get("Dude")
contacts.get("Guy")
contacts.get("Sheeeee")
contacts.get("iudwaid")
contacts.get("re")
contacts.get("YOOO")

contacts.remove("re")

contacts.print_contact_list()
