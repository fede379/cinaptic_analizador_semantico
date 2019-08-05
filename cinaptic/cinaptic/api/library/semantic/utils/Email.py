import sys
import os
import smtplib
import mimetypes
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
import logging

logger = logging.getLogger()

USER = "cinaptic.server@frre.utn.edu.ar"
PASS = "c1n4pt1c"
EMAIL_LIST = ["fedeloe379@gmail.com", "federico.loebarth@gmail.com"]
# EMAIL_LIST = ["fedeloe379@gmail.com", "mkaranik@gmail.com", "mminoli@gmail.com", "laura.aguilar90@gmail.com"]

class EmailSender:
    def sendMail(self, emailFrom, emailTo, info = '', filesToSend = [], error = False):
        msg = MIMEMultipart()
        msg["From"] = emailFrom
        msg["To"] = emailTo
        if not error:
            msg["Subject"] = "Server Info"                        
        else:
            msg["Subject"] = "Server Error"

        msg.attach(MIMEText(info, 'plain'))

        if filesToSend is not None:
            for file in filesToSend:
                try:
                    print(file)
                    with open(file, 'rb') as fp:
                        attachment = MIMEBase('application', "octet-stream")
                        attachment.set_payload(fp.read())
                    encoders.encode_base64(attachment)
                    attachment.add_header('Content-Disposition', 'attachment', filename=os.path.basename(file))
                    msg.attach(attachment)
                except:
                    logger.error(f"Unable to open one of the attachments. Error: {sys.exc_info()[0]}")
                    print("Unable to open one of the attachments. Error: ", sys.exc_info()[0])
                    pass

        try:
            with smtplib.SMTP('mail.frre.utn.edu.ar', 587) as s:
                s.ehlo()
                s.starttls()
                s.ehlo()
                s.login(USER, PASS)
                s.sendmail(emailFrom, emailTo, msg.as_string())
                s.close()
            print("Email sent to >", emailTo)
            logger.info(f"Email sent to > {emailTo}")
        except:
            print("Unable to send the email. Error:", sys.exc_info()[0])
            logger.error(f"Unable to send the email. Error: {sys.exc_info()[0]}")
            pass

    def sendMailToAll(self, info, filesToSend = [], error = False):
        try:
            files = list(map(lambda x: os.path.abspath(x), filesToSend))
            for email in EMAIL_LIST:
                self.sendMail(emailFrom=USER, emailTo=email, info=info, filesToSend=files, error=False)                
        except Exception as err:
            self.sendMailToAdmin("Error en el servicio de emails > {0}".format(err))
            print(err)
            logger.error(err)

    def sendMailToAdmin(self, info):
        self.sendMail(emailFrom=USER, emailTo=EMAIL_LIST[0], info=info, filesToSend=None, error=True)

# mail = EmailSender()
# files = ["results/Pesticide/Betweenness_idGraph_Pesticide_relation_BROADER.csv"]
# mail.sendMailToAll(info="test", filesToSend=files)