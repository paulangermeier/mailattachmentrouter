PROPERTY_CONTENT_ID = 'http://schemas.microsoft.com/mapi/proptag/0x3712001F'

def filter_archivable_attachments(attachments):
    """Liefert aus allen Anhängen einer Mail nur die echten Anhänge zurück (R17).

    Eingebettete Anhänge (Bilder im Text, Logos aus Mailverlauf) werden aussortiert.

    Erwartet die Attachments-Collection einer Outlook-Mail (MailItem.Attachments).
    Annahme: Bei einem echten Anhang liefert die Content-ID einen leeren String ('').

    Zurückgegeben wird die Liste der echten Attachment-Objekte, also nicht die Dateinamen. 
    Wenn kein echter Anhang vorhanden ist, wird eine leere Liste zurückgegeben.
    Die Reaktion auf die leere Liste (R18) liegt im Hauptprogramm. 

    Bekannte Risiken: 
        - Weitergeleitete Anhänge aus fremden Mailprogrammen können Content-IDs mitbringen.
          Diese werden dann ohne Meldung übersprungen.
        - Eingefügte Screenshots werden bewusst nicht archiviert.
    """
    archivable_attachments = []
    for attachment in attachments:
        if attachment.PropertyAccessor.GetProperty(PROPERTY_CONTENT_ID) == '':
            archivable_attachments.append(attachment)
    return archivable_attachments