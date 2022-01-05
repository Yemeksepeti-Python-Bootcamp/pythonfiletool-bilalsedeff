# Name: Bilal Sedef
# Topic: pythonfiletoollib homework / CSV Manipulator
# Program: Yemeksepeti-Python-Bootcamp
# This code can be improved much more. It has unnecessary repeating parts in it. Nonetheless, it does the job :)

import json
import csv
import os
import numpy as np

dict1 = {}


class FileTool:
    temp_dict = dict()
    temp_list = list()
    list_of_column_names = []

    def __init__(self, path, fields=""):
        self.fields = fields
        self.path = path

        try:
            with open(path, "r+", newline='') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')
                # If the initial code has "fields" parameter written within, this code chunk will
                # automatically attach the "fields" to the both existing or non-existing csv file first row
                if self.fields != "":
                    with open(f"new_{path}", "w+", newline='') as writeFile:
                        csvwriter = csv.writer(writeFile)
                        csv_file.seek(0)
                        first_row = next(csv_reader)
                        first_row = next(csv_reader)
                        self.list_of_column_names = list(self.fields)
                        # The code checks if written "fields" parameter number is matching with the existing data column number
                        # If it is less or more than the existing column numbers, different approaches will be executed
                        if len(self.fields) < len(first_row):
                            print(
                                "The number of fields given is less than the data columns, the missing field names are numbered")
                            for i in range(len(first_row) - len(self.fields)):
                                self.list_of_column_names.append(i)
                                self.fields = self.list_of_column_names
                        elif len(self.fields) > len(first_row):
                            print("The number of fields given is more than the data columns, redundancies are removed")
                            for i in range(len(self.fields) - len(first_row)):
                                self.list_of_column_names.pop()
                                self.fields = self.list_of_column_names
                        csvwriter.writerow(self.fields)
                        csvwriter.writerow(first_row)
                        for row in csv_reader:
                            csvwriter.writerow(row)
                        writeFile.close()
                        csv_file.close()
                        os.remove(path)
                        # The old(original) .csv file will be deleted and the new .csv file will be renamed
                        # as the original file
                        os.rename(rf"new_{path}", rf"{path}")

                elif self.fields == "":
                    # The code checks if the object file has headers. Different approaches will be applied to both existing
                    # and non-existing header names situations
                    csv_file.seek(0)
                    sniffer = csv.Sniffer()
                    has_header = sniffer.has_header(csv_file.read(2048))
                    csv_file.seek(0)
                    if has_header:
                        csv_reader = csv.reader(csv_file)
                        header = next(csv_reader)
                        self.list_of_column_names = list(header)
                    else:
                        with open(f"new_{path}", "w+", newline='') as writeFile:
                            csvwriter = csv.writer(writeFile)
                            csv_file.seek(0)
                            first_row = next(csv_reader)
                            # If the data does not have a header, it will be automatically titled with
                            # consecutive numbers as many as the data column.
                            header = [i for i, _ in enumerate(first_row)]
                            self.list_of_column_names = header
                            csvwriter.writerow(header)
                            csvwriter.writerow(first_row)
                            for row in csv_reader:
                                csvwriter.writerow(row)
                            writeFile.close()
                            csv_file.close()
                            os.remove(path)
                            os.rename(rf"new_{path}", rf"{path}")

        # The code handles the FileNotFoundError smoothly. It will create the given file if it does not exist.
        except FileNotFoundError:
            filename, file_extension = os.path.splitext(path)
            if file_extension == ".csv":
                print(
                    f"Due to there is no such csv file in described path, {filename}{file_extension} has been created")
                if fields != "":
                    with open(f"{filename}.csv", 'w') as csvfile:
                        # creating a csv writer object
                        csvwriter = csv.writer(csvfile)
                        csvwriter.writerow(fields)
                        self.list_of_column_names = fields
                        csvfile.close()
                elif fields == "":
                    fields = str(input("Please describe the field names of your data without coma separated: "))
                    fields = list(fields.split(" "))
                    with open(f"{filename}.csv", 'w') as csvfile:
                        # creating a csv writer object
                        csvwriter = csv.writer(csvfile)
                        csvwriter.writerow(fields)
                        self.list_of_column_names = fields
                        csvfile.close()
            elif file_extension == '.json':
                if self.fields == "":
                    print(
                        f"Due to there is no such json file in described path, {filename}{file_extension} has to be created")
                    fields = str(
                        input(
                            "No field name given. Please describe the field names of your data without coma separated: "))
                    fields = list(fields.split(" "))
                    self.list_of_column_names = fields
                    dict1["fields"] = json.dumps(fields)
                    # creating a json file
                    out_file = open(f"{filename}.json", "w")
                    json.dump(dict1, out_file, indent=4, sort_keys=False)
                    out_file.close()

                # creating a json file with given "fields" parameters
                elif self.fields != "":
                    self.list_of_column_names = self.fields
                    print(
                        f"Due to there is no such json file in described path, {filename}{file_extension} is created")
                    dict1["fields"] = json.dumps(self.fields)
                    out_file = open(f"{filename}.json", "w")
                    json.dump(dict1, out_file, indent=4, sort_keys=False)
                    out_file.close()

            else:
                print("Described file is neither csv nor json")

    # The user can add the "Temporary List" items to the main file
    def update(self):
        answer = input("Do you want want to add the temporary list to the main file? (Y/N): ")
        if answer.lower() == "y":
            with open(self.path) as csv_file:
                csv_reader = csv.reader(csv_file)
                csv_file.seek(0)
                col_n = len(next(csv_reader))
                temp_list_col_n = len(list(self.temp_list[0]))
                if col_n == temp_list_col_n:
                    csv_file.seek(0)
                    row_list = list(csv_reader)
                    for i in range(len(list(self.temp_list))):
                        row_list.append(list(self.temp_list[i]))
                    with open(f"new_{self.path}", "w+", newline='') as writeFile:
                        csvwriter = csv.writer(writeFile)
                        csv_file.seek(0)
                        for row in row_list:
                            csvwriter.writerow(row)
                        writeFile.close()
                        csv_file.close()
                        os.remove(self.path)
                        os.rename(rf"new_{self.path}", rf"{self.path}")
                        print(f"The temporary list has been added to the main file")
                else:
                    print("Temporary list column numbers and the main file column numbers are not matching.")

        self.file_menu()

    # The user can add data to either main file or temporary list.
    # He/she can do it with either by hand or using another existing data file.
    # The code will automatically detect the related parts, and it will add the data to either temporary list or to the main file.
    def adding(self, param=[]):
        if param:
            answer = input(
                f"Do you want to replace an existing row with {param} or do "
                f"you want to insert it to the rows? Please type 'R' or 'I' without quotes: ")

            # The user can either replace an existing row with the row he/she
            # sent before using other instruments of this object
            # or insert the row to the desired place.
            if answer.lower() == "r":
                answer = int(input("Please type the row number you want to replace: "))
                with open(self.path) as csv_file:
                    csv_reader = csv.reader(csv_file)
                    csv_file.seek(0)
                    row_list = list(csv_reader)
                    row_list[answer] = param
                    with open(f"new_{self.path}", "w+", newline='') as writeFile:
                        csvwriter = csv.writer(writeFile)
                        csv_file.seek(0)
                        for row in row_list:
                            csvwriter.writerow(row)
                        writeFile.close()
                        csv_file.close()
                        os.remove(self.path)
                        os.rename(rf"new_{self.path}", rf"{self.path}")
                        print(f"The row number {answer} has been replaced with {param}")
            elif answer.lower() == "i":
                answer = int(input("Please type the row number you want to insert your list: "))
                with open(self.path) as csv_file:
                    csv_reader = csv.reader(csv_file)
                    csv_file.seek(0)
                    row_list = list(csv_reader)
                    row_list.insert(answer, list(param))
                    with open(f"new_{self.path}", "w+", newline='') as writeFile:
                        csvwriter = csv.writer(writeFile)
                        csv_file.seek(0)
                        for row in row_list:
                            csvwriter.writerow(row)
                        writeFile.close()
                        csv_file.close()
                        os.remove(self.path)
                        os.rename(rf"new_{self.path}", rf"{self.path}")
                        print(f"The row {param} has been inserted to row number {answer}")

        # This part allows the user to pull data from an existing file or creating it by hand.
        else:
            answer = str(input(
                "Do you want to add data from a file, or you want to add it by hand? Please type 'F' or 'H' without quotes: "))
            if answer.lower() == "h":
                answer = str(input("Please type the data you want to use without commas: "))
                answer = answer.split()
                answer = map(int, answer)
                answer = list(answer)
                print(answer)
                purpose = str(input("If you want to add this data to the temporary list, please type 'T', "
                                    "if you want to add this data to the main file, please type 'M': "))

                # The created data will be sent to the temporary list.
                if purpose.lower() == "t":
                    self.temp_list.append(answer)
                    print(self.temp_list)
                    answer = str(input("Do you want to use the data stored in the temporary list? (Y/N): "))
                    if answer.lower() == "y":
                        self.update()
                    elif answer.lower() == "n":
                        self.file_menu()

                # The created data will be sent to the temporary list
                elif purpose.lower() == "m":
                    row_n = int(input("Please type the row number you want to insert your list: "))
                    with open(self.path) as csv_file:
                        csv_reader = csv.reader(csv_file)
                        csv_file.seek(0)
                        # The below part finds the column number of the main file and checks if the created data
                        # has the same column number with it.
                        col_n = len(next(csv_reader))
                        if col_n == len(answer):
                            row_list = list(csv_reader)
                            row_list.insert(row_n, answer)
                            with open(f"new_{self.path}", "w+", newline='') as writeFile:
                                csvwriter = csv.writer(writeFile)
                                csv_file.seek(0)
                                for row in row_list:
                                    csvwriter.writerow(row)
                                writeFile.close()
                                csv_file.close()
                                os.remove(self.path)
                                os.rename(rf"new_{self.path}", rf"{self.path}")
                                print(f"The row {answer} has been inserted to row number {row_n}")
                        else:
                            print(
                                "The length of the data you entered is not matching with the column number of the main file")
                            self.file_menu()

            # The user can address a file to pull it's data. Other file has to be in the same folder with this python file
            elif answer.lower() == "f":
                new_path = str(
                    input("Please type the name of the file (with it's extension) you want to process, without quotes. "
                          "Please make sure it is in the same folder with this python file: "))
                filename, file_extension = os.path.splitext(new_path)
                if file_extension == ".csv":
                    print(
                        f"If you want to add the rows of {filename}.csv to the temporary list, type 'T' without quotes.")
                    print(f"If you want to add the rows of {filename}.csv to the main file, type 'M' without quotes.")
                    answer = str(input("Please type your answer: "))
                    if answer.lower() == "t":
                        with open(f"{filename}.csv") as csv_file:
                            csv_reader = csv.reader(csv_file)
                            csv_file.seek(0)
                            row_list = list(csv_reader)
                            self.temp_list = row_list
                            print(self.temp_list)
                    elif answer.lower() == "m":
                        with open(f"{filename}.csv") as csv_file:
                            csv_reader = csv.reader(csv_file)
                            csv_file.seek(0)
                            column_number = len(next(csv_reader))
                        with open(self.path) as org_file:
                            org_reader = csv.reader(org_file)
                            org_file.seek(0)
                            org_column_number = len(next(org_reader))
                        if column_number == org_column_number:
                            with open(f"{filename}.csv") as csv_file:
                                # Below part tries to clean the data from redundancies as much as possible.
                                csv_reader = csv.reader(csv_file)
                                csv_file.seek(0)
                                row_list = list(csv_reader)
                                row_list = row_list[1:]
                                row_list = str(row_list)
                                row_list = row_list.strip('["],')
                                row_list = row_list.replace('"', '')
                                row_list = row_list.replace("'", '')
                                row_list = row_list.replace(',', '')
                                row_list = row_list.replace(']', '')
                                row_list = row_list.replace('[', '')
                                row_list = row_list.split()
                                row_list = map(int, row_list)
                                row_list = list(row_list)
                                with open(self.path, "r+") as org_csv_file:
                                    org_csv_reader = csv.reader(org_csv_file)
                                    org_csv_file.seek(0)
                                    org_row_list = list(org_csv_reader)
                                    print(org_row_list)
                                    org_row_list.extend(
                                        map(list, np.array_split(row_list, len(row_list) / len(org_row_list[-1]))))
                                    with open(f"new_{self.path}", "w+", newline='') as writeFile:
                                        csvwriter = csv.writer(writeFile)
                                        csv_file.seek(0)
                                        for row in org_row_list:
                                            csvwriter.writerow(row)
                                        writeFile.close()
                                        csv_file.close()
                                    org_csv_file.close()
                                    os.remove(self.path)
                                    os.rename(rf"new_{self.path}", rf"{self.path}")
                        else:
                            print("The column numbers are not matching")
                            self.file_menu()

        self.file_menu()

    # Below part allows the user to delete data either from the temporary list or from the main file
    def delete(self):
        print("If you want to delete data from the temporary list please type 'T' without quotes")
        print("If you want to delete data from the main file you are working on, please type 'M' without quotes")
        answer = input("Please type your answer: ")
        if answer.lower() == "t":
            print(self.temp_list)
            answer = int(
                input("Please type the row number you want to delete from the temporary list starting from zero: "))
            self.temp_list.pop(answer)
        elif answer.lower() == "m":
            answer = int(input("Please type the row number you want to delete from the main file starting from zero: "))
            with open(self.path) as csv_file:
                csv_reader = csv.reader(csv_file)
                csv_file.seek(0)
                row_list = list(csv_reader)
                row_list.pop(answer)
                with open(f"new_{self.path}", "w+", newline='') as writeFile:
                    csvwriter = csv.writer(writeFile)
                    csv_file.seek(0)
                    for row in row_list:
                        csvwriter.writerow(row)
                    writeFile.close()
                    csv_file.close()
                    os.remove(self.path)
                    os.rename(rf"new_{self.path}", rf"{self.path}")
                    print(f"The row number {answer} has been deleted")
        self.file_menu()

    # The user can search different parts of the main file or can check the temporary list if he/she added several data in it.
    def search(self):
        print("If you want to search 'temporary list', please type 'T' without quotes")
        print("If you want to search 'fields', please type 'F' without quotes")
        print("If you want to search 'rows', please type 'R' without quotes")
        answer = str(input("Please type your answer: "))
        if answer.lower() == "f":
            print(self.list_of_column_names)
        elif answer.lower() == "r":
            answer_n = int(input("Please type the row number you want to see (ex: 4): "))
            csv_reader = csv.reader(self.path)
            try:
                if answer_n <= len(list(csv_reader)):
                    with open(self.path) as csv_file:
                        csv_reader = csv.reader(csv_file)
                        csv_file.seek(0)
                        row_list = list(csv_reader)
                        # Throws the result in json format
                        result = json.dumps(row_list[answer_n])
                        print(result)
                    answer = input("Do you want to save this row to the temporary list? (Y/N): ")
                    if answer.lower() == "y":
                        # Again some cleaning
                        result = result.strip('["],')
                        result = result.replace('"', '')
                        result = result.replace(',', '')
                        result = str(result)
                        result = result.split()
                        result = map(int, result)
                        result = list(result)
                        self.temp_list.append(result)
                        print("The row has been saved to the temporary list: ", self.temp_list)
                        answer = input("Do you want to change this row's placement? (Y/N): ")
                        if answer.lower() == "y":
                            # Sends the parameter to the "adding" function of the object
                            self.adding(result)

            # If the given row number is more than the row number of the file, the code throws the below string.
            except IndexError:
                with open(self.path) as csv_file:
                    csv_reader = csv.reader(csv_file)
                    print(
                        f"The list index you have given is out of range. There are {len(list(csv_reader))} rows in this file")
                self.file_menu()
        elif answer.lower() == "t":
            print(self.temp_list)
            answer = str(input("Do you want to use the data stored in the temporary list? (Y/N): "))
            if answer.lower() == "y":
                self.update()
            elif answer.lower() == "n":
                self.file_menu()
        self.file_menu()

    # Exits the code
    def terminate(self):
        print("You are leaving the program now")

    # Main navigation unit of the class
    def file_menu(self):
        print("---------------- MENU ----------------")
        print("If you want to search for a data in the file, type 'S'")
        print("If you want to delete a data in the file, type 'D'")
        print("If you want to add a data to the file, type 'A'")
        print("If you want to update the data, type 'U'")
        print("If you want to exit, type 'E'")
        print("--------------------------------------")
        answer = str(input("Please type your answer: "))

        if answer.lower() == "s":
            self.search()
        elif answer.lower() == "d":
            self.delete()
        elif answer.lower() == "a":
            self.adding()
        elif answer.lower() == "u":
            self.update()
        elif answer.lower() == "e":
            self.terminate()
        else:
            print("Please type according to the defined letters above")
            self.file_menu()


deneme = FileTool("deneme.csv", ["col1", "col2", "col3", "col4", "col5"])
deneme.file_menu()
