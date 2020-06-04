# BackUp Utility In Jarvis - 

```
backup -d 
```
To backup all the directories only , directories are taken from settings.txt

&nbsp;
```
backup -a
```
To backup all the data of all the users

&nbsp;
```
backup -a -c
```
To backup all the data the current user

&nbsp;
```
backup -a -e
```
To backup all the essential data of all the users
 
Essential data is data inside desktop, download, videos, music, pictures folders only

&nbsp;
```
backup -e -c 
```
To backup all the essential data of current user only

&nbsp;
```
backup -a -d
```
-d command can be clubbed with any other command to perform actions at once

## FAQ - 

#### Jarvis is not backuping up some of my files ?

Unsupported files like encryted container and file that are not accessible due to OS permission issue are not backed up

#### Jarvis is not backing up my directories mentioned in the settings file ?

Make sure you write correct path.

For example if you want to backup a folder on the desktop then path will be something like this 

```C:/Users/userName/Desktop/folderName```

If you have mulitple directories then make sure to separate them out using colon ( , ) 

```C:/Users/userName/Desktop/folderName1 , C:/Users/userName/Desktop/folderName1```

#### How does the jarvis backup work ?
Jarvis copy all the files in the directory and all the subdirectories to the backUp path , if the files are already in the backup then the files will be replaced by the new files

#### Jarvis Backup is not working ?
Make sure that the path to backup in the settings is set and is correct , look at this example for the backup path in D drive

```D:/myFiles```

A folder will be created in the myfiles called backup in which your backed up data will be present

#### where is my directory backup in the backup folder ?
Your directories backup will be located under the additional files folder in the backup folder

#### Jarvis seems to be stuck while BackingUP Data ?
Copying files takes time and depends on the computer processing power and transfer speed btw drives, jarvis may be still running, you can conform that by opening task manager
