#------------------------------------------#
# Title: CDInventory.py
# Desc: Working with binary files and structured error handling
# Change Log: (Who, When, What)
# DBiesinger, 2030-Jan-01, Created File
# Bill McGinty, 2022-Mar-14, Modified File to add functionality
#------------------------------------------#

import sys
import pickle

# -- DATA -- #
strChoice = ""  # User input
lstTbl = []  # list of lists to hold data
dicRow = {}  # list of data row
strFileName = "CDInventory.dat"  # binary data storage file
objFile = None  # file object


class CDIDoutOfRange(Exception):
    """ custom error class for value not within upper or lower bounds """

    def __str__(self):
        return "CD ID must be greater than 0 and less than 500!"

# -- PROCESSING -- #

class DataProcessor:

    @staticmethod
    def myAddProcCode(myID, myTitle, myArtist):
        """ Function to process ID, Title and Artist

        Args:
            myID (string): ID of CD.
            myTitle (string): Title of CD.
            myArtist (string): Artist name.

        Returns:
            None.

        """
        # Add item to the table
        intID = int(myID)
        dicRow = {"ID": intID, "Title": myTitle, "Artist": myArtist}
        lstTbl.append(dicRow)
        IO.show_inventory(lstTbl)

    def myDeleteDataProcFunc(intIDDelReceived):
        """ Function to delete CD based on ID passed to function

        Args:
            intIDDelReceived (int): ID of CD to delete.

        Returns:
            None.

        """
        # search thru table and delete CD
        intRowNr = -1
        blnCDRemoved = False
        for row in lstTbl:
            intRowNr += 1
            if row["ID"] == intIDDelReceived:
                del lstTbl[intRowNr]
                blnCDRemoved = True
                break
        if blnCDRemoved:
            print("The CD was removed")
        else:
            print("\nCould not find this CD!!!\n")
        IO.show_inventory(lstTbl)  # display inventory
        return


class FileProcessor:
    """Processing the data to and from binary file"""

    @staticmethod
    def read_file(file_name, startTbl):
        """Function to manage data ingestion from file to a list of dictionaries

        Reads the data from file identified by file_name into a 2D table
        (list of dicts) table one line in the file represents one dictionary row in table.

        Structure error handlind added for missing read file

        Args:
            file_name (string): name of file used to read the data from
            table (list of dictionary): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            None.
        """
        try: #structured error handling, display error if file not found
            startTbl.clear()  # this clears existing data and allows to load data from file
            billStrIncr = -1  # disctionary row increment set to zero
            fileObj = open(file_name, "rb")  # open .dat in read binary mode
            billString = pickle.load(fileObj)  # set list billString equal to all pickled objects
            for row in billString:  # parse all rows in list
                billStrIncr += 1
                startTbl.append(billString[billStrIncr]) # appends dictionary row to list of lists
            fileObj.close()
        except FileNotFoundError as e: #detailed error information
            print("\nYou need to create a CDInventory.dat file first!")
            print("Build in error info: ")
            print(type(e), e, e.__doc__, sep="\n")
            print("Exiting Program\n")
            sys.exit()

    @staticmethod
    def write_file(file_name, recTbl):  # save data
        """ Function to save table data to binary file

        Structure error handlind added for missing write file
        Args:
            file_name (string): name of the file used to write data to.
            recTbl (list of dictionary): 2D data structure (list of dicts) that holds the data during runtime.

        Returns:
            None.

        """
        try: #structured error handling, display error if file not found
            fileObj = open(file_name, "wb")  # open .dat in write binary mode
            # write the pickled list of lists to binary file
            pickle.dump(recTbl, fileObj) # write picked data to binary file
            fileObj.close()
        except FileNotFoundError as e: #detailed error information
            print("\nCDInventory.dat is missing!")
            print("Build in error info: ")
            print(type(e), e, e.__doc__, sep="\n")
            print("Exiting Program\n")
            sys.exit()

# -- PRESENTATION (Input/Output) -- #


