import minecart
import re
import os
import sys
import pytesseract
import json
#from NumberOfPages import getPageNumber

mcq_list = []


def rmUTF(str):

    # replace UTF-8 chars with its ASCII 
    str = re.sub('\n+|\uf020','',str)
    str = re.sub('\u2013+|\u2014+','-',str)
    str = re.sub('\u2019+|\u2018+|\u201c|\u201d',"'",str)
    str = re.sub('\uf0ae+',"->",str)
    str = re.sub('\u00d7+',"x",str)

    return str

def addmqctolist(data):
    groups = re.split('Q[0-9+]+.',data)[1:]
    for group in groups:
        meta = re.split('\([abcd]\)|Ans:',group)
        question = re.sub('\n+',' ',meta[0])
        options = [re.sub('\n+',' ',option) for option in meta[1:5]]
        answer = re.sub('[\(\)]|\\n+','',re.split('Ans:',group)[-1])
        try:
            mcq_list.append(
                                {
                                    'Question':rmUTF(question),
                                    'Option_A':rmUTF(options[0]),
                                    'Option_B':rmUTF(options[1]),
                                    'Option_C':rmUTF(options[2]),
                                    'Option_D':rmUTF(options[3]),
                                    'Answer':answer
                                }
                            )
        except:
            pass

def pdftomcq(filename, num_pages):
    
    data = ''
    pdf_file = open(filename, 'rb')
    doc = minecart.Document(pdf_file)
    page = doc.get_page(num_pages)

    count = 0
    for page in doc.iter_pages():
        for i in range(len(page.images)):
            im = page.images[i].as_pil() 
            if count>=2:
                print('Parsing page ',count+1)
                data += pytesseract.image_to_string(im, lang='eng')
            count = count + 1
    return data


if __name__ == '__main__':

    filename = sys.argv[1]
    no_of_pages = sys.argv[2]

    fp = open('text_data.txt','w')
    data = pdftomcq(filename, no_of_pages)
    fp.write(data)
    fp.close()

    fp = open('text_data.txt','r')
    data = fp.read()    
    addmqctolist(data)
    fp.close()

    json_str = json.dumps(mcq_list, indent=4).encode('ascii',errors='ignore').decode('ascii')
    with open("output.json", "w") as write_file:
        write_file.write(json_str)