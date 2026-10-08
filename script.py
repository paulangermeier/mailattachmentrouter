from datetime import datetime
import config
import os
import string
import win32com.client

def subject_cleaner(subject):
    erlaubte_zeichen = string.ascii_letters + string.digits + " -+_"
    clean_subject = ""

    for char in subject:
        if char in erlaubte_zeichen:
            clean_subject += char

    clean_subject = clean_subject[:30]
    clean_subject = clean_subject.strip()
    clean_subject = clean_subject.replace(" ", "_")

    if len(clean_subject) == 0:
        clean_subject = "kein_betreff"
    
    return clean_subject

outlook = win32com.client.Dispatch("Outlook.Application")
namespace = outlook.GetNamespace("MAPI")
folder = namespace.GetDefaultFolder(config.OL_FOLDER_SENT_MAIL)
items = folder.Items
item = items.Item(1)

if item.Attachments.Count == 0:
    print("Keine Anhänge vorhanden.")
else: 
    date = item.SentOn.strftime("%y%m%d")
    subject = subject_cleaner(item.Subject)
    ordnername = date + "_" + subject

    vollpfad = os.path.join(config.ZIELORDNER, ordnername)

    os.mkdir(vollpfad, exist_ok=True)

    attachment = item.Attachments.Item(1)
    filename = attachment.FileName

    vollpfad = os.path.join(vollpfad, filename)
    attachment.SaveAsFile(vollpfad)




