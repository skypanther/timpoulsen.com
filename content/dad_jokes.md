Title: Dad Jokes As a Service
Description: Light-hearted article showing how to implement the Dad Jokes python library.
Date: 2023-07-24
Category: Python
Tags: python
Slug: dad-jokes

# Everyone loves a good dad joke

... now, if only there were some _good_ dad jokes!

The [ICanHazDadJoke site](https://icanhazdadjoke.com/) claims to maintain the internet's largest collection of dad jokes. GitHub user [CrossNox](https://github.com/crossnox/dadjokes) has made a nice wrapper around their API. Together, this lets you retrieve a random dad joke programmatically.

Why, you ask, would you want to get a dad joke programmatically? You could include it in your web site or app, showing random dad jokes to delight your users. You could write a simple script to retrieve and show you the joke from the command line. You could even prank someone and have their computer speak a dad joke every day.

You'll need the library. A simple `pip install dadjokes` will take care of that.

Then, you'll need this simple script:

    :::python
    from dadjokes import Dadjoke
    dadjoke = Dadjoke()
    print(dadjoke.joke)

Whenever you need a laugh, from the directory where you saved that script, run `python dadjoke.py`

## Some simple enhancements (for \*nix systems)

You can make this file executable, so you can run it with having to put the `python` part on the command. First, let's find out where your `python` executable is located. Enter `which python3` and note the path that is output. Next, edit your script. As the very first line, you'll add a "hashbang" that points to your python executable. Like this:

    :::python
    #!/path/to/your/python

    from dadjokes import Dadjoke
    dadjoke = Dadjoke()
    print(dadjoke.joke)

Once you've saved your changes, you can mark the file as executable with `chmod +x dadjoke.py` From now on, you can type `./dadjoke.py` to run the script. Wow, that saved you from typing like 5 whole characters!

For you Mac users, you can use the built-in `say` program and have your system speak the dad joke. Enter `./dadjoke.py | say` (If you can believe it, the jokes are even less funny when spoken by the monotone computerized voice.)

It would be unprofessional of me to suggest you sneak over to a coworkers computer when they leave it unlocked, and set up a cron job to have a dad joke spoken to them throughout the day. So, I won't suggest that.

<img src="https://icanhazdadjoke.com/static/smile.svg" alt="icanhazdadjoke logo" style="width:1.5em;margin-top:0.25em;">
