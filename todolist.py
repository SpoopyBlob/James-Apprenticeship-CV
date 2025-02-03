#Todo: 
#Check strings for better wording and punctuation

import csv
from datetime import datetime

#Filename function, to clean up code and stop repatition
def file_name(username = "user", mode = "default"):
    if mode == "default":
        filename = "{username}_list.csv".format(username = username)
        return filename
    elif mode == "valid_users":
        filename = "valid_users.csv"
        return filename

#This function checks to see if the user already has a profile     
def user_check():
    
    username = input("Enter your name: ")
    filename = file_name(mode = "valid_users")
    file = read_file(filename)

    for user in file:
        if user["name"] == username.upper():
            return "valid_user", username

    print("I'm sorry, there is no user under that name.")
    print("To create a new user type \"0\"")
    answer = input("or type any other character to exit: ")
            
    if answer == "0":
        return "new_profile", username
              
#This function creates a new profile
def new_profile(username):
    
    fields_for_valid_users = ["name"]
    filename = file_name(username)

    task = input("Enter your first task for your todo list: ")
    task_date = date_string_converter(input("With the format DD/MM/YYYY enter your deadline: "))
    if task_date == "exit":
        return task_date
    current_date = datetime.now().replace(microsecond=0)
 
    task_todo = {
        "id": 0, 
        "task": task, 
        "deadline": task_date, 
        "start_timestamp": current_date, 
        "status": False,
        "before_del_status": "N/A",
        "end_timestamp": "N/A"
    }

    write_file(filename, task_todo, "new_profile")
    write_file(mode = "valid_users", user = username)
    return "Success"

#This function handels dates
def date_string_converter(date):
    valid = False
    check = 0
    while valid == False:
        check = 0
        split_string = date.split()
        print(split_string)
        #days in months  0   1   2   3   4   5   6   7   8   9   10  11
        #                jan feb mar apr may jun jul aug sep oct nov dec
        days_in_month = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        
        #month
        string_month_list = []
        for i in range(1, 13):
            if i < 10:
                string_month_list.append("0" + str(i))
            else:
                string_month_list.append(str(i))
        if split_string[1] in string_month_list:
            check += 1

        #year + change feb/m02 if it is leap year
        if len(split_string[2]) == 4:
            check += 1
            if float(split_string[2]) % 4 == 0 and float(split_string[2]) % 100 != 0:
                days_in_month[1] = 29
            elif float(split_string[2]) % 400 == 0:
                days_in_month[1] = 29
            
    
        #day
        if int(split_string[1]) - 1 < 12:
            month_index = int(split_string[1]) - 1
            string_day_list = []
            for i in range(1, int(days_in_month[month_index]) + 1):
                if i < 10:
                    string_day_list.append("0" + str(i))
                else:
                    string_day_list.append(str(i))
            if split_string[0] in string_day_list:
                check += 1
                
        if check == 3:
            valid = True
        
        if valid == False:
            date = input("I'm sorry, the format or date was invalid, please re-enter the date (DD MM YYYY), or to exit back to the menu type E:")    
            if date.upper() == "E":
                valid = True

    if check == 3:
        date_string = datetime.strptime(date, "%d %m %Y")
        return date_string
    else:
        return "exit"
    

#This is the main page
def main_page(username):
    print("Hello {username}! This is your current profile.".format(username=username))
    present_list(username)
 
    message = "Controls: A to append list | C to mark task as complete | M to modify list | D to delete/undelete tasks | E to exit the program:   "
    print("-" * len(message))
    print(message)
    print("-" * len(message))
    user_input = input()

    return user_input

#append a list
def append_list(username):
    filename = file_name(username)
    file = read_file(filename)


    task = input("Enter your task: ")
    task_date = date_string_converter(input("With the format DD MM YYYY, as in 02 02 2025 enter your deadline: "))
    if task_date == "exit":
        return 
    current_date = datetime.now().replace(microsecond=0)
    id_num = id_check(username)

    task_todo = {
        "id": id_num,
        "task": task, 
        "deadline": task_date, 
        "start_timestamp": current_date, 
        "status": False,
        "before_del_status": "N/A",
        "end_timestamp": "N/A"
    }

    file.append(task_todo)
    write_file(filename, file)
    
