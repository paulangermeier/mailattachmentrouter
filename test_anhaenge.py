"""Tests für R17 (filter_archivable_attachments) gegen Outlook-Fixtures.

Fixtures
--------
Die Testmails liegen im Outlook-Ordner config.FISTURE_FOLDER_NAME
(neben "Gesendete Elemente", im eigenen Postfach). Der Ordner darf nicht
verändert werden, denn die definierten Sollwerte unten hängen von seinem
Inhalt ab.

Erzeugung: Mail an sich selbst schicken, die Kopie aus "Gesendete Elemente"
in den Fixture-Ordner verschieben, die Kopie im Posteingang löschen.
Gefunden werden die Mails über das Betreff-Präfix, nicht über die Position;
Dafür wurde die Hilfsfunktion find_test_mail definiert.

    FX01 1 PDF angehängt + 1 Bild in den Text eingefügt
    FX02 nur 1 Bild in den Text eingefügt, kein Dateianhang
    FX03 nur Text, keine Anhänge
    FX04 2 verschiedene PDFs angehängt
    FX05 2 Dateien mit gleichem Namen, unterschiedlicher Inhalt - Stichwort
         späterer Überschreibungsschutz
    FX06 Antwort auf eine externe Mail mit Logos im zitierten Verlauf
         + 1 PDF angehängt (realistischer Hauptfall für eingebettete Bilder)

Sicherheit: Alle Betreffe beginnen mit "FX", damit R2 sie aussortiert und 
sie auch bei einem Lauf mit Ziel Projekt-Laufwerk nie dort abgelegt werden.
"""

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