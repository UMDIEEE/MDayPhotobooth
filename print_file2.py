import cups
conn = cups.Connection()
printers = conn.getPrinters()
printer_name = printers.keys()[0]
cups.setUser('pi')
conn.printFile(printer_name, "/home/pi/bigprint.jpg", "Photo_Booth_Print", { "media": "Custom.4x6in" })

