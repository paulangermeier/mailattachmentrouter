RECIPIENT_FIELD_TO = 1 # OlMailRecipientType.olTo

# Bekommt mail_item.Recipients

def get_addresses(all_recipients):
    addresses = []
    for recipient in all_recipients:
        if recipient.Type == RECIPIENT_FIELD_TO:
            exchange_user = recipient.AddressEntry.GetExchangeUser()
            if exchange_user is not None:
                addresses.append(exchange_user.PrimarySmtpAddress)
            else:
                addresses.append(recipient.Address)
    return addresses