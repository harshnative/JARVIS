# JARVIS
A cool simple personal assistant that can do many things to make your life easier a little bit built in house using python


## Discription -
this is simple personal assistant named after everyones favourite jarvis assistant in the MCU

this as of now can perform the following actions :

1. Get you the weather details
2. backUp your computer or certain folder on a single command


scroll down to Usage section to see the examples and commands of performing the above tasks

As of now this project is under development but the goal list of feature is given at the end


## Installation -
Download the executable from the releases section of [Github](https://github.com/harshnative/JARVIS/releases)


## Usage -

#### Weather - 
```
weather city-cityName
```
You will get the weather details of cityName  

Weather information is provided by open weather , all information is available in SI units  

&nbsp;
```
weather city-cityName -f
```
You will get the temperature in faraniet also  

&nbsp;
```
weather
```
If no city name is passed - Jarvis will use the default city saved in settings.txt

&nbsp;
#### BackUp
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

&nbsp;
#### Restore
```
restore
```
To restore the default settings if you have messed around with them

&nbsp;
#### Settings
```
change settings
```
command to open the settings file for editing the main program settings

###### Default settings page looks like [this](https://github.com/harshnative/JARVIS/blob/master/settings.txt) 

&nbsp;
#### Help
```
help
```
To open the help in the console window itself

&nbsp;
```
help open
```
To open the help in the TEXT file format

&nbsp;
```
help weather
```
To open the help for the weather only

&nbsp;
#### Update
```
update
```
To update the settings in the program 

This is automatically called when the program restarts 

&nbsp;
## Support 
comming soon.....

&nbsp;
## Contribution
Your every contribution is appreciated , if you want to contribute to the project please contact at Harshnative@gmail.com

&nbsp;
## Authors & Acknowledgement
We thank every person who have commited anything to the open source world, those small contibutions combined together run this beautiful tech world

we cannot even imagine the world without the open source things

&nbsp;
## License
This code is licensed under GPL 3.0 terms 
read more about it [here](https://github.com/harshnative/JARVIS/blob/master/LICENSE)

&nbsp;
## Project status
This project is currently under development 

#### Features available write now -
1. weather
2. backup

#### Features comming soon -
1. internet searching 
2. in built notepad and sticky notes 
3. play short iron man instrumental music 
4. play any music from youtube 
5. launch programmer on system 
6. tell time and date by voice  
7. gives a brief system status 
8. password storer 
9. to do list 
10. remainder creator - google calender integration 
11. shortcut commands to open certain apps or directories 
12. accessible from anywhere - like pip is directly accessible from anyWhere  