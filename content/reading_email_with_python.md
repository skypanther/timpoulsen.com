Title: Reading email with Python
Date: May 10, 2018
Category: Python
Tags: python

For a recent project at work, I needed to read and parse email messages with a python script. I found the documentation confusing, and most of the samples on various blogs and StackOverflow posts to be old and not fully compatible with python 3.x. So, here is an adaptation of my solution.

Further below in this post is my actual class for interacting with an IMAP email account, logging in and out, accessing the messages in a folder, and even deleting messages. But let's start with a simple script that uses the class.

## Using the class

As I'm sure you know, it's a bad idea to code passwords into a file. Instead, you should load them at runtime, either from a command line argument (e.g. with the `argparse` library) or from the system environment. The script I wrote for work was going to be part of a Django project deployed in a Docker container, so for my needs an environment variable was the best choice. 

Before you can use the script below, you'll have to add a `mailpwd` environment variable (or modify the code to use argparse). On Linux/OS X, use `export mailpwd=password` and on Windows, er, sorry, I don't know.


    #!python
    from .ImapClient import ImapClient


    def main():
        """
        You will need to store your email password in your environment, e.g.
        export mailpwd=password
        """
        imap = ImapClient(recipient='you@gmail.com')
        imap.login()
        # retrieve messages from a given sender
        messages = imap.get_messages(sender='a_friend@another_isp.com')
        # Do something with the messages
        print("Messages in my inbox:")
        for msg in messages:
            # msg is a dict of {'num': num, 'body': body}
            print(msg['body'])
            # you could delete them after viewing
            # imap.delete_message(msg['num'])
        # when done, you should log out
        imap.logout()


    if __name__ == "__main__":
        main()

## Some peculiarities of the class

For my work needs, I needed to access a GSuite (Gmail for business) email account. So, the class is a bit specific to Gmail. While it will work with other providers, you may need to tweak the `delete_message` method since it is specific to Gmail's trash-vs-deleted folder locations.

Another specific need I had was to monitor emails from a specific sender. Thus, as shown on line 12 above, you must pass in a sender's email address when calling `get_message()`. The script would need some rewriting to accommodate other needs. But hopefully what's below will get you started.

## The class

The class itself is considerably longer and more involved than the script that uses it. The following should be in a file named ImapClient.py in the same directory as the script that uses it. Look the code over. I'll explain some its points after the code.

    #!python
    import email
    import email.header
    import imaplib
    import os
    import sys
    
    
    class ImapClient:
        imap = None

        def __init__(self,
                     recipient,
                     server='imap.gmail.com',
                     use_ssl=True,
                     move_to_trash=True):
            # check for required param
            if not recipient:
                raise ValueError('You must provide a recipient email address')
            self.recipient = recipient
            self.use_ssl = use_ssl
            self.move_to_trash = move_to_trash
            self.recipient_folder = 'INBOX'
            # instantiate our IMAP client object
            if self.use_ssl:
                self.imap = imaplib.IMAP4_SSL(server)
            else:
                self.imap = imaplib.IMAP4(server)

        def login(self):
            try:
                rv, data = self.imap.login(self.recipient, os.getenv('mailpwd', ''))
            except (imaplib.IMAP4_SSL.error, imaplib.IMAP4.error) as err:
                print('LOGIN FAILED!')
                print(err)
                sys.exit(1)

        def logout(self):
            self.imap.close()
            self.imap.logout()

        def select_folder(self, folder):
            """
            Select the IMAP folder to read messages from. By default
            the class will read from the INBOX folder
            """
            self.recipient_folder = folder

        def get_messages(self, sender, subject=''):
            """
            Scans for email messages from the given sender and optionally
            with the given subject

            :param sender Email address of sender of messages you're searching for
            :param subject (Partial) subject line to scan for
            :return List of dicts of {'num': num, 'body': body}
            """
            if not sender:
                raise ValueError('You must provide a sender email address')

            # select the folder, by default INBOX
            resp, _ = self.imap.select(self.recipient_folder)
            if resp != 'OK':
                print(f"ERROR: Unable to open the {self.recipient_folder} folder")
                sys.exit(1)

            messages = []

            mbox_response, msgnums = self.imap.search(None, 'FROM', sender)
            if mbox_response == 'OK':
                for num in msgnums[0].split():
                    retval, rawmsg = self.imap.fetch(num, '(RFC822)')
                    if retval != 'OK':
                        print('ERROR getting message', num)
                        continue
                    msg = email.message_from_bytes(rawmsg[0][1])
                    msg_subject = msg["Subject"]
                    if subject in msg_subject:
                        body = ""
                        if msg.is_multipart():
                            for part in msg.walk():
                                type = part.get_content_type()
                                disp = str(part.get('Content-Disposition'))
                                # look for plain text parts, but skip attachments
                                if type == 'text/plain' and 'attachment' not in disp:
                                    charset = part.get_content_charset()
                                    # decode the base64 unicode bytestring into plain text
                                    body = part.get_payload(decode=True).decode(encoding=charset, errors="ignore")
                                    # if we've found the plain/text part, stop looping thru the parts
                                    break
                        else:
                            # not multipart - i.e. plain text, no attachments
                            charset = msg.get_content_charset()
                            body = msg.get_payload(decode=True).decode(encoding=charset, errors="ignore")
                        messages.append({'num': num, 'body': body})
            return messages

        def delete_message(self, msg_id):
            if not msg_id:
                return
            if self.move_to_trash:
                # move to Trash folder
                self.imap.store(msg_id, '+X-GM-LABELS', '\\Trash')
                self.imap.expunge()
            else:
                self.imap.store(msg_id, '+FLAGS', '\\Deleted')
                self.imap.expunge()


