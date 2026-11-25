import config
import win32com.client

outlook = win32com.client.Dispatch('Outlook.Application')
namespace = outlook.GetNamespace('MAPI')
folder = namespace.Folders(config.MAILBOX_NAME).Folders(config.FIXTURE_FOLDER_NAME)
items = folder.Items

item = []
attachments = []
recipients = []

for i in range(1, 11):
    item.append({
        'number': str(i), 
        'subject': items.Item(i).Subject,
        'attachmentcount': str(items.Item(i).Attachments.Count)
        })
    for recipient in items.Item(i).Recipients:
        exchange_user = recipient.AddressEntry.GetExchangeUser()
        if exchange_user is not None: 
            exchange_user_smtp = exchange_user.PrimarySmtpAddress
        else: 
            exchange_user_smtp = 'Kein Exchange-User'
        recipients.append({
            'number': str(i),
            'recipienttype': recipient.Type,
            'resolved': recipient.Resolved,
            'recipientaddress': recipient.Address,
            'recipientname': recipient.Name,
            'recipientaddressentrytype': recipient.AddressEntry.Type,
            'addressentryusertype': recipient.AddressEntry.AddressEntryUserType,
            'primarysmtpaddress': exchange_user_smtp
        })
    for attachment in items.Item(i).Attachments: 
        attachments.append({
            'number': str(i),
            'name': attachment.Filename,
            'size': attachment.Size,
            'content_id': attachment.PropertyAccessor.GetProperty('http://schemas.microsoft.com/mapi/proptag/0x3712001F')
        })
    

for i in item:
    print(i['number'] + ' | ' + i['subject'] + ' | ' + i['attachmentcount'])
    print('Empfänger')
    for recipient in recipients:
        if i['number'] == recipient['number']:
            print(recipient['number'] + ' | ' + str(recipient['recipienttype']) + ' | ' +  str(recipient['resolved']) + ' | ' + str(recipient['recipientaddress']) + ' | ' + str(recipient['recipientname']) + ' | ' + str(recipient['recipientaddressentrytype']) + ' | ' + str(recipient['addressentryusertype']) + ' | ' + str(recipient['primarysmtpaddress']))
    print('Anhänge')
    for attachment in attachments:
        if i['number'] == attachment['number']:
            print(attachment['number'] + ' | ' + str(attachment['name']) + ' | ' + str(attachment['size']) + ' | ' + repr(attachment['content_id']))
    print('___________________')

