import argparse
import re
import csv

# When you export a chat from Whatsapp it will be a zip file which contains a _chat.txt file
# with or without all media attachments. Exporting a chat with media attachments is an option
# in Whatsapp
WHATSAPP_EXPORTED_CHAT_TXT_NAME = '_chat.txt'
REGEXP = '\[(?P<date>\d{1,2}/\d{1,2}/\d{1,2}) [\d:]+\] (?P<participant>[\w\s]+): <attached: (?P<media_file_name>\d+-(?:PHOTO|VIDEO)[\d\w-]+\.\w+)>'

def remove_non_ascii_chars(string):
    encoded_string = string.encode("ascii", "ignore")
    return encoded_string.decode()

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument('-d', '--directory', help='Exported chat directory', required=True)
args = arg_parser.parse_args()
exported_chat_dir = args.directory

if exported_chat_dir[-1] != '/':
    exported_chat_dir += '/'

chat_txt_file = open(exported_chat_dir + WHATSAPP_EXPORTED_CHAT_TXT_NAME, 'r')

extracted_data = []

for line in chat_txt_file:
    line = remove_non_ascii_chars(line)
    match = re.search(REGEXP, line)
    if match != None:
        date = match.group('date')
        participant = match.group('participant')
        media_file_name = match.group('media_file_name')
        extracted_data.append({
            'date': date,
            'participant': participant,
            'media_file_name': media_file_name
        })
chat_txt_file.close()

csv_file = open('extracted_data.csv', 'w')
writer = csv.writer(csv_file)
writer.writerow(['Date', 'Participant', 'Media file path'])
for document in extracted_data:
    writer.writerow([document['date'], document['participant'], exported_chat_dir + document['media_file_name']])
csv_file.close()