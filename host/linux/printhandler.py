#!/usr/bin/env python

import struct
import sys
import cups
import json
import urllib2
import zipfile
import os
import Queue


class PrintHost:

    c_path = os.path.dirname(os.path.realpath(__file__))+os.sep
    file = ""
    raw = ""
    real_name = ""
    printer = ""
    queue = Queue.Queue()
    interactions = 3  # Number of retries before quit reading stdin

    def read_input(self):  # Read web messages and put them in the queue
        self.send_message("LOG", "Started reading input")
        text = ""
        while text == "":
            self.send_message("LOG", "Waiting for input")
            text_length_bytes = sys.stdin.read(4)  # Read the message length integer at first 4 bytes.
            if len(text_length_bytes) > 0:
                text_length = struct.unpack("i", text_length_bytes)[0]  # Convert Bytes to integer
                text = sys.stdin.read(text_length)  # Reading length defined at the 4 bytes header
                self.queue.put(text)
                self.process_message()
        self.interactions -= 1
        if self.interactions == 0:
            if self.queue.empty():  # if nothing more to process quit else continue
                sys.exit(0)
            else:
                self.process_message()
        else:
            self.read_input()

    def process_message(self):  # Message Processor reads the queued messages and quit
        while not self.queue.empty():
            message = self.queue.get_nowait()
            self.send_message("LOG", "process_message -> Processing received message: " + message)
            content = json.loads(message)
            content_keys = content.keys()
            if "printer" in content_keys:  # User sent a print intent
                self.printer = content["printer"]
                self.file = content["file"]
                self.send_message("LOG", "process_message -> Try Printing at " + self.printer)
                try:
                    is_zip = self.get_file()
                    if is_zip:
                        self.unzip()
                    self.send_to_printer()
                    self.send_message("LOG", "process_message -> Printed at " + self.printer)
                except (IOError, RuntimeError, OSError):
                    self.send_message("ERROR", sys.exc_info())
                    sys.exit(1)
            elif "list" in content_keys:  # Retrieve the printers list
                self.enum_printers()
            else:  # Command not implemented
                self.send_message("LOG", "There is no method implemented to handle:" + message)
                sys.exit(1)
        self.read_input()  # Check again for incoming messages

    def enum_printers(self):
        try:
            con = cups.Connection()
            printer_list = con.getPrinters()
            for printer in printer_list:
                self.send_message("printer", json.dumps(printer))
        except (IOError, RuntimeError, OSError):
            self.send_message("ERROR", sys.exc_info())

    def get_file(self):
        file_type = self.file.split(".")[-1]
        self.real_name = self.file.split(".")[-2].split("/")[-1]
        self.send_message("LOG", "get_file -> Starting download of " + self.file)

        download_file = urllib2.urlopen(self.file)
        dl_file = self.c_path + "print."+file_type  # Set local file name, will be downloaded to the installation folder
        fo = open(dl_file, "wb+")  # Open the destination file for writing in binary mode (clears the previous content)
        self.raw = ""
        while True:  # waiting to finish the download
            data = download_file.read(8192)
            if not data:
                break
            else:
                try:
                    fo.write(data)  # write chunk to the zip file
                    self.raw += data
                except IOError:
                    self.send_message("ERROR", sys.exc_info())
                    sys.exit(1)
        self.file = dl_file
        self.send_message("LOG", "get_file -> Done downloading file")
        return True if file_type == "zip" else False  # Define if the file is a zip or not

    # TODO: Create a method that supports multiple files at the zip archive if needed
    def unzip(self):
        print_file = self.c_path + "print.txt"
        self.send_message("LOG", "unzip -> File set as: {0}".format(self.file))
        self.raw = ""
        if zipfile.is_zipfile(self.file):
            to_unzip = zipfile.ZipFile(self.file)
            for name in to_unzip.namelist():
                try:
                    fo = open(print_file, "wb")
                    self.raw = to_unzip.read(name)
                    fo.write(self.raw)
                    fo.close()
                except (IOError, RuntimeError, AssertionError, OSError):
                    self.send_message("LOG", "unzip -> ERROR: Cannot Open zip file")
                    self.send_message("ERROR", sys.exc_info())
                    sys.exit(1)
        else:
            sys.exit(5)
        self.file = print_file

    def send_to_printer(self):
        doc_name = "PyJob_" + self.real_name  # create a name for the job
        self.send_message("LOG", "send_to_printer -> Print job setup")
        con = cups.Connection()
        con.printFile(self.printer, self.file, doc_name, dict())
        self.send_message("LOG", "send_to_printer -> print Job done")
        sys.exit(0)

    @staticmethod
    def send_message(msg_type, msg):

        if msg_type == "ERROR":
            msg = "{\"Error\": \"An error has occurred:\n" + repr(msg) + "\"}"
        elif msg_type == "EXIT":
            sys.stdin.close()
        else:
            msg = json.dumps({msg_type.lower(): msg})
        sys.stdout.write(struct.pack("I", len(msg)))
        sys.stdout.write(msg)
        sys.stdout.flush()

    def __init__(self):
        self.send_message("LOG", "Main -> Started native client")
        self.read_input()


def main():
    PrintHost()

if __name__ == "__main__":
    main()
