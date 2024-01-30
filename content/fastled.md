Title: Pixels part 3: FastLED
Description: Third in the series, this post discusses using the FastLED library for controlling RGB LEDs, aka pixels.
Date: 2024-01-30
Category: Making
Tags: leds, electronics
Status: draft

In the first post in this series, I introduced RGB pixels, discussed the various types, and compared analog and true RGB pixels. In the second part, I covered wiring and shared my tips for reliably connecting to your microcontroller. In this third part, I will discuss the FastLED library, one of the most popular libraries for programming pixels.

## FastLED

<a href="http://fastled.io/" target="_blank">FastLED</a> is a hugely popular library for programming all sorts of RGB pixels. The intro on that linked page summarizes the library nicely: fast, easy to use, widely used, and under active development. See the <a href="https://github.com/FastLED/FastLED" target="_blank">GitHub page</a> for code and an excellent wiki. Get help in the <a href="https://www.reddit.com/r/FastLED/" target="_blank">FastLED Reddit sub</a>.

Let's start with the basics. For this, I think it will help to see code. The comments inline explain what's going on.

    #!c
    #include "FastLED.h"           // include the FastLED library
    #define LED_TYPE      WS2812B  // specify which type of pixels you're using
    #define DATA_PIN      5        // which GPIO pin is outputting the data signal
    #define NUM_LEDS      32       // how many LEDs in your setup
    #define COLOR_ORDER   RGB      // the order of red-green-blue values in the data
    #define BRIGHTNESS    128      // from 0 - 255

    CRGB leds[NUM_LEDS];           // create an array to hold LED values

    uint8_t startIndex;            // a couple of variables for tracking info
    uint8_t colorIndex;

    void setup() {
        delay(1500);
        // Set up our LED configuration, specifying the type, data pin, and color order
        // Then we pass in the array of values and the number of LEDs. Finally, and this
        // is optional, we apply a color correction to help account for color variations
        // across LED strips.
        FastLED.addLeds<LED_TYPE, DATA_PIN, COLOR_ORDER>(leds, NUM_LEDS).setCorrection(TypicalLEDStrip);
        // Next we set the brightness level
        FastLED.setBrightness(BRIGHTNESS);
    }

    void loop() {
        colorIndex = startIndex;   // this is a counter value, we're setting a start point
        for( int i = 0; i < NUM_LEDS; i++) {
            // for each LED in the array, set its color to a value picked from the
            // predefined (by FastLED) palette of colors -- in this case a rainbow
            // The `colorIndex` specifies which color to grab from the palette.
            // The function also expects a brightness value, and a way to blend
            // colors from one pixel to the next.
            leds[i] = ColorFromPalette( RainbowColors_p, colorIndex, BRIGHTNESS, LINEARBLEND);
            colorIndex = colorIndex + 10;  // increment our index
        }

        // You have to call show() to actually write the values to the physical LEDs and
        // light them up
        FastLED.show();
        // For delays, best to use the FastLED-provided functions instead of built-ins
        FastLED.delay(10);
        // Finally, increment our counter so that the next time through the loop, the
        // colors will be assigned one LED ahead of where they were this time.
        startIndex = startIndex + 1;
    }

Phew, that was a lot. I hope you read through the comments and they were helpful. I'll expand on a few points. Starting from the top, the `LED_TYPE` is a constant representing the type of pixels you're using. FastLED supports many, though not all types. The supported pixels are <a href="https://github.com/FastLED/FastLED/blob/9307a2926e66dd2d4707315057d1de7f2bb3ed0b/keywords.txt#L360" target="_blank">listed here</a>.

Next is the `COLOR_ORDER`. This varies by pixel type. Some expect the data to have the red color bits first, followed by green, then blue. But others will be in BGR or GRB or <a href="https://github.com/FastLED/FastLED/blob/9307a2926e66dd2d4707315057d1de7f2bb3ed0b/keywords.txt#L408" target="_blank">whatever order</a>. I'm sure there's a better way, but when I don't know, I'll set all the LEDs to be red. If they show up blue or green, I know to start with a different order. Repeat for green and blue till you get the order correct.

Next I'll jump down to the `FastLED.addLeds` call. There are two primary versions of this function: one for 3-wire pixels and the other for 4-wire pixels. Shown above is the 3-wire variant, where there is no dedicated clock line. If you're using 4-wire pixels, the function you'll call is `FastLED.addLeds<LED_TYPE, DATA_PIN, CLOCK_PIN, COLOR_ORDER>(leds, NUM_LEDS)`.

## Colors and palettes

In the example above, I demonstrated using one of <a href="https://github.com/FastLED/FastLED/blob/9307a2926e66dd2d4707315057d1de7f2bb3ed0b/keywords.txt#L461" target="_blank">the pre-defined palettes of color</a>. These define a set of colors that you can apply across the array of LEDs to get a pleasing mix of colors, such as a rainbow or set of ocean (blue-green) tones. That might be considered a bit more advanced than setting a specific color.

FastLED gives you many ways to specify a color for an LED. You can do so using one of <a href="https://github.com/FastLED/FastLED/blob/9307a2926e66dd2d4707315057d1de7f2bb3ed0b/keywords.txt#L201" target="_blank">the pre-defined named colors</a>, by RGB value, HSV value, and more. For example, to set an LED to display 100% red, you could use any of the following:

    :::c
    leds[i] = CRGB::Red;
    leds[i] = 0xFF0000;
    leds[i] = CRGB(255, 0, 0);
    leds[i].setRGB(255, 0, 0);
    leds[i] = CHSV(HUE_RED, 255, 255);  // HUE_RED happens to be 0 on the color wheel
    leds[i].setHSV(HUE_RED, 255, 255);
    // or
    leds[i].red   = 255;
    leds[i].green = 0;
    leds[i].blue  = 0;
    // ... and probably more!

There's one more trick up the sleeve ... let's say you wanted to set all of the LEDs to red. You could loop through, set the color using one of the above techniques, then call `FastLED.show()`. Or, you could call `FastLED.setColor(CRGB::Red)` (or specify a hex value, HSV value, etc.). With `setColor()` you _do not_ call `.show()`!

## Fading out

I'll end with two techniques for fading to black. In both cases, you would put the call to the function inside the `loop()` function so that it's called with each iteration of the program loop.

    #!c
    // Technique 1: brute force
    #define BRIGHTNESS    255

    // Assumes there's something that sets all the LEDs to some color, like:
    FastLED.setColor(CRGB::Red);

    void fade_to_black() {
        // put the call to this function inside loop()
        static int brightness = BRIGHTNESS;
        static int fadeAmount = 2;
        if (brightness <= 0) {
            return;
        }
        brightness -= fadeAmount;
        FastLED.setBrightness(brightness);
    }

Or:

    #!c
    // Technique 2: use one of the built-ins

    void fade_to_black() {
        for (int i = 0; i < NUM_LEDS; i++) {
            // Dim a color by 25% (64/256ths)
            // eventually fading to full black
            leds[i].fadeToBlackBy( 64 );

            // Or, reduce color to 75% (192/256ths) of its previous value
            // eventually fading to full black
            // leds[i].nscale8( 192);
        }
        FastLED.show();
    }

There's a ton more to explore in the FastLED library. There's support for matrices, controlling multiple strips (even of different types), built-in fast math functions for varying pixels by sine waves and such, and so much more. I hope this gets you off to a good start. Happy exploring.
