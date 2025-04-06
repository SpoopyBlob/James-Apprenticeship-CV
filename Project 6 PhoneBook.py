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
    
    def set_value(self, value):
        self.value = value


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

        while current_node != None:
            if current_node.get_key() == key:
                return current_node
            current_node = current_node.get_next_node()

        return None
    
    def remove_node(self, key):
        node = self.find_node(key)
        if node == None:
            return None

        elif self.head_node == node:
            self.head_node = node.get_next_node()
            node.set_prev_node(None)

        elif self.tail_node == node:
            self.tail_node = node.get_prev_node()
            node.set_next_node(None)

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

        key_exist = self.array[array_index].find_node(key)

        if key_exist == None:
            self.array[array_index].add_node(key, value)
            print(f"{key} has been added to your contact")
        else:
            valid_input = False
            while valid_input == False:
                user_input = input("Contact already exists, would you like to overwrite the number? Y/N: ")
                if user_input.upper() == "Y":
                    key_exist.set_value(value)
                    print(f"{key}'s number has been updated!")
                    valid_input = True
                elif user_input.upper() == "N":
                    print(f"{key}'s details have not been updated")
                    valid_input = True
                else:
                    print("Invalid input, try again.")


    def get(self, key):
        hash_value = self.hash(key)
        array_index = self.compressor(hash_value)

        node = self.array[array_index].find_node(key)

        if node == None:
            print("Contact does not exist.")
        else:
            print(f"Contact: {node.get_key()} | Number: {node.get_value()} | Array Index: {array_index}")

    def remove(self, key):
        hash_value = self.hash(key)
        array_index = self.compressor(hash_value)

        node = self.array[array_index].find_node(key)

        if node == None:
            print("Contact does not exist")
            return

        self.array[array_index].remove_node(key)
        print(f"{key} has been removed")

    def print_contact_list(self):
        for node in self.array:
            node.show_list()
    
def handle_user_input(hashmap):
    user_input = input("")

    if user_input == "1":
        key = input("Enter contacts name: ")
        value = input(f"Enter {key}'s number:")
        add_contact(key, value, hashmap)
    elif user_input == "2":
        key = input("Enter contact's name: ")
        remove_contact(key, hashmap)
    elif user_input == "3":
        key = input("Enter contact's name: ")
        view_contact(key, hashmap)
    elif user_input == "4":
        view_all_contacts(hashmap)
    elif user_input == "5":
        key = input("Enter contact's name: ")
        new_value = input(f"Enter {key}'s new number: ")
        change_contact_number(key, new_value, hashmap)
    elif user_input == "6":
        return False
    
    return True
#1
def add_contact(key, value, hashmap):
    hashmap.set(key, value)
#2
def remove_contact(key, hashmap):
    hashmap.remove(key)
#3
def view_contact(key, hashmap):
    hashmap.get(key)
#4
def view_all_contacts(hashmap):
    hashmap.print_contact_list()
#5
def change_contact_number(key, new_value, hashmap):
    hash_value = hashmap.hash(key)
    array_index = hashmap.compressor(hash_value)

    contact = hashmap.array[array_index].find_node(key)

    if contact == None:
        print("Contact dose not exist")
        return
    
    contact.set_value(new_value)
    print(f"{key}'s number has been changed to {new_value}")



contacts = HashMap(5)
running = True
while running == True:

    print("""
      
[1] add contact
[2] remove contact
[3] view contact
[4] view all contacts
[5] change contact number   
[6] exit program
          
    """)

    running = handle_user_input(contacts)
