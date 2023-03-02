from io import BytesIO
import quopri
from bs4 import BeautifulSoup
from datetime import date

names = []
nums = []
encoded_names = []
text_for_write = {}


def main():
    today = date.today()
    vcf_file = 'YourContacts.vcf'

    cont()
    encode()
    make_vcard()

    write_vcard(vcf_file, text_for_write)


def cont():
    with open("./lists/contacts.html", "rb") as tele_contacts:
        to_utf8 = tele_contacts.read().decode('utf-8', 'ignore')

    contacts_beauti = BeautifulSoup(to_utf8, "html.parser")

    name = contacts_beauti.find_all("div", attrs={"class": "name bold"})
    global names
    for i in name:
        names.append(i.text.strip())


    num = contacts_beauti.find_all("div", attrs={"details_entry details"})
    global nums
    for j in num:
        nums.append(j.text.strip())


def encode():
    global names
    for i in names:
        outputfile = BytesIO()
        inputfile = BytesIO(i.encode('utf-8'))
        quopri.encode(inputfile, outputfile, quotetabs=False)

        language_encoded = outputfile.getvalue().decode()
        print(language_encoded)

        global encoded_names
        encoded_names.append(language_encoded)


def make_vcard():
    global encoded_names
    global nums
    global text_for_write

    for i in range(0, len(names)):
        text_for_write[i] = [
            'BEGIN:VCARD',
            'VERSION:2.1',
            f'N;CHARSET=UTF-8;ENCODING=QUOTED-'
            f'PRINTABLE:;{encoded_names[i]};;;',
            f'FN;CHARSET=UTF-8;ENCODING=QUOTED-'
            f'PRINTABLE:{encoded_names[i]}',
            f'TEL;WORK;VOICE:{nums[i]}',
            f'REV:1',
            'END:VCARD'
        ]


def write_vcard(f, text_for_write):
    with open(f, 'w') as f:
        for i in range(0, len(text_for_write)):
            f.writelines([l + '\n' for l in text_for_write[i]])


if __name__ == "__main__":
    main()