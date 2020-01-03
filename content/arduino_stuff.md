Title: Arduino something-er-other
Date: September 23, 2019
Category: Arduino
Tags: arduino
Status: draft


## The `loop()` function

When I first got started with the Arduino, I thought the program loop was special somehow. Somewhere I came up with the notion that `loop()` ran at some fixed interval. I worried that I had to keep the code within the loop short, or the loop would move to the next iteration before my code was done. As a result, I struggled to understand how I'd organize my code as my programs grew.

While it seems like a special function, under the covers of the Arduino's magic, all that's happening is:

    :::c
    while(true) {
        loop();
    }

In other words, `loop()` will take as long to execute as whatever you put into it. 


## Using Visual Studio Code for Arduino development

plugins, config you need to do (some of it every time)

https://medium.com/home-wireless/use-visual-studio-code-for-arduino-2d0cf4c1760b

## Multiple files in a sketch

https://arduino.stackexchange.com/a/61636

Need to figure out the conflicting advice of using a src subfolder even though it doesn't work using the Arduino IDE.

## Good stuff over at

https://hackaday.io/project/8238-embedding-c