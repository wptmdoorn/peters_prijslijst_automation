from nicegui import ui
from generate_pdf import generate_custom
from templates.peters_heesch.parser import get_product_information

# import the necessary components first
import smtplib
import imaplib
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage

port = 465
smtp_server = "smtp.strato.com"
login = "info@pydoorn.nl"  # paste your login generated by Mailtrap
password = "giMrin-sihja6-cemhep"  # paste your password generated by Mailtrap

base_html = f"""
<html>
    <body>
    Beste ..., <br> <br>

    Ik ben Maikel van Doorn van PyDoorn. Samen met mijn broer, William van Doorn,
    heb ik een tool ontwikkeld die het maken van prijslijsten een stuk makkelijker maakt.
    Met onze achtergrond, hij in de software-ontwikkeling, en ik in aanhangwagen branche, weten we hoe
    tijdrovend sommige taken kunnen zijn.
    <br> <br>

    Ons eerste product, <b>Automatische Prijslijsten</b>, helpt je om binnen een halve minuut een up-to-date prijslijst te maken. Het enige wat je hoeft te doen is de link van het product op je website kopiëren, plakken op onze site, en voilà, je printklare prijslijst is klaar. Zo simpel is het echt.
    Wat kun je verwachten? <br> <br>

    <span style="color:#035F22"><b>☑Supersnel:</b></span> Je hebt in no time een nieuwe prijslijst klaar. <br>
    <span style="color:#035F22"><b>☑Eenvoudig:</b></span> Drie klikken en het is geregeld. <br>
    <span style="color:#035F22"><b>☑Flexibel:</b></span> Geen extra software, je kunt het overal gebruiken! <br> <br>

    We bieden je aan om het zelf <b>gratis te proberen</b> voor de eerste 20 prijslijsten.
    Zo kun je zelf zien hoe handig onze tool is zonder dat het je iets kost. <br> <br>
    Ben je benieuwd <b>hoe het werkt</b>? Check deze video van minder dan één minuut waarin we laten zien
    hoe het werkt: <br> <br>

    <a href="https://www.youtube.com/watch?v=kUvSIjPXM3c">
        <img src="cid:image1" alt="Logo" style="height:250px;">
    </a> <br> <br>

    Heb je bepaalde wensen of een uitdaging waar je tegenaan loopt? Laat het ons weten,
    want we kunnen onze software aanpassen aan jouw behoeften. Lopen jullie tegen andere
    dingen aan? We maken ook software-oplossingen voor jullie op maat! <br> <br>

    Als dit interessant klinkt, stel ik voor een korte online demo te plannen waarin ik u onze software in actie kan laten zien

    Alvast hartelijk dank en hopelijk tot snel! <br> <br>

    Met vriendelijke groet, <br>
    Maikel van Doorn <br>
    info@pydoorn.nl <br>

    <a href="https://pydoorn.nl">
        <img src="cid:image2" alt="Logo" style="height:100px;">
    </a>
    </body>
</html>
"""


def send_mail(receiver_email: str, text: str):
    try:
        sender_email = "info@pydoorn.nl"

        message = MIMEMultipart("related")
        message["Subject"] = "Maak je eigen Prijslijst binnen 30 seconden!"
        message["From"] = sender_email
        message["To"] = receiver_email

        msgAlternative = MIMEMultipart('alternative')
        message.attach(msgAlternative)

        msgAlternative.attach(MIMEText("", "plain"))
        msgAlternative.attach(MIMEText(text, "html"))

        # convert both parts to MIMEText objects and add them to the MIMEMultipart message

        fp = open('static/demo.jpg', 'rb')
        msgImage = MIMEImage(fp.read())
        fp.close()
        msgImage.add_header('Content-ID', '<image1>')
        message.attach(msgImage)

        fp = open('static/logo 1000x400.png', 'rb')
        msgImage = MIMEImage(fp.read())
        fp.close()
        msgImage.add_header('Content-ID', '<image2>')
        message.attach(msgImage)

        # send your email
        with smtplib.SMTP_SSL("smtp.strato.com", port=port) as server:
            server.login(login, password)
            server.sendmail(
                sender_email, receiver_email, message.as_string()
            )

        imap = imaplib.IMAP4_SSL("imap.strato.com", 993)
        imap.login(login, password)
        print(imap.list())
        imap.append('Sent Items', '\\Seen', imaplib.Time2Internaldate(
            time.time()), message.as_string().encode('utf-8'))
        imap.logout()

        ui.notify(f'Mail is succesvol naar {receiver_email}!',
                  type='positive', position='center')

    except Exception as e:
        ui.notify('Er is iets fout gegaan bij het versturen van de mail!',
                  type='error', position='center')
        print(e)


def page(router) -> None:
    @ router.page('/senddemo/')
    def test_render_page():
        with ui.card().classes('items-center fixed-center').style('min-width: 700px; max-width: 800px'):
            mail = ui.input(label='Mail').classes('w-full')

            ui.label('Pas hieronder de mail aan:')
            body = ui.textarea(
                label='Tekst', value=base_html).classes('w-full')

            ui.button('Verstuur!', on_click=lambda: send_mail(
                mail.value, body.value)).classes('w-full')