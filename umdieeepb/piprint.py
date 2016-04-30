import cups
import traceback

def printFile(selected_frame_num, num_times):
    print(" ** Printing!")
    try:
        conn = cups.Connection()
        printers = conn.getPrinters()
        printer_name = list(printers.keys())[0]
        cups.setUser('pi')
        
        if selected_frame_num < 8:
            selected_frame_pic = "tmp/frame_%i.jpg" % (selected_frame_num)
        else:
            selected_frame_pic = "nice_image.jpg"
        
        print(" ** Image is %s | fnum is %i | num_times is %i" % (selected_frame_pic, selected_frame_num, num_times))
        
        for i in range(0, num_times):
            print(" ** Printing iteration!")
            conn.printFile(printer_name, os.path.abspath(selected_frame_pic), "Photo_Booth_Print", { "media": "Custom.4x6in" })
    except:
        print(" ** Printing FAILED!")
        traceback.print_exc()
