import config
import win32com.client

outlook = win32com.client.Dispatch('Outlook.Application')
namespace = outlook.GetNamespace('MAPI')
folder = namespace.Folders(config.MAILBOX_NAME).Folders(config.FIXTURE_FOLDER_NAME)
items = folder.Items

item = []
attachments = []

for i in range(1, 7):
    item.append({
        'number': str(i), 
        'subject': items.Item(i).Subject,
        'attachmentcount': str(items.Item(i).Attachments.Count)
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
    for attachment in attachments:
        if i['number'] == attachment['number']:
            print(attachment['number'] + ' | ' + str(attachment['name']) + ' | ' + str(attachment['size']) + ' | ' + repr(attachment['content_id']))
    print('___________________')