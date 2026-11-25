from empfaenger import get_addresses
from testhilfen import find_test_mail
import config
import win32com.client

outlook = win32com.client.Dispatch('Outlook.Application')
namespace = outlook.GetNamespace('MAPI')
folder = namespace.Folders(config.MAILBOX_NAME).Folders(config.FIXTURE_FOLDER_NAME)
items = folder.Items

address_cases = [
    ('FX07', ['Paul.Angermeier@tga-consulting.ag', 'max.mustermann@example.com', 'huber@sanitaer.example']),
    ('FX08', ['Paul.Angermeier@tga-consulting.ag', 'maximiliane.musterfrau@example.com']),
    ('FX09', ['Paul.Angermeier@tga-consulting.ag', 'maier@rlt-maier.example']),
    ('FX10', ['maier@rlt-maier.example'])
]

for eingabe, sollwert in address_cases: 
    mail_item = find_test_mail(items, eingabe)
    istwert = get_addresses(mail_item.Recipients)
    assert sorted(istwert) == sorted(sollwert), f'\n Eingabe: {eingabe!r} \n Ist: {istwert!r} \n Soll: {sollwert!r}'