import mysql.connector
import time
import os

os.system("")


class style():
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'


fileName = input("Enter file name (with the file extension) : ")

Lines = open(fileName, 'r').readlines()

print("Found {} users in the file".format(len(Lines)))

valid = input("Do you want to continue? (y/n) : ")
if valid != "y" and valid != "Y":
    print("Exiting...")
    exit()

print("Please enter the database credentials. ")
host = input("Enter the host : ")
user = input("Enter the user : ")
password = input("Enter the password : ")

mydb = None

try:
    mydb = mysql.connector.connect(
        host=host,
        user=user,
        password=password
    )
except Exception as e:
    print(style.RED + style.UNDERLINE + "Error while trying to connect to database. Exiting..")
    print(style.RESET + "Error : {}".format(e))
    exit()


def action():
    print("1. Create users / Recreate missing users")
    print("2. Delete users")
    print("3. Exit")
    act = int(input("What do you want to do? : "))

    if act == 1:
        createUsers()
    elif act == 2:
        deleteUsers()
    else:
        exit()


def createUsers():
    start = time.time()
    print("Creating users...")
    cursor = mydb.cursor()
    for line in Lines:
        user = line.strip()
        print("Creating user : {}".format(user))
        cursor.execute("CREATE USER IF NOT EXISTS {}".format(user, user))
        cursor.execute("GRANT USAGE ON *.* TO {}@'%' REQUIRE NONE WITH MAX_QUERIES_PER_HOUR 0 "
                       "MAX_CONNECTIONS_PER_HOUR 0 MAX_UPDATES_PER_HOUR 0 MAX_USER_CONNECTIONS 0".format(user))
        cursor.execute("GRANT ALL PRIVILEGES ON {}.* TO {}@'%'".format(user, user))
        cursor.execute("CREATE DATABASE IF NOT EXISTS {}".format(user))
        cursor.execute("GRANT ALL PRIVILEGES ON {}.* TO {}@'%'".format(user, user))
    print("Done creating users. Took {} ms".format(time.time() - start))
    action()


def deleteUsers():
    start = time.time()
    print("Deleting users...")
    for line in Lines:
        user = line.strip()
        print("Droping user : {}".format(user))
        cursor = mydb.cursor()
        cursor.execute("DROP DATABASE IF EXISTS {}".format(user))
        cursor.execute("DROP USER IF EXISTS {}".format(user))
    print("Done deleting users. Took {} ms".format(time.time() - start))
    action()


action()
