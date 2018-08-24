Title: Multiple cameras with a single Raspberry Pi
Date: 
Category: 
Tags: 
Status: draft

The Arducam Multi Camera Adapter board is a neat accessory for a Raspberry Pi. With it, you can connect multiple cameras to a single Pi. A single board supports up to four cameras. According to Arducam, you can stack up to four boards for a total of 16 cameras on a single Pi. 

I had a chance to use a couple of these boards in a recent project. Our goal was to capture multiple images to form an image mosaic. My setup included a Raspberry Pi 3B+, two of the Arducam multicamera boards, and six cameras. (Only the 5MP v1 Pi cameras, or Arducam's 5MP camera are supported, not the 8MP v2 camera.)

Since Arducam's documentation is sparse, I thought I'd share my experiences with this adapter as well as a Python library I wrote that simplifies accessing each of the cameras.

First, you should know that you cannot capture the images simultaneously. The adapter works by enabling one camera at a time. So, you can take photos one after the other, but there will be a small delay between each. Currently, our code pauses for 0.1 second between photos though we could probably wait less time than that.

## Hardware setup

Let's start with the hardware side. The adapter board will use 26 of the GPIO pins of the Pi, leaving you the last 14 pins free for other purposes. You will connect the Pi's camera port (called the CSI port) to the adapter board with a ribbon cable. Then, you'll connect the CSI cable from each of your cameras to the ports on the adapter. Those cables attach blue tab side out (or think of it as conductors towards the board). 

How about stacking multiple boards? You'll need to solder on the 10-pin connector that Arducam supplies to each of the adapters. These are the high-speed MSI bus over which the camera data is transferred between boards. Because of this connector, the bottom adapter didn't sit straight on my Pi3B+ since the connector hits the HDMI connector. I'm not sure if this contributed to the issues I had.

You'll need to set DIP switches on the boards to identify which of the OE (output enable) pins that board will use. For board 1, switches 1 and 5 must be on and the rest off. For board 2, switches 2 and 6 are on. See the <a href="http://www.arducam.com/multi-camera-adapter-module-raspberry-pi/" target="_blank">Arducam site</a> for the full list. Pictures on the Amazon listing for the adapter shows the CSI cable going between the bottom board to the Pi. In their emails to me, Arducam suggested connecting the ribbon cable to the top-most board. (It made no difference for me where it was connected.)

Each adapter board has two channels, with two camera ports each. You select which camera to use by enabling one of the channels and one of the cameras. Arducam calls these the channel select (CS) and output enable (OE). All of the stacked boards share the same CS pin but have their own OE pins (hence the DIP switches you must set). There's a listing of which pins you must set on the <a href="http://www.arducam.com/multi-camera-adapter-module-raspberry-pi/" target="_blank">Arducam site</a>, though my library hides that complexity.

## Software



With that hardware setup out of the way, with multiple boards you should in theory be able to take pictures from up to 16 cameras by setting the correct GPIO pins high or low. My library does support up to 16 cameras. Perhaps you'll have better luck stacking boards than I did.


First, I couldn't get it to work. Even after multiple emails back and forth with Arducam, connecting a second adapter would cause my Pi to crash as soon as I tried accessing any camera. In theory, this is how it's supposed to work.


Syntax highlighting with & without line numbers

    :::python
    print("The triple-colon syntax will *not* show line numbers.")

To display line numbers, use a path-less shebang instead of colons:

    #!python
    print("The path-less shebang syntax *will* show line numbers.")

    #!javascript
    sample code block

Include font-awesome symbols like this
<i class="fa fa-heart red"></i>