"""
Tool to send emails and attachments through the terminal
"""
import smtplib
import argparse
import json
import getpass
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


class TerminalEmail(object):
    """
    Send email from the terminal.
    """
    def __init__(self,
                 toaddr,
                 subject="",
                 body="",
                 file_path=""):
        """
        initialize initial arguments and set up
        """
        self.msg = MIMEMultipart()
        self.toaddr = toaddr
        self.subject = subject
        self.body = body
        self.file_path = file_path
        self.fromaddr = ""
        self.password = ""
        self.__parse_credentials()

    def __parse_credentials(self):
        """
        parse credentials json file if it exists
        """
        if os.path.isfile("credentials.json"):
            with open("credentials.json") as f:
                data = json.load(f)
            self.fromaddr = data["fromaddr"]
            self.password = data["password"]
        else:
            self.fromaddr = input("Enter your email\n")
            self.password = getpass.getpass("Enter email password\n")

    def build_msg(self):
        """
        Builds the message to be sent
        """
        self.msg["fromaddr"] = self.fromaddr
        self.msg["To"] = self.toaddr
        self.msg["Subject"] = self.subject
        self.msg.attach(MIMEText(self.body, "plain"))

    def send_file(self):
        """
        Send a file if a file path was supplied
        """
        attachment = open(self.file_path, "rb")
        filename = os.path.basename(self.file_path)
        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition',
                        "attachment; filename= %s" % filename)
        self.msg.attach(part)

    def launch_server(self):
        """
        Sets up smtp server and launches it with created message
        """
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.login(self.fromaddr, self.password)
        text = self.msg.as_string()
        server.sendmail(self.fromaddr, self.toaddr, text)
        server.quit()

    @classmethod
    def __parse_args(cls):
        """
        parse args
        """
        parser = argparse.ArgumentParser()
        parser.add_argument("toaddr",
                            help="Recipient address",
                            action="store")
        parser.add_argument("-s", "--subject",
                            help="Subject of email",
                            action="store")
        parser.add_argument("-b", "--body",
                            help="Body of email",
                            action="store")
        parser.add_argument("-f", "--file_path",
                            help="File to send",
                            action="store")
        args = parser.parse_args()
        return vars(args)

    @classmethod
    def main(cls):
        """
        main
        """
        args = cls.__parse_args()
        obj = cls(**args)
        obj.build_msg()
        if os.path.isfile(obj.file_path):
            obj.send_file()
        obj.launch_server()

if __name__ == "__main__":
    TerminalEmail.main()