class IO:
    """Handling Input / Output"""

    @staticmethod
    def print_menu():
        """Displays a menu of choices to the user

        Args:
            None.

        Returns:
            None.
        """

        print(
            "Menu\n\n[l] load Inventory from file\n[a] Add CD\n[i] Display Current Inventory")
        print("[d] delete CD from Inventory\n[s] Save Inventory to file\n[x] exit\n")

    @staticmethod
    def menu_choice():
        """Gets user input for menu selection

        Args:
            None.

        Returns:
            choice (string): a lower case sting of the users input out of the choices l, a, i, d, s or x

        """
        choice = " "
        while choice not in ["l", "a", "i", "d", "s", "x"]:
            choice = input(
                "Which operation would you like to perform? [l, a, i, d, s or x]: ").lower().strip()
        print()  # Add extra space for layout
        return choice

    @staticmethod
    def show_inventory(invTbl):
        """Displays current inventory of table invTbl


        Args:
            invTbl (list of dict): 2D data structure (list of dicts) that holds the data during runtime.

        Returns:
            None.

        """
        print("======= The Current Inventory: =======")
        print("ID\tCD Title (by: Artist)\n")
        for row in invTbl:
            print("{}\t{} (by:{})".format(*row.values()))
        print("======================================")

    @staticmethod
    def myAddIOFunc():
        """ Function for input / ouput
            Ask the user CD ID, Title and Artist

        Returns:
            strID1 (string): User inputted CD ID.
            strTitle1 (string): User inputted CD Title.
            strArtist1 (string): User inputted CD Artist.

        """
        while True:
            strID1 = input("Enter ID: ").strip()
            try: #check if integer and within range
                myTmpID1 = int(strID1)
                if not 0 < myTmpID1 < 500:
                    raise print(CDIDoutOfRange())
            except ValueError as e:
                print("\n")
                print("That is not an Integer!")
                print("Build in error info: ")
                print(type(e), e, e.__doc__, sep="\n")
                continue
            except Exception:
                continue
            while True:
                strTitle1 = input("What is the CDs title? ").strip()
                try: # if blank raise error and start over
                    if len(strTitle1) == 0:
                        raise ValueError("You must enter a Title!")
                except ValueError as e:
                    print("\n")
                    print("Build in error info: ")
                    print(type(e), e, e.__doc__, sep="\n")
                    continue
                while True:
                    strArtist1 = input("What is the Artist\"s name? ").strip()
                    try: # if blank raise error and start over
                        if len(strArtist1) == 0:
                            raise ValueError("You must enter an Artist!")
                    except ValueError as e:
                        print("\n")
                        print("Build in error info: ")
                        print(type(e), e, e.__doc__, sep="\n")
                        continue
                    return strID1, strTitle1, strArtist1


# When program starts, read in the currently saved Inventory
FileProcessor.read_file(strFileName, lstTbl)

# Start main loop
while True:
    # Display Menu to user and get choice
    IO.print_menu()
    strChoice = IO.menu_choice()

    # Process menu selection
    # Process exit first
    if strChoice == "x":
        break
    # Process load inventory
    if strChoice == "l":
        print("WARNING: If you continue, all unsaved data will be lost and the Inventory re-loaded from file.")
        strYesNo = input(
            "type \"yes\" to continue and reload from file. otherwise reload will be canceled: ")
        if strYesNo.lower() == "yes":
            print("reloading...")
            FileProcessor.read_file(strFileName, lstTbl)
            IO.show_inventory(lstTbl)
        else:
            input(
                "canceling... Inventory data NOT reloaded. Press [ENTER] to continue to the menu.")
            IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # Process add a CD
    elif strChoice == "a":
        # Ask user for new ID, CD Title and Artist
        strID, strTitle, strArtist = IO.myAddIOFunc()
        DataProcessor.myAddProcCode(strID, strTitle, strArtist)
        continue  # start loop back at top.
    # Process display current inventory
    elif strChoice == "i":
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    elif strChoice == "d":  # process delete a CD
        IO.show_inventory(lstTbl)  # display inventory
        # Get Userinput for which CD to delete
        try:
            intIDDelInput = int(
                input("Which ID would you like to delete? ").strip())
        except ValueError as e:
            print("\n")
            print("That is not an Integer!")
            print("Build in error info: ")
            print(type(e), e, e.__doc__, sep="\n")
            continue
        DataProcessor.myDeleteDataProcFunc(intIDDelInput)
        continue  # start loop back at top.
    elif strChoice == "s":  # process save inventory to file
        # Display current inventory and ask user for confirmation to save
        IO.show_inventory(lstTbl)
        strYesNo = input("Save this inventory to file? [y/n] ").strip().lower()
        # Process choice
        if strYesNo == "y":
            FileProcessor.write_file(strFileName, lstTbl)
        else:
            input(
                "The inventory was NOT saved to file. Press [ENTER] to return to the menu.")
        continue  # start loop back at top.
    # Catch-all should not be possible, as user choice gets vetted in IO, but to be save:
    else:
        print("General Error")
