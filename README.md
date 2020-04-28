# JARVIS
A cool simple personal assistant that can do many things to make your life easier a little bit


## Discription
this is simple personal assistant named after everyones favourite jarvis assistant in the MCU

this as of now can perform the following actions :

1. Get you the weather details
2. backUp your computer or certain folder on a single command


scroll down to Usage section to see the examples and commands of performing the above tasks

As of now this project is under development but the goal list of feature is given at the end


## Installation
Download the executable from the releases section of [Github](https://github.com/harshnative/JARVIS/releases)


## Usage

#### Weather - 
```
weather city-cityName
```
You will get the weather details of cityName  

Weather information is provided by open weather , all information is available in SI units  


```
weather city-cityName -f
```
You will get the temperature in faraniet also  


```
weather
```
If no city name is passed - Jarvis will use the default city saved in settings.txt


#### BackUp
```
backup -d 
```
To backup all the directories only , directories are taken from settings.txt


```
backup -a
```
To backup all the data of all the users


```
backup -a -c
```
To backup all the data the current user


```
backup -a -e
```
To backup all the essential data of all the users
 
Essential data is data inside desktop, download, videos, music, pictures folders only

```
backup -e -c 
```
To backup all the essential data of current user only


```
backup -a -d
```
-d command can be clubbed with any other command to perform actions at once

#### Restore
```
restore
```
To restore the default settings if you have messed around with them

#### Settings
```
change settings
```
command to open the settings file for editing the main program settings

###### Default settings page looks like [this](https://github.com/harshnative/JARVIS/blob/master/settings.txt) 


#### Help
```
help
```
To open the help in the console window itself

```
help open
```
To open the help in the TEXT file format

```
help weather
```
To open the help for the weather only

#### Update
```
update
```
To update the settings in the program 

This is automatically called when the program restarts 