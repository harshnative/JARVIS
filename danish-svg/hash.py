#Install stdiomast first :
#On terminal - sudo pip3 install stdiomask
#On cmd - pip install stdiomask
import stdiomask
def hash():
    password = stdiomask.getpass("Password :")
    return password
