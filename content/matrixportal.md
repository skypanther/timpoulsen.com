Title: Weather display on an LED matrix
Description: Using CircuitPython on a HUB75 LED matrix to display current weather conditions pulled from the Ambient Weather API.
Date: April 24, 2024
Category: Making
Tags: electronics, circuitpython, python

# Using CircuitPython on a HUB75 LED matrix

I bought a couple of surplus LED matrix panels a while back, and I finally got around to playing with them. My panels are 16x32 HUB75-compatible panels. I planned to "stack" them to create an effective 32x32 matrix. Adafruit makes a neat little ESP32-based microcontroller, the MatrixPortal that features HUB75 output and built-in WiFi support. I picked up one of them and then had everything I needed.

I wanted to do something useful with the matrix. Eventually I settled on showing the current weather conditions on it. I have an Ambient Weather weather station. It uploads data to the Ambient Weather site. Nicely, they provide a simple API where I can pull my data back down.

<a href="../images/2024/weather_matrix.jpg" title="click for larger size"><img src="../images/2024/weather_matrix.jpg" width="480" title="My matrix showing the weather conditions"/></a>

Given the really low resolution of my matrix, I planned to show one weather stat at a time, then cycle to the next. For example, show the temperature, then a moment later show the wind speed, and so forth. I planned to poll the API every few minutes to get updated data.

## CircuitPython

While I could program the MatrixPortal in C, I'm a lot more comfortable with Python. Adafruit publishes a version of <a href="https://docs.circuitpython.org/en/latest/docs/index.html" target="_blank">CircuitPython</a> for this board. CircuitPython is a slimmed-down version of Python meant to run on microcontrollers. I downloaded the version for my board. The install process is pretty simple. You plug the board into a USB port and copy the CircuitPython files to the board. That's it.

