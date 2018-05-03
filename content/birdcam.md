Title: Streaming birdcam with a Raspberry Pi and picamera
Date: April 29, 2018
Category: Making
Tags: raspberry pi, making, python
Slug: pi-birdcam
Status: draft

My darling wife got me a Raspberry Pi 3B+ and a NOIR Pi camera for my birthday so that I could set up a streaming camera to monitor our nesting bluebirds. Here's how I did it.

My first attempt was to use the Motion program as <a href="https://hackernoon.com/spy-your-pet-with-a-raspberry-pi-camera-server-e71bb74f79ea" target="_blank">described by Hackernoon</a>. It worked, but the resulting video stream was very slow and jerky. I'd say I was getting only a few frames a second at best. I knew I could do better.

## Picamera

The better solution turned out to be <a href="https://picamera.readthedocs.io" target="_blank">picamera</a>. This is a Python module for using the Raspberry Pi camera. The author has not only written a fantastic library, but he's also provided lots of great recipes (sample scripts) showing how to use it.

His <a href="https://github.com/waveform80/pistreaming/" target="_blank"> pistreaming </a> recipe looked to be perfect for my needs. Raspbian Stretch (at least the Desktop flavor) comes with Python installed. So I jumped right into the pistreamer install steps described on the <a href="https://github.com/waveform80/pistreaming/" target="_blank"> pistreaming GitHub site</a>.

The setup was quite simple and with the script running, I could go to localhost:8082 and see the stream live. It was much faster than Motion. I just needed to get this streaming across the web and I would be good to go.

## Houston, we have a problem

I hit a little snag at this point. While I could access the stream just fine from the Pi itself, I could not do so from another computer on my local network. I found that I could access the pistreamer page if I connected the Pi to my network over Ethernet. So, something was up (or down) with my wifi connection.

After lots of struggling, thinking that maybe there was a firewall or iptables rule blocking access, I found my wifi router was blocking the traffic. I had to go into my router's admin screens and enable Wireless Multicast Routing. With that done, I could access the stream from my laptop.

## Streaming to the internet

Streaming to the internet would involve a couple of changes. First, I had to use the Port Forwarding screens in my router's admin tool to let traffic to those ports go through.

![port forwarding in Tomato](../images/2018/portforwarding.png)

Then, according to a closed issue on the pistreaming repo, I needed to modify the script's index.html file. 


Modify index.html to stream over the internet:

    #!javascript
    // change the var client line (at the bottom) to be:
    var client = new WebSocket('ws://your_external_ip_address:${WS_PORT}/');

Make sure you have the quotes right on that. There are few in there to start and you end up with two single quotes around everything between the parentheses.


## Streaming on startup

Modify server.py for starting on boot:

    #!python
    class StreamingHttpServer(HTTPServer):
        def __init(self):
            # add this line
            cwd = os.path.dirname(os.path.realpath(__file__))
            super(StreamingHttpServer, self).__init__(
                  ('', HTTP_PORT), StreamingHttpHandler)
            # modify this next line
            with io.open(os.path.join(cwd, 'index.html'), 'r') as f:
                self.index_template = f.read()
            # this one too
            with io.open(os.path.join(cwd, 'jsmpg.js'), 'r') as f:
                self.jsmpg_content = f.read()

Then, update /etc/rc.local:

```
which python3  # record this somewhere
sudo nano /etc/rc.local

# before the `exit 0` line, add:
(sleep 10 && /path/to/python3 /home/pi/pistreaming/server.py) &

```

## Focusing the camera

![Focusing the Pi cam](../images/2018/focusing_pi_camera.jpg)



Include font-awesome symbols like this
<i class="fa fa-heart red"></i>