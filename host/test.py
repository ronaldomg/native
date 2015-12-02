import win32print
printer = win32print.OpenPrinter('Argox')  # connect to the selected printer
win32print.StartDocPrinter(printer, 1, ('teste', None, "RAW"))
win32print.StartPagePrinter(printer)
win32print.WritePrinter(printer,"n\nL\nD8\n121100200200100nome ACESSORIO\n1211001007005501578\n121100101100100R$\n12110010110014039,94\n1E3052000008504807909206234109\nQ0001\nE\n")
win32print.EndPagePrinter(printer)
win32print.EndDocPrinter(printer)
win32print.ClosePrinter(printer)