It's important to note again that CircuitPython is a subset of Python. You could probably install some Python (PyPI) libraries, but more commonly you'll use the libraries that Adafruit publishes. These are provided as files that you copy as needed to the lib folder on the MatrixPortal (or other board you're using).

The MatrixPortal has pretty limited memory and storage. You need to be careful to install only the libraries you need to reduce the chance of running out of memory for your code. Make sure to delete any libraries you're not using off the board, too.

There's no compile step with CircuitPython. Simply copy your code.py file to your microcontroller. It will reboot and load your new version.

## Challenges

Like Python, CircuitPython includes an automatic garbage collector to free memory when it's no longer used. However, the MatrixPortal was so limited in memory, I found I needed to force collection regularly in my program. Without that, the program would crash with an out of memory error.

Liberal use of `gc.collect()` helped a lot, but didn't fully resolve the issue. For a while, I was convinced that the requests library was too heavy for the MatrixPortal. I even considered giving up on the project till I realized the silly error I was making. By default, the Ambient Weather API call I was making was returning dozens of data readings when I wanted only the most recent one. Once I added the `&limit=1` param to the URL, I was able to get the program working.

The other challenge I had to overcome was how to handle the two panels I was trying to use as if it were one larger panel. The trick turned out to be the `serpentine` parameter. In the following call, `tile_rows` specifies I have two panels. `serpentine=False` indicates I want them laid out serially, not in a serpentine fashion. You'd think that wouldn't matter with just two panels. But without that, I could not get the orientation of the two panels to work correctly.

    :::python
    matrix = Matrix(width=32, height=32, tile_rows=2, serpentine=False)

## Adding a background graphic

Once I had the basic text version working, I decided to get fancy and show a GIF as a background. I used a graphics editor to create a 32x32 pixel image (to match my matrix size). The `gifio` built-in library can be used to show static or animated GIFs. Note that the `OnDiskGif()` function loads the GIF, but not the image within it until you call the `next_frame()` method. (That's the method you'd call to load subsequent frames in an animated GIF.)

    :::python
    odg = gifio.OnDiskGif('/background.gif')
    odg.next_frame()  # critical or no image will appear
    # Depending on your display the next line may need Colorspace.RGB565
    #   instead of Colorspace.RGB565_SWAPPED. If the colors are wonky,
    #   try changing this.
    mygif = displayio.TileGrid(odg.bitmap,
                            pixel_shader=displayio.ColorConverter
                            (input_colorspace=displayio.Colorspace.RGB565_SWAPPED))
    group.append(mygif)

My GIF is pretty simple. Some blue at the top to represent the sky. Some green at the bottom to represent grass. It's simple, but it made me happy to have it there.

## Full code

Below is the full contents of my code.py file. The secrets.py file contains a simple dict named `secrets` whose keys are my SSID, WiFi password, Ambient Weather keys, and so forth.

    #!python
    import board  # for pin definitions
    import busio  # to access SPI bus
    import displayio
    import gc
    import gifio

    from adafruit_esp32spi import adafruit_esp32spi_wifimanager
    from adafruit_display_text.label import Label
    from adafruit_esp32spi import adafruit_esp32spi
    from adafruit_matrixportal.matrix import Matrix
    from digitalio import DigitalInOut
    from rtc import RTC
    from terminalio import FONT  # Provides the font we use
    from time import sleep

    gc.collect()

    # Get wifi details and more from a secrets.py file
    try:
        from secrets import secrets
    except ImportError:
        raise

    print(f"Free memory (start): {gc.mem_free()}")

    url = f"https://rt.ambientweather.net/v1/devices/{secrets['device_mac']}?applicationKey={secrets['awn_application_key']}&apiKey={secrets['awn_api_key']}&limit=1"

    esp32_cs = DigitalInOut(board.ESP_CS)
    esp32_ready = DigitalInOut(board.ESP_BUSY)
    esp32_reset = DigitalInOut(board.ESP_RESET)
    spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
    esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)

    requests = adafruit_esp32spi_wifimanager.ESPSPI_WiFiManager(esp, secrets, None)
    requests.connect()

    try:
        print("Connected to", str(esp.ssid, "utf-8"), "\tRSSI:", esp.rssi)
        print("My IP address is", esp.pretty_ip(esp.ip_address))
        print(f"Free memory (network connected): {gc.mem_free()}")
    except:
        pass

    matrix = Matrix(width=32, height=32, tile_rows=2, serpentine=False)
    display = matrix.display

    # --- Drawing setup ---
    group = displayio.Group()  # Create a Group
    bitmap = displayio.Bitmap(32, 32, 1)  # Create a bitmap object,width, height, bit depth
    color = displayio.Palette(2)  # Create a color palette

    # Create a TileGrid using the Bitmap and Palette
    tile_grid = displayio.TileGrid(bitmap, pixel_shader=color)
    group.append(tile_grid)  # Add the TileGrid to the Group
    display.root_group = group

    odg = gifio.OnDiskGif('/background2.gif')
    odg.next_frame()
    # Depending on your display the next line may need Colorspace.RGB565
    #   instead of Colorspace.RGB565_SWAPPED
    mygif = displayio.TileGrid(odg.bitmap,
                            pixel_shader=displayio.ColorConverter
                            (input_colorspace=displayio.Colorspace.RGB565_SWAPPED))
    group.append(mygif)

    # Text area 1
    label_1 = Label(FONT)
    label_1.text = "LOADING"
    label_1.color = 0xFF0000
    _, bby, bbwidth, bbh = label_1.bounding_box  # _ is bbx
    label_1.x = 2  # round(display.width / 2 - bbwidth / 2)
    label_1.y = display.height // 2 - bbh // 2 - (-bby) // 2 + 3
    group.append(label_1)

    # # Text area 2
    label_2 = Label(FONT)
    label_2.text = "##"
    label_2.color = 0xFF0000

    _, bby2, bbwidth2, bbh2 = label_2.bounding_box
    label_2.x = 2  # round(display.width / 2 - bbwidth2 / 2)
    label_2.y = display.height - bbh2 // 2 - (-bby2) // 2 - 1
    group.append(label_2)

    display.show(group)


    def twoDigits(n):
        d2 = n % 10
        d1 = int(n / 10)
        return str(d1) + str(d2)


    def parse_weather_data(resp):
        gc.collect()
        print(f"Free memory (parse_weather_data): {gc.mem_free()}")
        if resp:
            updated_weather = resp.json()
            gc.collect()
            return updated_weather[0]
        return current_weather


    def get_weather_conditions():
        gc.collect()
        print(f"Free memory (get_weather_conditions): {gc.mem_free()}")
        resp = requests.get(url)
        print(f"response code: {resp.status_code}")
        if resp.status_code == 200:
            return resp


    """
    0xFF0000  # red
    0x00FF00  # green
    0x0000FF  # blue
    0x9933FF  # purple
    """
    keys = [
        "tempf",
        "feelsLike",
        "humidity",
        "windspeedmph",
        "windgustmph",
        "winddir",
        "dailyrainin",
    ]
    labels = {
        "tempf": ("Temp.", 0xFF0000),
        "feelsLike": ("Feels", 0xFF0000),
        "humidity": ("Humid", 0x0000FF),
        "windspeedmph": ("Wind", 0x9933FF),
        "windgustmph": ("Gust", 0x9933FF),
        "winddir": ("Direc", 0x00FF00),
        "dailyrainin": ("Rain", 0x0000FF),
    }
    current_key = 0
    current_weather = parse_weather_data(get_weather_conditions())

    def publish_weather_conditions(current_weather: dict, current_key: int):
        key = keys[current_key]
        value = str(current_weather[key])
        try:
            value_int = int(float(value))
        except ValueError:
            value_int = 0
        label = labels[key][0]
        color = labels[key][1]
        print(key, value)
        label_1.text = label
        label_2.text = value
        label_1.color = color
        label_2.color = color
        if current_key == 0 and value_int < 40:
            # if the temp is below 40, blue instead of red for Temp
            label_1.color = 0x0000FF
            label_2.color = 0x0000FF


    while True:
        if current_key == len(keys):
            current_key = 0
        ts = RTC().datetime
        mins = twoDigits(ts.tm_min)
        secs = twoDigits(ts.tm_sec)
        if int(mins) % 5 == 0.0 and int(secs) == 0:
            # retrieve data every 5 mins
            print("Retrieving fresh data & updating display...")
            current_weather = parse_weather_data(get_weather_conditions())
            publish_weather_conditions(current_weather, current_key)
        if int(secs) % 3 == 0:
            # update display every 3 seconds
            print("updating display...")
            publish_weather_conditions(current_weather, current_key)
        current_key += 1
        sleep(1)
