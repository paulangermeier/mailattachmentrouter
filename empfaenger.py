RECIPIENT_FIELD_TO = 1 # OlMailRecipientType.olTo

# Bekommt mail_item.Recipients

def get_addresses(all_recipients):
    """Erwartet Recipients-Collection des Mailitems (COM-Objekt).

    Zurückgegeben wird eine Liste von Adress-Strings. Es handelt sich
    um eine Liste von Rohdaten die nicht normalisiert werden.

    Berücksichtigt werden nach R9 nur Empfänger aus dem An-Feld,
    CC/BCC wird ignoriert.
    Nach R10.1 ist eine Weiche eingebaut, die Exchange-User identifiziert
    und den Adress-String über PrimarySmtpAddress zurückgibt. Bei nicht
    Exchange-Usern wird der Adress-String über Recipient.Address zurückgegeben.

    Im Falle eines Mailitems, das ein leeres An-Feld hat, wird eine leere Liste
    zurückgegeben.
    """
    addresses = []
    for recipient in all_recipients:
        if recipient.Type == RECIPIENT_FIELD_TO:
            exchange_user = recipient.AddressEntry.GetExchangeUser()
            if exchange_user is not None:
                addresses.append(exchange_user.PrimarySmtpAddress)
            else:
                addresses.append(recipient.Address)
    return addresses