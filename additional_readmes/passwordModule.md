# Password Manager

```password```
Enter this command in jarvis window to open the Manager

If the password module started correctly then for the first you have to set a master password, This will be used to encrypt you passwords while they are stored as storing your passwords unencrypted is not a good idea

If you are visiting after first time, then you will need to enter your master password so that jarvis can again decrpyt and show your password


##### Are my Passwords safe ?
We use one time pad cipher encryption technology to encrypt the passwords in the Storage, anyone will need to have your master password to decrpyt it.

This is quite strong encryption tech, but still things can be cracked down by using brute force attach by a very powerfull computer, so we do not recommend storing extremely sensitive information into this.


## Commands to use in this module

#### Adding Password

```-a```
This is used to Add New Password to the Storage.

Now just follow on screen instruction to add

#### Updating Password

```-u```
This is used to Update the already existing Password in the Storage

Now just follow the on screen insruction to update

#### Deleting Password

```-d```
This is used to Delete the passwords in the Storage

Now just follow the on Screen instruction to delete

#### Seeing All Passwords

```-sa```
This is used to see all the passwords in the storage

#### Seeing particular website password

```-s```
This is used to see all the password associated with a particular website

Now just follow the on Screen instruction to see

#### Change Password

```-c```
This is used to change the master password


## FAQ - 

##### Password input is not taking input ? 
It is recording input but you are not seeing it as it is the security feature in jarvis while entering passwords to avoid password inputs leakage. If you missedTyped few things just press backSpace for 1 to 2 sec and start entering the password again :)

##### I am not able to delete or update any thing ?
Make sure you enter correct index number when asked to them

##### I have forgotten my master password ?
We are extremely sorry but you now cannot decrypt your passwords again, they are lost 