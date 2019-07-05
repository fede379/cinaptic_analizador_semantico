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

USER = "cinapticserver@gmail.com"
PASS = "c1n4pt1c"
EMAIL_LIST2 = ["fedeloe379@gmail.com", "federico.loebarth@gmail.com"]
EMAIL_LIST = ["fedeloe379@gmail.com", "mkaranik@gmail.com", "mminoli@gmail.com", "lauraguilar90@gmail.com"]

class EmailSender:
    def sendMail(self, emailFrom, emailTo, info, fileToSend = None, error = False):
        msg = MIMEMultipart()
        msg["From"] = emailFrom
        msg["To"] = emailTo
        if not error:
            msg["Subject"] = "Server Info"
            msg.preamble = "Información del server: " + info            
        else:
            msg["Subject"] = "Server Error"
            msg.preamble = "Error: " + info

        if fileToSend is not None:
            ctype, encoding = mimetypes.guess_type(fileToSend)
            if ctype is None or encoding is not None:
                ctype = "application/octet-stream"

            maintype, subtype = ctype.split("/", 1)

            if maintype == "text":
                fp = open(fileToSend)
                # Note: we should handle calculating the charset
                attachment = MIMEText(fp.read(), _subtype=subtype)
                fp.close()
            elif maintype == "image":
                fp = open(fileToSend, "rb")
                attachment = MIMEImage(fp.read(), _subtype=subtype)
                fp.close()
            elif maintype == "audio":
                fp = open(fileToSend, "rb")
                attachment = MIMEAudio(fp.read(), _subtype=subtype)
                fp.close()
            else:
                fp = open(fileToSend, "rb")
                attachment = MIMEBase(maintype, subtype)
                attachment.set_payload(fp.read())
                fp.close()
                encoders.encode_base64(attachment)
            attachment.add_header("Content-Disposition", "attachment", filename=fileToSend)
            msg.attach(attachment)

        server = smtplib.SMTP("smtp.gmail.com:587")
        server.starttls()
        server.login(USER, PASS)
        server.sendmail(emailFrom, emailTo, msg.as_string())
        server.quit()

    def sendMailToAll(self, info, fileToSend = None, error = False):
        try:
            for email in EMAIL_LIST2:
                self.sendMail(USER, email, info, fileToSend, False)
                logger.info("Email sent to: " + email)
        except Exception as err:
            self.sendMail(USER, EMAIL_LIST[0], "Error en el servicio de emails", None, True)
            logger.error(err)

mail = EmailSender()
mail.sendMailToAll("test")