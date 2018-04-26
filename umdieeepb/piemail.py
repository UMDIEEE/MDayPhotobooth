import os
import cups
import traceback

import smtplib

from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

GMAIL_USERNAME = "ieee.umd@gmail.com"
GMAIL_PASSWORD = "EyeTripleE1617"

PIEMAIL = """Hi there!

Thank you so much for stopping by IEEE@UMD's photo booth! We
hope that you having (or had!) a great time at Maryland Day 2017,
and we hope you come back next year!

Attached is the photo you took with us today.

Thanks again!
IEEE@UMD"""

def send_email_with_img(user, pwd, recipient, subject, body, img_filename):
    img_data = open(img_filename, 'rb').read()
    msg = MIMEMultipart()  
    msg['Subject'] = subject
    msg['From'] = user
    msg['To'] = ", ".join(recipient) if type(recipient) == list else recipient

    text = MIMEText(body)
    msg.attach(text)
    image = MIMEImage(img_data, name=os.path.basename(img_filename))
    msg.attach(image)

    gmail_user = user
    gmail_pwd = pwd

    # Prepare actual message
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(user, recipient, msg.as_string())
        server.close()
        print("Successfully sent email! Sent to: %s" % msg['To'])
    except:
        print("Failed to send mail! Could not send to: %s" % msg['To'])
        traceback.print_exc()

def emailFile(selected_frame_num, email_dest):
    print(" ** Emailing!")
    try:
        if selected_frame_num < 8:
            selected_frame_pic = "tmp/frame_%i.jpg" % (selected_frame_num)
        else:
            selected_frame_pic = "nice_image.jpg"
        
        print(" ** Image is %s | fnum is %i | email_dest is %s" % (selected_frame_pic, selected_frame_num, email_dest))
        
        send_email_with_img(GMAIL_USERNAME, GMAIL_PASSWORD, email_dest,
            "IEEE@UMD Maryland Day 2017 - Your Photo!", 
            PIEMAIL, os.path.abspath(selected_frame_pic))
    except:
        print(" ** Emailing FAILED!")
        traceback.print_exc()
