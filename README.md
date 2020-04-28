# JARVIS
A cool simple personal assistant that can do many things to make your life easier a little bit


## Discription
this is simple personal assistant named after everyones favourite jarvis assistant in the MCU 

this as of now can perform the following actions :

1. Get you the weather details
2. backUp your computer or certain folder on a single command

scroll down to Usage section to see the examples and commands of performing the above tasks

As of now this project is under development but the goal list is feature is given at the end


## Installation
Download the executable from the realeses section of github


## Usage

#### Weather - 
```console
weather city-cityName
```
You will get the weather details of cityName

Weather information is provided by open weather , all information is available in SI units

```console
weather city-cityName -f
```
You will get the temperature in faraniet also

```console
weather
```
Jarvis will use the default city saved in settings.txt


#### BackUp
```console
backup -d 
```
To backup all the directories only , directories are taken from settings.txt

```console
backup -a
```
To backup all the data of all the users

```console
backup -a -c
```
To backup all the data the current user

```console
backup -e -c
```
To backup all the essential data of current user 
Essential data is data inside desktop, download, videos, music , pictures only