#presents list to screen
def present_list(username):
    filename = file_name(username)
    file = read_file(filename)
    
    #Tasks in progress print
    in_progress = "Tasks in progress" 
    print(in_progress)
    print("-" * len(in_progress))
    
    row_count = 0
    true_count = 0
    for row in file:
        row_count += 1
        if row['status'] == "False":
            time_left = datetime.strptime(row["deadline"], "%Y-%m-%d %H:%M:%S" ) - datetime.now()
            print("ID: {id} | Task: {task} | Deadline: {deadline} | Time left: {time_left}".format(id = row["id"], task=row["task"], deadline=row["deadline"], time_left=time_left))
        else:
            true_count += 1
            
    if true_count == row_count:
        print("There are no tasks in progress")
        
    #Tasks in progress print
    complete = "Tasks completed" 
    print(complete)
    print("-" * len(complete))

    row_count = 0
    true_count = 0
    for row in file:
        row_count += 1
        if row['status'] == "True":
            time_past = datetime.strptime(row["end_timestamp"], "%Y-%m-%d %H:%M:%S" ) - datetime.strptime(row["start_timestamp"], "%Y-%m-%d %H:%M:%S") 
            print("ID: {id} | Task: {task} | Deadline: {deadline} | This took: {time_past}".format(id = row["id"], task=row["task"], deadline=row["deadline"], time_past=time_past))
        else:
            true_count += 1
            
    if true_count == row_count:
        print("There are no tasks completed")


#checks what the next ID in the list is
def id_check(username):
    filename = file_name(username)
    file = read_file(filename)
        
    id_check = 0
    for row in file:
        id_check += 1
    
    return id_check

#marks task as complete
def mark_task_complete(username):
    
    entered_id = input("Enter task ID: ")
    filename = file_name(username)
    file = read_file(filename)

    id_valid = False
    for row in file:
        
        if row["id"] == entered_id and row["status"] == "False":
            check = input("Are you sure, Y for yes, N for no: ")
            if check.upper() == "Y":
                row["status"] = "True"
                row["end_timestamp"] = datetime.now().replace(microsecond=0)
                id_valid = True
            if check.upper() == "N":
                return
        elif row["id"] == entered_id and row["status"] == "True":
            exit_function("This task is already complete")
            return
            
    if id_valid == False:
        exit_function("You have entered a invalid ID")
        return
    
    write_file(filename, file)

#allows you to modify, status of completed tasks, the task and deadline.
def modify_list(username):
    list_id = input("Enter ID: ")
    filename = file_name(username)
    file = read_file(filename)

    for rows in file:
        if list_id == rows["id"]:
            user_input = input("You can modify the following, deadline (D), task (T) or status (S): ")
                
            #Status
            if user_input.upper() == "S":
                if rows["status"] == "False":
                    exit_function("This function only allows you to mark a task as uncomplete, to mark a task as complete, click M within the current profile page")
                    return
                elif rows["status"] == "True":
                    next_input = input("This task is marked as complete, would you like to mark this task uncomplete, yes (Y) or no (any other character): ")
                    if next_input.upper() == "Y":
                        rows["status"] = "False"
                        rows["end_timestamp"] = "N/A"
                    else:
                        return

            #Task
            elif user_input.upper() == "T":
                next_input = input("Please write the modified task here: ")
                third_input = input("To confirm, you would like to change {og_task} to {new_task}. Yes (Y) or No (any other character): ".format(og_task=rows["task"], new_task=next_input))
                if third_input.upper() == "Y":
                    rows["task"] = next_input
                else:
                    return

            #Deadline
            elif user_input.upper() == "D":
                if rows["status"] == "True":
                    exit_function("I'm sorry, this task is marked as complete, to change the deadline you will need to mark the task as uncomplete")
                    return
                    
                    return
                elif rows["status"] == "False":
                    next_input = input("With the format DD MM YYYY enter your new deadline: ")
                    date = date_string_converter(next_input)
                    third_input = input("To confirm, you would like to change your deadline from {og_deadline} to {new_deadline}, yes (Y) or no (any character)".format(og_deadline=rows["deadline"], new_deadline=date))
                    if third_input.upper() == "Y":
                        rows["deadline"] = date
                    else:
                        return
                
                #Invalid input
            else:
                exit_function("Im sorry, the input your entered is invalid")
                return
    
    write_file(filename, file)