## Class details

The `login()` and `logout()` methods should be fairly self-explanatory. The `select_folder()` method is optional. By default, the class will read from the INBOX folder but you could change that with this method.

As you can see in the `__init__` method, you must specify a recipient address. This is the email account you're logging into. You can override other defaults, such as the server to log into, whether to connect over SSL, and so forth.

Let's dig into the `get_messages()` method since it's the meat of what the class is offering. After checking params, it attempts to select the folder to search. Of the two values returned, we care only about the first one `resp` which will be the string 'OK' if we succeed. Next we search for messages from the sender (line 68). Again, two values are returned, but this time we want to use both.

As before, the first value, `mbox_response` is an OK/not okay string. The second value is a list, the first member of which is the list of message numbers that match our search criteria. Every IMAP message in the folder is identified by an integer ID. To fetch the actual message, we'll use the `imap.fetch()` method, passing to it the message ID number, and the portion of the content we want to retrieve. If you've looked at other IMAP examples, you'll see folks using many other content selectors. Here, we're using `'(RFC822)'` to basically grab the entire message.

Assuming that was retrieved from the server successfully, on line 75 we convert the raw representation of the message into a mail object we can further inspect. Then, we grab the subject on line 76. My original needs called for looking for messages with a given subject. It's optional; if you don't pass in a subject param to the function you'll retrieve all the messages from the sender.

Starting on line 78, we extract the text from the message. The full IMAP specification (RFC 822) is quite complex. But for our needs now, we can ignore many of those details. Messages can be single or multipart. A single part message would be a very simple plain text email message, the type generated by email clients of the days before pretty formatted emails. (Such messages are still sent, though more typically these days by scripts/generators rather than by users with some mail app.) Multipart messages represent their contents in multiple formats, such as plain text and HTML formatted. The typical Gmail, Outlook, webmail generated email message would be a multipart message containing probably both a plain text and HTML formatted part.

On line 79, we determine the message type and on line 80, we begin walking the parts looking for the plain text part. We do so in two ways. First, with `part.get_content_type()` we determine whether it is plain/text or not. But, a text attachment to a message would have that content type too. So, on line 84 we check for that by looking at the content disposition, which will include the string `'attachment'` if this part is an attachment. 

Finally (and we do this for both the multipart and single part sections) we need to convert the raw byte representation of the part into plain text. We determine its original character set (e.g. ISO-8859-1, UTF-8, etc.) using `part.get_content_charset()` and then convert to that representation on line 87 (or 92). 

Each message that makes it through this filtering and converting is added as a dict to the `messages` list. We return both the message ID and its text. And then finally we return that list to the caller.

## Deleting messages

Deleting a message from an IMAP server involves two steps: copying it to the trash folder and calling `expunge()` to remove it from its original folder. With Gmail, there are two "deleted" folders: Trash and Deleted. The first of these is like the Recycle Bin / Trash folder on your computer. Messages in Trash are easily recoverable. Depending on your mail provider, messages moved to Deleted could be fully removed. Google never deletes anything, even when you empty the trash. You can always do a search to find messages in the Deleted folder (but you'll need to know a subject or sender or some other criterion to find it).

The `delete_message()` method requires a message ID and will then move that message to the Trash (default behavior) or delete the message based on the value of `move_to_trash` parameter you supplied when instantiating the ImapClient object.

## Summary

While the class is a bit involved, it really only scratches the surface of IMAP message complexity. Still, this class makes for a fairly simple means to grab messages from an email inbox and read their plaintext representations. I hope it helps clarify how IMAP works and gives you a good starting point for your email needs.

