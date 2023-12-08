Title: Pixels part 2: the hardware
Description: Second in the series, this post discusses wiring RGB pixels to a microcontroller and shares an example sketch for making the LEDs show a rainbow pattern.
Date: December 7, 2023
Category: Making
Tags: leds, electronics

In the first post in this series, I introduced RGB pixels. I discussed the various types and compared analog and true RGB pixels. I also covered power requirements. In this post, I'll cover wiring and share my tips for reliably connecting to your microcontroller. I also include a basic sketch for displaying some colorful blinkies.

## Microcontrollers

I personally prefer to use ESP32 or ESP8266 microcontrollers. They're small, cheap, and readily available from Amazon or Aliexpress. They even feature built-in wifi and Bluetooth connectivity. But any Arduino-compatible microcontroller will work.

I recommend powering your pixels directly. Don't pull power from a 5v pin on the microcontroller. As discussed in the previous post, pixels draw a lot of power so you could easily burn out your microcontroller by drawing too much power through it.

Another consideration is powering the microcontroller itself. You could power it through its USB port. Most microcontrollers do just fine running off any old 5v power brick you have laying around. But, wiring that way means you'll essentially need two power sources: one for the microcontroller and another for the pixels. So, instead of powering over USB, you can supply power and ground directly to the Vin and Gnd pins on your microcontroller.

<a href="../images/2023/pixel_schematic.png" title="click for larger size"><img src="../images/2023/pixel_schematic.png" width="480" title="Wiring schematic for an ESP32 dev board and 3-wire pixel strip"/></a>

Finally, there's wiring up the data (signal) line. Wiring 3-wire or 4-wire pixels is essentially identical. With 3-wire pixels, you'll run a wire from a digital output pin to the Di (data in) pad on the pixel. For 4-wire pixels, you'll also need to run another wire to the Clk (clock) pad.

Consult the pinout documentation for your specific microcontroller. You want to choose pins that are not pulled high or low during boot (i.e. "strapped" pins). If you do, you might have odd difficulties like not being able to flash your microcontroller or having it not boot. Also, don't choose the pin whose GPIO port corresponds to an on-board LED. If you do, you may experience some flashing during boot or other odd lighting behavior as general operations light up the on-board LED.

In the diagram above, I illustrate connecting pin D1 to the data line. This pin on the ESP32s I use corresponds to GPIO pin 5 which is an unused GPIO port on that particular board. Again, consult the documentation for your microcontroller.

## Soldering the strip

I have never found quick-connectors to work reliably with pixel strips. For that reason, I always solder connections to the pads. Here's a tip: tin the pads first, then solder on the wires. By "tinning" I mean put solder on the pad. Clean the pads or dab a small amount of liquid flux on the pad. Heat it carefully, quickly, though you don't need to rush. Add a small bead of solder once the pad is hot.

Next, tin the wire. Again, flux it, heat it, tin it. Once that's done, you can more easily connect the two. Heat the pad and when the solder melts, bring the wire to the pad. Its solder will melt quickly, fusing the wire to the pad.

<a href="../images/2023/tinned_pixels.jpeg" title="click for larger size"><img src="../images/2023/tinned_pixels.jpeg" width="480" title="Solder bead on pixel strip, ready to have the wire soldered to it"/></a>

There's no easy way to recover if you destroy a pad, say by over-heating or scraping off the thin copper coating. In those cases, you'll need to cut off that pixel and work with a slightly shorter strip.

If your microcontroller has header pins soldered to it already, I recommend you use jumper wires with Dupont connectors. Connect the female end to the microcontroller and cut off the other end and solder that to the pixel strip. Soldering to a header pin is tough, plus once you do you'll never be able to insert the pins into a breadboard or socket. You can super-glue the connector to the board. If you ever need to remove it, you can dissolve the glue with acetone. If your microcontroller has through-board holes or pads, you can solder the other end of the wire directly to your microcontroller.

I went so far as to create a <a href="https://www.timpoulsen.com/2020/my-first-custom-pcb#my-first-custom-pcb" title="Earlier post on creating my custom carrier board">custom PCB carrier board</a>. I can solder the ESP8266/ESP32 and a few components to the board then have easy screw-connect headers to make connecting the wires easy and reliable.

<a href="../images/2020/custom_pcb_assembled.jpg" title="click for larger size"><img src="../images/2020/custom_pcb_assembled.jpg" width="480" title="My custom carrier board, assembled"/></a>

As you see on my board, I typically wire in a capacitor (500–1000 µF at 6.3V or higher) across the + and – terminals. <a href="https://learn.adafruit.com/adafruit-neopixel-uberguide/best-practices" target="_blank">Adafruit also recommends</a> a small resistor, 300-500 Ohms, between the output pin and the LED strip. My board above shows that resister. However, in general I don't include such a resistor. I have not found it necessary and sometimes my strips don't light if I include one. Your mileage may vary.

## Simple blinky script

Now that you have your LED strip connected to your microcontroller, you need to flash some code to get the lights blinking. A very popular library for working with pixels is <a href="https://github.com/FastLED/FastLED" target="_blank">FastLED</a>. It contains all the core functionality you need plus many helpful functions and constants. In a future article, I will dive more deeply into FastLED. Here we'll go with a simple example from the <a href=" In a future article, I will dive more deeply into FastLED." target="_blank">FastLED_examples repo</a>.

Below is a simple example of a FastLED script that will show a moving rainbow palette of colors. This script is for the 3-wire WS2812B type pixels, with the data line connected to GPIO 5. In essence, each time through the loop, the script assigns a color to each LED in the strip from a rainbow palette. After showing the colors, it delays 10 milliseconds, advances the starting point in the palette for the colors, and repeats.

    #!python
    //***************************************************************
    // Basic palette example using one of FastLED's palettes.
    // From https://github.com/marmilicious/FastLED_examples
    // Marc Miller,  March 2019
    //***************************************************************

    #include "FastLED.h"
    #define LED_TYPE      WS2812B
    #define DATA_PIN      5
    #define NUM_LEDS      32
    #define COLOR_ORDER   RGB
    #define BRIGHTNESS    128

    CRGB leds[NUM_LEDS];

    uint8_t startIndex;
    uint8_t colorIndex;

    void setup() {
        delay(1500);
        FastLED.addLeds<LED_TYPE, DATA_PIN, COLOR_ORDER>(leds, NUM_LEDS).setCorrection(TypicalLEDStrip);
        FastLED.setBrightness(BRIGHTNESS);
    }

    void loop() {
        colorIndex = startIndex;
        for( int i = 0; i < NUM_LEDS; i++) {
            leds[i] = ColorFromPalette( RainbowColors_p, colorIndex, 255, LINEARBLEND);
            colorIndex = colorIndex + 10;
        }

        FastLED.show();
        FastLED.delay(10);
        startIndex = startIndex + 1;
    }

That should get your lights blinking!