def delete_undelete_file (username):
    filename = file_name(username)
    file = read_file(filename)

    user_input = input("To delete a file type 0, to un-delete a file type 1")
    
    #undelete file
    if user_input == "1":
        print("Here are you previously deleted tasks")
        count = 0
        for row in file:
            if row["status"] == "del":
                print("ID: {id}, Task: {task}".format(id=row["id"], task=row["task"]))
                count +=1
        if count == 0:
            exit_function("You have no deleted tasks.")
            return
        second_input = input("Please enter the ID of the task you would like to un-delete")
        valid_id = False
        for row in file:
            if second_input == row["id"] and row["status"] == "del":
                status_before = row["before_del_status"]
                row["status"] = status_before
                write_file(filename, file)
                valid_id = True
                return
            elif second_input == row["id"] and row["status"] != "del":
                exit_function("It looks like the task wasnt actually deleted, so theres no need to undo anything.")
                return
        if valid_id == False:
                exit_function("This ID dosen't match with any existing task.")
                return
    #delete file
    elif user_input == "0":
        print("Here are your tasks: ")
        for row in file:
            if row["status"] != "del":
                print("ID: {id}, Task: {task}".format(id=row["id"], task=row["task"]))
        entered_id = input("Please enter the ID of the task you would like to delete")
        valid_id = False
        for row in file:
            if entered_id == row["id"] and row["status"] != "del":
                current_status = row["status"]
                row["before_del_status"] = current_status
                row["status"] = "del"
                write_file(filename, file)
                valid_id = True
                return
            elif entered_id == row["id"] and row["status"] == "del":
                exit_function("This task has already been deleted.")
                return
        if valid_id == True:
                exit_function("You have entered in an invalid ID.")

#I created this function so that the user can read the text before being sent back to the main page and flooded with information
def exit_function(string):
    exit_condition = False
    while exit_condition == False:
        user_input = input("{string} To go back to the main page, type E".format(string=string))
        if user_input.upper() == "E":
            exit_condition = True

#reads file
def read_file(filename):
    contents = []
    with open(filename, "r") as file:
        reader_object = csv.DictReader(file)
        contents = [row for row in reader_object]
    return contents

#writes file 
def write_file(filename = "optional", list = [], mode = "default", user = "N/A"):
    field_names = ["id", "task", "deadline", "start_timestamp", "status", "before_del_status", "end_timestamp"]
    
    if mode == "default":
        with open(filename, "w") as file:
            writer_object = csv.DictWriter(file, fieldnames=field_names)

            writer_object.writeheader()
            writer_object.writerows(list)
    elif mode == "new_profile":
        with open(filename, "w") as file:
            writer_object = csv.DictWriter(file, fieldnames=field_names)

            writer_object.writeheader()
            writer_object.writerow(list)
    elif mode == "valid_users":
        with open("valid_users.csv", 'a') as valid_user:

            #Creates a writer object that can be used to alter the file
            file_writer_2 = csv.writer(valid_user)
            file_writer_2.writerow([user.upper()])

#Main Body
start_run = False
username = ""
while start_run == False:
    user_find, username = user_check()

    if user_find == "new_profile":
        exit_handeling = new_profile(username)
        if exit_handeling == "exit":
            continue
    elif user_find == "valid_user":
        start_run = True


running = True
while running == True:
    
    user_input = main_page(username)
    
    if user_input.upper() == "A":
        append_list(username)
    elif user_input.upper() == "C":
        mark_task_complete(username)
    elif user_input.upper() == "M":
        modify_list(username)
    elif user_input.upper() == "D":
        delete_undelete_file(username)
    elif user_input.upper() == "E":
        running = False





    

