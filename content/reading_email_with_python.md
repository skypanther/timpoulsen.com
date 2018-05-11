Title: Reading email with Python
Date: May 10, 2018
Category: Python
Tags: python
Status: draft

For a recent project at work, I needed to read and parse email messages with a python script. I found the documentation confusing, and most of the samples on various blogs and StackOverflow posts to be old and not fully compatible with python 3.x. So, here is an adaptation of my solution.

Further below in this post is my actual class for interacting with an IMAP email account, logging in and out, accessing the messages in a folder (such as the INBOX), and even deleting messages. But let's start with a simple script that uses the class.

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

## Gmail vs other mail servers

For my work needs, I needed to access a GSuite (Gmail for business) email account. So, the class and my use of it is a bit specific to Gmail. While it will work fine for other providers, you may need to tweak the `delete_message` method since it is specific to Gmail's trash-vs-deleted folder locations.


## The class

The class itself is considerably longer and more involved than the script that uses it. The following should be in a file named ImapClient.py in the same directory as the script that uses it. Look the code over. I'll explain some key points after the code.

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
                        return
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

As you can see in the `__init__` method, you must specify a recipient address. This is the email account you're logging into. You can override other defaults, such as the server to log into, the folder to read from, and so forth.

The `login()` and `logout()` methods should be fairly self-explanatory. The `select_folder()` method is optional. By default, the class will read from the INBOX folder but you could change that with this method.

Let's dig into the `get_messages()` method since it's the meat of what the class is offering. My work needs dictated that I would be monitoring messages from a specific sender. For that reason, line 55 checks for a required `sender` param. Then, on line 60 we search the inbox for



IMAP, folders, message IDs, message parts, content disposition, etc.

