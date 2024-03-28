# https://sowmiyak.medium.com/file-translation-with-google-translate-api-in-python-210446800543
# https://thepythoncode.com/article/translate-text-in-python
# translate text using google translate api
 
from googletrans import Translator
from pprint import pprint

translator = Translator()

with open('result/stt-spa.txt', 'r+') as f:
    contents = f.read()
    print(contents)

    result = translator.translate(contents, dest='en')
    #print(result)
    #print(result.text)
    m = open('result/translated-text.txt', 'w')
    m.write(str(result.text))