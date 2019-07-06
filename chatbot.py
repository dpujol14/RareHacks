#telegram api
from telegram.ext import Updater
from telegram.ext import MessageHandler, Filters

#nltk
import nltk
import numpy as np
import random
import string # to process standard python strings
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk import pos_tag
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from textblob import TextBlob

# ******************************************************************
# GREETINGS
GREETING_INPUTS = ("hello", "hi", "greetings", "sup", "what's up","hey",)
GREETING_RESPONSES = ["hi", "hey", "*nods*", "hi there", "hello", "I am glad! You are talking to me"]

def greeting(sentence):
    """If user's input is a greeting, return a greeting response"""
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            return random.choice(GREETING_RESPONSES)



# ******************************************************************
#TREAT THE INPUT

#LEMMATIZATION
remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)	#remove punctuation

#funtion to lemmatize a sentance
lemmer = WordNetLemmatizer()	#this is an internal dictionary
def lemmatize(p):
    if p[1][0] in {'N','V'}:
        return lemmer.lemmatize(p[0].lower(), pos=p[1][0].lower())
    return p[0]

#STOPWORDS
def removeStopWords(sentance):
    words = word_tokenize(sentance)
    filtered_words = [word for word in words if word not in stopwords.words('english')]
    return filtered_words

#CORRECCIO
def correccio(text):
    s = TextBlob(text)
    return s.correct()

def extractSintagma (text):
    pairs = pos_tag(text)
    grammar = "NP: {<DT>?<JJ>*<NN>}"
    cp = nltk.RegexpParser(grammar)
    result = cp.parse(pairs)
    return result

def treatInput(sentence):
    sentence = str(correccio(sentence.lower()))
    sentence = sentence.lower().translate(remove_punct_dict)    #eliminem els punts
    aux = removeStopWords(sentence)
    pairs = pos_tag(aux)
    result = [lemmatize(p) for p in pairs]
    result = extractSintagma(result)
    return result

# ******************************************************************

from googletrans import Translator

def tr2english(text):
    translator = Translator()
    msg_tr = translator.translate(text).text
    global language
    language = translator.detect(text).lang
    return msg_tr

def tr2other(text):
    print(text)
    translator = Translator()
    print(language)
    msg_tr = translator.translate(text, dest=str(language)).text
    print(msg_tr)
    return msg_tr

# ******************************************************************


#function to be called
def responde(bot, update):
    user_response = tr2english(update.message.text)

    if (user_response != 'bye' or user_response != 'Bye'):
            if (user_response == 'thanks' or user_response == 'thank you'):
                bot.send_message(chat_id=update.message.chat_id, text="You are very welcome")

            else:
                if (greeting(user_response) != None):
                    bot.send_message(chat_id=update.message.chat_id, text=greeting(user_response))
                else:
                    aux = treatInput(user_response)
                    bot.send_message(chat_id = update.message.chat_id, text=aux)
    else:
            bot.send_message(chat_id = update.message.chat_id, text="Goodbye!!")


# ******************************************************************


def radians(c):
    return pi/180 * c

def distancia(acte, bici):
    lat1 = radians(float(acte.lat))
    long1 = radians(float(acte.long))
    lat2 = radians(float(bici.lat))
    long2 = radians(float(bici.long))
    lat = abs(lat2-lat1)
    long = abs(long2-long1)
    a = sin(lat/2)**2+cos(lat1)*cos(lat2)*sin(long/2)**2
    c = 2*atan2(sqrt(a),sqrt(1-a))
    return R*c






# *********************************************************************


tipus = [
'Uveal melanoma',
'Diffuse leptomeningeal melanocytosis',
'Familial atypical multiple mole melanoma syndrome',
'Familial melanoma',
'Malignant melanoma of the mucosa',
'Melanoma and neural system tumor syndrome',
'Melanoma of soft tissue',
'Primary melanoma of the central nervous system'
]

sinonims = [
    ['choroidal melanoma' ,'iris melanoma','Intraocular melanoma'],
    ['DLM Leptomeningeal melanomatosis'],
    ['B-K mole syndrome',
    'FAMM-PC syndrome',
    'FAMMM syndrome',
    'Familial Clark nevus syndrome',
    'Familial atypical mole syndrome',
    'Familial atypical multiple mole melanoma-pancreatic carcinoma syndrome',
    'Familial dysplastic nevus syndrome',
    'Melanoma-pancreatic cancer syndrome'],
    ['Dysplastic nevus syndrome hereditary','B-K mole syndrome'],
    [],
    ['Melanoma-astrocytoma syndrome'],
    ['Clear cell sarcoma of the tendons and aponeuroses'],
    ['Malignant melanoma of meninges','Primary melanoma of the CNS']
    ]

dic = dict(zip(tipus,sinonims))
tipus_melanomes = tipus + [item for sublist in sinonims for item in sublist]



print(dic)
print(tipus_melanomes)

#load the access token
TOKEN = open('token.txt').read().strip()

updater = Updater(token= TOKEN)
dispatcher = updater.dispatcher

#handling the call
dispatcher.add_handler(MessageHandler(Filters.text, responde, pass_user_data=True))

#starting the bot
updater.start_polling()





