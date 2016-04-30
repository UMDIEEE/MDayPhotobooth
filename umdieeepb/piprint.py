import cups

def printFile(selected_frame_num, num_times):
    print(" ** Printing!")
    try:
        conn = cups.Connection()
        printers = conn.getPrinters()
        printer_name = printers.keys()[0]
        cups.setUser('pi')
        
        if selected_frame_num < 8:
            selected_frame_pic = "tmp/frame_%i.jpg" % (selected_frame_num)
        else:
            selected_frame_pic = "nice_image.jpg"
        
        for i in xrange(0, num_times):
            conn.printFile(printer_name, os.path.abspath(selected_frame_pic), "Photo_Booth_Print", { "media": "Custom.4x6in" })
    except:
        print(" ** Printing FAILED!")
