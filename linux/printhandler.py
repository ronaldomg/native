import struct
import sys

import json
import urllib2
import zipfile
import os


class PrintHost:

    c_path = os.path.dirname(os.path.realpath(__file__))+os.sep
    file = ""
    raw = ""
    real_name = ""
    printer = ""
    # Thread that reads messages from the web.

    @staticmethod
    def read_input(self):

        self.send_message("LOG", "Started reading input")
        text = ""
        # Number of retries after quitting
        interactions = 2

        while text == "":
            self.send_message("LOG", "Waiting for input")
            # Read the message length (first 4 bytes).
            text_length_bytes = sys.stdin.read(4)

            if len(text_length_bytes) > 0:
                self.send_message("LOG", "Reading input")
                # Unpack message length as 4 byte integer.
                self.text_length = struct.unpack("i", text_length_bytes)[0]

                # Read the text (JSON object) of the message.
                text = sys.stdin.read(text_length)
                self.send_message("LOG", "{received:" + text + "}")
                self.process_message(text)

            # Reduce remaining interactions
            interactions -= 1
            if interactions == 0:
                sys.exit(0)
            else:
                read_input()
        sys.exit(0)

    # Message Processor
    def process_message(self, message):
        self.send_message("LOG", "process_message -> Processing received message: " + message)
        content = json.loads(message)
        if content["printer"]:  # user sent a print intent
            self.printer = content["printer"]
            self.file = content["file"]
            self.send_message("LOG", "process_message -> Try Printing at " + printer)
            try:
                is_zip = self.get_file()
                if is_zip:
                    self.unzip()
                self.send_to_printer()
                # print_it(printer, to_print)
                send_message("LOG", "process_message -> Printed at " + printer)
            except (IOError, RuntimeError, OSError):
                send_message("ERROR", sys.exc_info())
                sys.exit(1)
        sys.exit(0)

    @staticmethod
    def enum_printers(self):
        try:
            import cups
            con = cups.Connection()
            printer_list = con.getPrinters()
            # print printer_list
            for printer in printer_list:
                self.send_message("printer", json.dumps(printer))

        except (IOError, RuntimeError, OSError):
            self.send_message("ERROR", sys.exc_info())
            sys.exit(1)
        sys.exit(0)

    @staticmethod
    def get_file(self):
        file_type = self.file.split(".")[-1]
        self.real_name = self.file.split(".")[-2].split("/")[-1]
        self.send_message("LOG", "get_file -> Starting download of " + file_url)

        download_file = urllib2.urlopen(self.file)
        self.send_message("LOG", "get_file -> Download setup done")

        dl_file = self.c_path + "print."+file_type  # Set local zip file name will be written at the installation folder
        self.send_message("LOG", "get_file -> Download file set as: {0}".format(dl_file))

        fo = open(dl_file, "wb+")  # Open the destination file for writing in binary mode (clears the previous content)
        self.send_message("LOG", "get_file -> Opening file for writing")
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

        self.send_message("LOG", "get_file -> Done downloading file")
        is_zip = True if file_type == "zip" else False

        return is_zip

    @staticmethod
    def unzip(self):
        print_file = c_path + "print.txt"
        self.send_message("LOG", "unzip -> File set as: {0}".format(prn_file["file"]))
        self.raw = ""
        try:
            if zipfile.is_zipfile(prn_file["file"]):
                to_unzip = zipfile.ZipFile(prn_file["file"])
            else:
                send_message("LOG", "unzip -> ERROR: Cannot Open zip file")
                sys.exit(1)
            for name in to_unzip.namelist():
                fo = open(print_file, "wb")
                self.raw = to_unzip.read(name)
                fo.write(print_file)
                fo.close()
        except (IOError, RuntimeError, AssertionError, OSError):
            send_message("ERROR", sys.exc_info())
            sys.exit(1)
        self.file = print_file

    @staticmethod
    def send_to_printer(self):
        doc_name = "PyJob_" + self.real_name  # create a name for the job
        self.send_message("LOG", "send_to_printer -> Print job setup")
        con = cups.Connection()
        con.printFile(self.printer, self.file, doc_name, dict())
        self.send_message("LOG", "send_to_printer -> print Job done")
        sys.exit(0)

    @staticmethod
    def send_message(msg_type, msg):
        print msg
        if msg_type != "ERROR":
            message = "{\"" + msg_type.lower() + "\": \"" + msg + "\"}"
        else:
            message = "{\"Error\": \"An error has occurred\"}"
            fo = open("errorlog", "wb+")
            fo.write()
            fo.write(msg)
            fo.close()
        sys.stdout.write(struct.pack("I", len(message)))
        sys.stdout.write(message)
        sys.stdout.flush()

    def __init__(self):
        self.send_message("LOG", "Main -> Started native client")
        self.read_input(self)
        sys.exit(0)


def main():
    PrintHost()
    sys.exit(0)

if __name__ == "__main__":
    main()
