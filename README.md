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
#### Play games
&nbsp;
###### HangMan game
This is a cool word guessing game in which a random word in thrown at you containing 4-8 letters hidden *****
&nbsp;
you have to guess a character , if the character is the word then all the spaces with those character will be visible to you , suppose you enter e then in the above world hello you will be shown *e*** , now you have to guess other words 
&nbsp;
for each  wrong guess you become a additional letter of DumbAss , once you become full DumbAss , the game is over
&nbsp;
&nbsp;
To play
```
hangman game
```

&nbsp;
#### Txt compare
This is really cool , sometimes you have two txt files that looks identical but somebody has changed somethings in one of the file , you can know what as changed , simply drag and drop files once the run command is executed , although you still will be prompted to do do this
&nbsp;
To run this
```
txt compare
```

&nbsp;
#### Convert google drives shareable link to direct downloadable link
The link that you share with others from google drive , the viewer first goes to the google drive page and the download it , but if you share link generate by this the viewer will directly download the file as soon as they click the link
&nbsp;
To run this
```
google drive
```


#### Some usefull external programms are also included :)
&nbsp;
###### Generate random stuff
Want to generate some random stuff whether it be number or strings for encryption hell knows why , well jarvis as got you covered
&nbsp;
To run this
```
generate random
```
The program will open a other program for the task :)

&nbsp;
###### Number system converter
Now convert any number from any number system to any other number system easily 
&nbsp;
To run this
```
number system convertor
```
or
```
no sys conv
```
The program will open a other program for the task :)

&nbsp;
###### Average finder
just keep inputting numbers and the program will automatically count how much you inputted and find the avearge
&nbsp;
To run this
```
average
```
or 
```
avg
```
The program will open a other program for the task :)

&nbsp;
###### Coin toss 
Stuck in a situation were you have to decide a decision by luck , luck is one hell of a thing , well now get coin toss result virtaully with absolute randomness
&nbsp;
To run this
```
coin toss
```
The program will open a other program for the task :)

&nbsp;
###### Group generator
Sometimes in colleges or schools you need to divide students into groups acc to their roll no , no just input roll no's into the program and generate groups easily
Input is very easy , just input 100-120 for inputting 100 to 120 roll no students or input each seperately
To run this
```
group generator
```
The program will open a other program for the task :)

&nbsp;
###### Interest calculator
Want to calculate interest on some thing btw diff dates , well just input details and get the most accurate result ever
To run this
```
interest calculator
```
or
```
interest calc
```
The program will open a other program for the task :)

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