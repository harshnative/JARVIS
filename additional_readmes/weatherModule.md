# Weather Module Jarvis - 

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
weather city-new_york 
```
For the city having names in more than one word use underscore instead of space

&nbsp;
```
weather
```
If no city name is passed - Jarvis will use the default city saved in settings.txt


## FAQ - 

####  I want to get whether of new york and I am using following command but program crashes after i run this command ? 

``` weather city-new york```

You have to use _ (underscore) instead of space for city having more than one word in name

``` weather city-new_york```


#### Program says error while getting wheather details after I run this command ?

``` weather city-cityNameHere ```

Open weather probably does not provide weather details of your city. Although more than 2,50,000 city are supported , still their can be some city for which the weather details may not be found. Also make sure you are entering right set of commands

