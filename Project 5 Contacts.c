//Note: I won't be using structs within this code, I'm sticking to my learning plan and only using what I have learned to reinforce the knowledge that I have gained
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>

void resize_pointer_array (char*** contactNames, char*** contactNumbers, int maxSize);
void allocate_new_contact (char*** contactNames, char*** contactNumbers, int contactSize);

int main (void) {
    int contactSize = 0;
    int maxSize = 1;
    //I'm using malloc to create an "array" in memory that stores the pointers to strings
    //I use char** to store the pointers of the contact names and phone numbers
    //I use sizeof(char*) instead of char because each element in char** is a pointer to a char. I'm allocating memory for the pointer itself
    char** contactNames = malloc(maxSize * sizeof(char*));
    char** contactNumbers = malloc(maxSize * sizeof(char*));
    bool running = true;

    while (running == true) {
        printf("\n\nMain Page:\n"); 
        
        //Displays my contacts
        for (int i = 0; i < contactSize; i++) {
            printf("Contact %i:\n", i + 1);
            printf("Name: %s\n", contactNames[i]);
            printf("Number: %s\n\n", contactNumbers[i]);
        }

        printf("To add a new contact (1), to remove contacts (2), to exit (3)\n");
        char user_input;
        scanf("%c", &user_input);
        //clears scanf function
        while (getchar() != '\n');

        if (user_input == '1') {
            printf("\nEnter your contacts name\n");
            char name[30];
            //29 in our %29s limits the characters to 29 characters
            scanf("%29s", name);
            while (getchar() != '\n');

            printf("\nEnter your contacts number\n");
            char number[15];
            scanf("%14s", number);
            while (getchar() != '\n');

            maxSize++;
            resize_pointer_array(&contactNames, &contactNumbers, maxSize);
            allocate_new_contact(&contactNames, &contactNumbers, contactSize);

            strcpy(contactNames[contactSize], name);
            strcpy(contactNumbers[contactSize], number);
            contactSize++;
            
        } else if (user_input == '2') {
            printf("\nEnter the name of the contact you would like to remove: \n");
            char name[30];
            scanf("%29s", name);
            while (getchar() != '\n');

            //Finds index
            int index = -1;
            for (int i = 0; i < contactSize; i++) {
                if (strcmp(contactNames[i], name) == 0) {
                    index = i;
                    break;
                } 
            }

            //If index is not found, break
            if (index == -1) {
                printf("\nName not in contacts\n");
                continue;
            } 

            //Access index then shift every other element down one
            for (int i = index; i < contactSize - 1; i++) {
                strcpy(contactNames[i], contactNames[i + 1]);
                strcpy(contactNumbers[i], contactNumbers[i + 1]);
            }

            //Free memory to prevent memory leak
            free(contactNames[contactSize - 1]);
            free(contactNumbers[contactSize - 1]);

            //Update contact size
            contactSize--;

            //Reallocate size of contact list
            maxSize--;
            resize_pointer_array(&contactNames, &contactNumbers, maxSize);
            
        } else if (user_input == '3') {
            printf("\nExit\n");
            running = false;
        } else {
            printf("\nInvalid Input\n");
        }
    }

}

void resize_pointer_array (char*** contactNames, char*** contactNumbers, int maxSize) {
    char** tempNames = realloc(*contactNames, maxSize * sizeof(char*));
    char** tempNumbers = realloc(*contactNumbers, maxSize * sizeof(char*));

    if (tempNames == NULL || tempNumbers == NULL) {
        printf("\nRealloc error, process canceled, try again\n");
    } else {
        *contactNames = tempNames;
        *contactNumbers = tempNumbers;
    }
}

void allocate_new_contact (char*** contactNames, char*** contactNumbers, int contactSize) {
    (*contactNames)[contactSize] = malloc(30 * sizeof(char)); 
    (*contactNumbers)[contactSize] = malloc(15 * sizeof(char));
}
