from anhaenge import filter_archivable_attachments
import config
import win32com.client

outlook = win32com.client.Dispatch('Outlook.Application')
namespace = outlook.GetNamespace('MAPI')
folder = namespace.Folders(config.MAILBOX_NAME).Folders(config.FIXTURE_FOLDER_NAME)
items = folder.Items

def find_test_mail(items, subject_prefix):
    for item in items:
        if item.Subject.startswith(subject_prefix):
            return item
    raise ValueError(f'Keine Testmail mit Betreff-Präfix {subject_prefix!r} gefunden.')

archivable_attachments_cases = [
    ('FX01', ['Angebot_Variante_A.pdf']),
    ('FX02', []),
    ('FX03', []),
    ('FX04', ['Lastenheft_Kaffeemaschine.pdf', 'Angebot_Variante_A.pdf']),
    ('FX05', ['Angebot.pdf', 'Angebot.pdf']),
    ('FX06', ['Angebot_Variante_B.pdf'])
]

for eingabe, sollwert in archivable_attachments_cases: 
    mail_item = find_test_mail(items, eingabe)
    attachments = filter_archivable_attachments(mail_item.Attachments)
    istwert = []
    for attachment in attachments:
        istwert.append(attachment.Filename)
    assert sorted(istwert) == sorted(sollwert), f'\n Eingabe: {eingabe!r} \n Ist: {istwert!r} \n Soll: {sollwert!r}'