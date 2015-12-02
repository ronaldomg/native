class printHost:

    import struct
    import sys
    import cups
    import json
    import urllib2
    import zipfile
    import os

    c_path = os.path.dirname(os.path.realpath(__file__))+os.sep

    # Thread that reads messages from the web.
    @staticmethod
    def read_input():
        process_message('{"file": "http://192.168.0.30:8080/blue/admin/EtqTermica70408.txt.zip", "printer": "Argox-PPLB-Label"}')
        sys.exit(0)
        send_message("LOG", "Started reading input")
        text = ""
        # Number of retries after quitting
        interactions = 2

        while text == "":
            send_message("LOG", "Waiting for input")
            # Read the message length (first 4 bytes).
            text_length_bytes = sys.stdin.read(4)

            if len(text_length_bytes) > 0:
                send_message("LOG", "Reading input")
                # Unpack message length as 4 byte integer.
                text_length = struct.unpack("i", text_length_bytes)[0]

                # Read the text (JSON object) of the message.
                text = sys.stdin.read(text_length)
                send_message("LOG", "{received:" + text + "}")
                process_message(text)

            # Reduce remaining interactions
            interactions -= 1
            print(interactions)
            if interactions == 0:
                sys.exit(0)
            else:
                read_input()
        sys.exit(0)


    # Message Processor
    def process_message(message):
        send_message("LOG", "process_message -> Processing received message: " + message)
        content = json.loads(message)
        # printer is the user selected printer
        printer = content["printer"]
        # toPrint is the file url
        file_url = content["file"]
        send_message("LOG", "process_message -> printer: " + printer)
        send_message("LOG", "process_message -> file: " + file_url)
        if printer:
            send_message("LOG", "process_message -> Try Printing at " + printer)
            try:
                send_message("LOG", "process_message -> Will Printing at " + printer)
                prn_file = get_file(file_url)
                if prn_file['is_zip']:
                    prn_file = unzip(prn_file)
                prn_file['printer'] = printer
                send_to_printer(prn_file)
                # print_it(printer, to_print)
                send_message("LOG", "process_message -> Printed at " + printer)
            except (IOError, RuntimeError, OSError):
                send_message("ERROR", sys.exc_info())
                sys.exit(1)
        sys.exit(0)


    def get_file(file_url):
        file_type = file_url.split('.')[-1]
        real_name = file_url.split('.')[-2].split("/")[-1]
        send_message("LOG", "get_file -> Starting download of " + file_url)
        # open url connection to download file
        download_file = urllib2.urlopen(file_url)
        send_message("LOG", "get_file -> Download setup done")
        # Set local zip file name will be written at the installation folder
        dl_file = c_path + "print."+file_type
        send_message("LOG", "get_file -> Download file set as: {0}".format(dl_file))
        # Open the destination file for writing (clears the previous content)
        fo = open(dl_file, "wb+")
        send_message("LOG", "get_file -> Opening file for writing")
        raw = ""
        while True:  # waiting to finish the download
            send_message("LOG", "get_file -> Downloading data ...")
            data = download_file.read(8192)
            send_message("LOG", "get_file -> Getting a 1Kb chunk ...")
            if not data:
                send_message("LOG", "get_file -> No data stream ....")
                break
            else:
                send_message("LOG", "get_file -> Try: Write to file")
                try:
                    fo.write(data)  # write chunk to the zip file
                    raw += data
                    send_message("LOG", "get_file -> Writing to file")
                except IOError:
                    send_message("ERROR", sys.exc_info())
                    sys.exit(1)

        send_message("LOG", "get_file -> Done downloading file")
        is_zip = True if file_type == 'zip' else False
        result = {'file': dl_file, 'raw': raw, 'is_zip': is_zip, 'real_name': real_name}

        return result


    def unzip(prn_file):
        print_file = c_path + "print.txt"
        send_message("LOG", "unzip -> File set as: {0}".format(prn_file['file']))
        raw = ''
        try:
            send_message("LOG", "unzip -> Try: Unzip the file: {0}".format(prn_file['file']))
            send_message("LOG", "unzip -> Try: Open zip file")
            if zipfile.is_zipfile(prn_file['file']):
                to_unzip = zipfile.ZipFile(prn_file['file'])
            else:
                send_message("LOG", "unzip -> ERROR: Can't Open zip file")
                sys.exit(1)
            for name in to_unzip.namelist():  # interact with the list of files at zip archive
                fo = open(print_file, "wb")
                raw = to_unzip.read(name)  # open the print file for writing (clears the previous content)
                fo.write(print_file)  # write the result of the unzipping
                fo.close()  # close the file object
        except (IOError, RuntimeError, AssertionError, OSError):
            send_message("ERROR", sys.exc_info())
            send_message("LOG", "unzip -> A error has occurred")
            sys.exit(1)
        result = {'file': print_file, 'raw': raw, 'is_zip': prn_file['is_zip'], 'real_name': prn_file['real_name']}
        return result


    def send_to_printer(prn_file):
        doc_name = "Pyprint" + prn_file['real_name']  # create a name for the job
        send_message("LOG", "send_to_printer -> Print job setup")
        con = cups.Connection()
        con.printFile(prn_file['printer'], prn_file['file'], doc_name, dict())
        send_message("LOG", "send_to_printer -> print Job done")
        sys.exit(0)


    def send_message(msg_type, msg):
        print(msg_type)
        print(msg)
        # if msg_type == "LOG":
        #     message = '{"log": "' + msg + '"}'
        #     sys.stdout.write(struct.pack("I", len(message)))
        #     sys.stdout.write(message)
        #     sys.stdout.flush()


    def main():
        send_message("LOG", "Main -> Started native client")
        read_input()
        sys.exit(0)


    if __name__ == "__main__":
        main()
        sys.exit(0)
