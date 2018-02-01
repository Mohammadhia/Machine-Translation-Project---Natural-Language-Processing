#Dictionary of spanish words from dev set and word-to-word translations (using google translate)
dictionary = {'The': 'The', 'Colbert': 'Colbert', 'Report': 'Report', 'es': 'is', 'un': 'a', 'programa': 'Program', 'de': 'from', 'entrevistas': 'interviews', 'nocturnas': 'nocturnal', 'y': 'and', 'sÃ¡tira': 'satire', 'polÃ\xadtica': 'political', 'estadounidense': 'American', 'presentado': 'presented', 'por': 'by', 'Stephen': 'Stephen', 'que': 'what', 'se': 'HE', 'emitÃ\xada': 'emitted', '4': '4', 'dÃ\xadas': 'days', 'a': 'a', 'la': 'the', 'semana': 'week', 'en': 'in', 'Comedy': 'Comedy', 'Central': 'Central', 'desde': 'since', 'el': 'he', '17': '17', 'octubre': 'October', '2005': '2005', 'al': 'to', '18': '18', 'noviembre': 'November', '2014': '2014', 'contando': 'counting', 'con': 'with', '1447': '1447', 'episodios': 'episodes', '.': '.', 'El': 'He', 'centraba': 'centered', 'reportero': 'reporter', 'ficticio': 'fictional', 'llamado': 'called', '"': '"', ',': ',', 'interpretado': 'interpreted', 'presentador': 'presenter', 'del': 'of the', 'mismo': 'same', 'nombre': 'first name', 'personaje': 'character', 'descrito': 'described', 'como': 'as', 'bien': 'good', 'intencionado': 'deliberate', 'poco': 'little bit', 'informado': 'informed', 'idiota': 'idiot', 'alto': 'alto', 'status': 'status', 'una': 'a', 'caricatura': 'cartoon', 'los': 'the', 'expertos': 'Experts', 'polÃ\xadticos': 'political', 'televisiÃ³n': 'television', 'AdemÃ¡s': 'besides', 'satirizaba': 'satirizaba', 'programas': 'programs', 'opiniÃ³n': 'opinion', 'conservadores': 'conservatives', 'mÃ¡s': 'more', 'concretamente': 'specifically', "O'Reilly": "O'Reilly", 'Factor': 'Factor', 'emitido': 'issued', 'Fox': 'Fox', 'News': 'News', 'spin-off': 'spin-off', 'Daily': 'Daily', 'Show': 'Show', 'donde': 'where', 'tambiÃ©n': 'also', 'actuÃ³': 'acted', 'corresponsal': 'correspondent', 'durante': 'during', 'varios': 'various', 'aÃ±os': 'years', 'mientras': 'While', 'desarrollaba': 'I was developing', 'naciÃ³': 'was born', 'Washington': 'Washington', 'D.C.': 'D.C.', 'joven': 'young', '11': '11', 'hermanos': 'brothers', 'seno': 'otherwise', 'familia': 'family', 'catÃ³lica': 'catholic', 'CreciÃ³': 'He grew up', 'James': 'James', 'Island': 'Island', 'Charleston': 'Charleston', 'Carolina': 'Carolina', 'Sur': 'Sure', 'Su': 'his', 'padre': 'father', 'William': 'William', 'Jr.': 'Jr.', 'era': 'era', 'doctor': 'doctor', 'decano': 'dean', 'escuela': 'school', 'medicina': 'medicine', 'Universidad': 'college', 'Yale': 'Yale', 'San': 'San', 'Luis': 'Luis', 'finalmente': 'Finally', 'sirviÃ³': 'it served', 'vicepresidente': 'vice president', 'asuntos': 'affairs', 'acadÃ©micos': 'academics', 'madre': 'mother', 'Lorna': 'Lorna', 'Elizabeth': 'Elizabeth', 'ama': 'but', 'casa': 'home', 'En': 'In', 'ha': 'he has', 'sus': 'their', 'padres': 'parents', 'personas': 'people', 'devotas': 'devotees', 'pero': 'but', 'valoraban': 'they valued', 'fuertemente': 'strongly', 'intelectualismo': 'intelectualismo', 'le': 'the', 'enseÃ±aron': 'they taught', 'hijos': 'children', 'posible': 'possible', 'cuestionar': 'question', 'iglesia': 'church', 'seguir': 'follow', 'siendo': 'being', 'catÃ³licos': 'catholic'}
lowercaseDictionary = {}
for k, v in dictionary.items():
    lowercaseDictionary[k[0].lower()+k[1:]] = v.lower() #Make only the first character lowercase for spanish (escape sequences need to stay the same) and make all characters lowercase in english

#from googletrans import Translator #INSTALLED USING PIP; NOT IN PYTHON BY DEFAULT!!!!!
dev_spanish_sentences = []
dev_english_sentences = []

f = open("dev.es")
for line in iter(f): #Iterates through each line in spanish dev set
    words = line.split()
    words = [x[0].lower()+x[1:] for x in words] #Make only the first character lowercase for spanish
    dev_spanish_sentences.append(words)
f.close()

g = open("dev.en")
for line in iter(g): #Iterates through each line in english dev set
    words = line.split()
    words = [x.lower() for x in words] #Makes english words lowercase
    dev_english_sentences.append(words)
g.close()


#################### DEV SET RESULTS
print("DEV SET RESULTS")
########################## Without pre- or post-processing strategies applied ############################################
generatedEnglish = []
for sentence in dev_spanish_sentences:
    tempList = []
    for word in sentence:
        tempList.append(lowercaseDictionary[word]) #Appends direct translation of word from spanish dev set
    generatedEnglish.append(tempList)


copyOfDevEnglish = dev_english_sentences #Copies english dev set
accuracyList = []
for i in range(len(generatedEnglish)):
    tempAccuracy = 0
    for j in range(len(generatedEnglish[i])):
        if(generatedEnglish[i][j] in copyOfDevEnglish[i]): #If the generated word is in the target sentence
            tempAccuracy += 1
            copyOfDevEnglish[i].remove(generatedEnglish[i][j]) #Caps the unigram accuracy in the reference/target sentence
    tempAccuracy /= len(generatedEnglish[i]) ################STILL DON'T KNOW HOW TO TAKE INTO ACCOUNT ALIGNMENT IN MEASURING ACCURACY FOR PART 1. Just using unigram precision right now (and capping at number of words in reference)
    accuracyList.append(tempAccuracy)

print("Baseline: ", accuracyList)


###################### STRATEGY 1 - Lemmatize generated words ##########################
import nltk
lemma = nltk.wordnet.WordNetLemmatizer()

generatedEnglish = []
for sentence in dev_spanish_sentences:
    tempList = []
    for word in sentence:
        tempList.append(  lemma.lemmatize(lowercaseDictionary[word])  )  #Lemmatizes generated words
    generatedEnglish.append(tempList)

copyOfDevEnglish = dev_english_sentences
accuracyList = []
for i in range(len(generatedEnglish)):
    tempAccuracy = 0
    for j in range(len(generatedEnglish[i])):
        if(generatedEnglish[i][j] in copyOfDevEnglish[i]): #If the generated word is in the target sentence
            tempAccuracy += 1
            copyOfDevEnglish[i].remove(generatedEnglish[i][j])
    tempAccuracy /= len(generatedEnglish[i]) ################STILL DON'T KNOW HOW TO TAKE INTO ACCOUNT ALIGNMENT IN MEASURING ACCURACY FOR PART 1. Just using unigram precision right now (and capping at number of words in reference)
    accuracyList.append(tempAccuracy)

print("Strategy 1: ", accuracyList) #CONCLUSION: EVERYTHING IS WORSE!!!


################### STRATEGY 2 - Part of Speech (Add verbs only if noun will precede it) #######################
import nltk

generatedEnglish = []
for sentence in dev_spanish_sentences:
    tempList = []
    for word in sentence:
        try:
            partOfSpeech = nltk.tag.pos_tag([word]) #Gets part of speech of current word
            if(partOfSpeech[0][1][0] == "V"):  # If it's a verb
                for k in range(len(tempList)):
                    if (nltk.tag.pos_tag(tempList[k])[0][1][0] == "N"):  # Only adds verb if a noun precedes it
                        tempList.append(lowercaseDictionary[word])
                        break
            else:
                tempList.append(lowercaseDictionary[word])
        except:
            tempList.append(lowercaseDictionary[word]) #Simply appends direct translation if all else fails
    generatedEnglish.append(tempList)

copyOfDevEnglish = dev_english_sentences #Copies english dev set
accuracyList = []
for i in range(len(generatedEnglish)):
    tempAccuracy = 0
    for j in range(len(generatedEnglish[i])):
        if(generatedEnglish[i][j] in copyOfDevEnglish[i]): #If current word is in target english sentence
            tempAccuracy += 1
            copyOfDevEnglish[i].remove(generatedEnglish[i][j])
    tempAccuracy /= len(generatedEnglish[i]) ################STILL DON'T KNOW HOW TO TAKE INTO ACCOUNT ALIGNMENT IN MEASURING ACCURACY FOR PART 1. Just using unigram precision right now (and capping at number of words in reference)
    accuracyList.append(tempAccuracy)

print("Strategy 2: ", accuracyList) #CONCLUSION: EVERYTHING IS WORSE (0 percent accuracy on all)!!!


################### STRATEGY 3 - Stemming (Use Snowball stemmer on words) ##################################
from nltk.stem.snowball import SnowballStemmer
stemmer = SnowballStemmer("english")

generatedEnglish = []
for sentence in dev_spanish_sentences:
    tempList = []
    for word in sentence:
        tempList.append( stemmer.stem(lowercaseDictionary[word])  )  #Stemmer version of generated words
    generatedEnglish.append(tempList)

copyOfDevEnglish = dev_english_sentences
accuracyList = []
for i in range(len(generatedEnglish)):
    tempAccuracy = 0
    for j in range(len(generatedEnglish[i])):
        if(generatedEnglish[i][j] in copyOfDevEnglish[i]): #If current word is in target english sentence
            tempAccuracy += 1
            copyOfDevEnglish[i].remove(generatedEnglish[i][j])
    tempAccuracy /= len(generatedEnglish[i]) ################STILL DON'T KNOW HOW TO TAKE INTO ACCOUNT ALIGNMENT IN MEASURING ACCURACY FOR PART 1. Just using unigram precision right now (and capping at number of words in reference)
    accuracyList.append(tempAccuracy)

print("Strategy 3: ", accuracyList) #CONCLUSION: EVERYTHING IS WORSE (0 percent accuracy on all but last sentence (2.71%))!!!


###################### STRATEGY 4 - Use a tokenizer ##############################################
from nltk.tokenize.moses import MosesTokenizer
tokenizer = MosesTokenizer()

generatedEnglish = []
for sentence in dev_spanish_sentences:
    tempList = []
    for word in sentence:
        tempList.append(  lowercaseDictionary[word]  )  #Appends generated words
    tempSentence = " ".join(tempList) #Joins into a sentence
    tempSentence = tokenizer.tokenize(tempSentence) #Tokenizes again using Moses tokenizer

    generatedEnglish.append(tempSentence) #Appends to generated list

copyOfDevEnglish = dev_english_sentences
accuracyList = []
for i in range(len(generatedEnglish)):
    tempAccuracy = 0
    for j in range(len(generatedEnglish[i])):
        if(generatedEnglish[i][j] in copyOfDevEnglish[i]): #If current word is in target english sentence
            tempAccuracy += 1
            copyOfDevEnglish[i].remove(generatedEnglish[i][j])
    tempAccuracy /= len(generatedEnglish[i]) ################STILL DON'T KNOW HOW TO TAKE INTO ACCOUNT ALIGNMENT IN MEASURING ACCURACY FOR PART 1. Just using unigram precision right now (and capping at number of words in reference)
    accuracyList.append(tempAccuracy)

print("Strategy 4: ", accuracyList) #CONCLUSION: EVERYTHING IS STILL WORSE THAN BASELINE!!!


##################### STRATEGY 5 - WSD (see if one of the meanings of a generated word is in the target sentence) ########################
import nltk
from nltk.corpus import wordnet as wn

generatedEnglish = []
for sentence in dev_spanish_sentences:
    tempList = []
    for word in sentence:
        tempList.append(  lowercaseDictionary[word]  )  #Appends generated words
    generatedEnglish.append(tempList)

copyOfDevEnglish = dev_english_sentences
accuracyList = []
for i in range(len(generatedEnglish)):
    tempAccuracy = 0
    for j in range(len(generatedEnglish[i])):
        if(generatedEnglish[i][j] not in copyOfDevEnglish[i]): #If current word is NOT in target english sentence
            tempSynonymSet = []
            for ss in wn.synsets(generatedEnglish[i][j]): #Find all meanings of current word
                tempSynonymSet.append(ss.definition())
            for z in range(len(copyOfDevEnglish[i])): #Find all meanings of each word in target sentence
                tempTargetWord = copyOfDevEnglish[i][z]
                tempTargetWordSynonymSet = []
                for m in wn.synsets(tempTargetWord):
                    tempTargetWordSynonymSet.append(m.definition())

                for k in range(len(tempSynonymSet)):
                    if(tempSynonymSet[k] in tempTargetWordSynonymSet): #If there is a match between any 2 meanings, increase accuracy count by 1
                        tempAccuracy += 1
                        break
        elif(generatedEnglish[i][j] in copyOfDevEnglish[i]): #If current word is in target english sentence
            tempAccuracy += 1
            copyOfDevEnglish[i].remove(generatedEnglish[i][j])
    tempAccuracy /= len(generatedEnglish[i]) ################STILL DON'T KNOW HOW TO TAKE INTO ACCOUNT ALIGNMENT IN MEASURING ACCURACY FOR PART 1. Just using unigram precision right now (and capping at number of words in reference)
    accuracyList.append(tempAccuracy)

print("Strategy 5: ", accuracyList) #CONCLUSION: EVERYTHING IS WORSE!!!


######################## STRATEGY 6 - Producing all synonyms of a word not in the target sentence and seeing if any of those are ##################################
from nltk.corpus import wordnet
import nltk

generatedEnglish = []
for sentence in dev_spanish_sentences:
    tempList = []
    for word in sentence:
        tempList.append(lowercaseDictionary[word]) #Appends directly translated word
    generatedEnglish.append(tempList)

copyOfDevEnglish = dev_english_sentences #Copies text from english dev set
accuracyList = []
for i in range(len(generatedEnglish)):
    tempAccuracy = 0
    for j in range(len(generatedEnglish[i])):
        if(generatedEnglish[i][j] in copyOfDevEnglish[i]): #If current word is in target english sentence
            tempAccuracy += 1
            copyOfDevEnglish[i].remove(generatedEnglish[i][j])
        else:
            try:
                tempLemmas = []

                synynomSet = wordnet.synsets(generatedEnglish[i][j]) #Get synonyms/lemmas of word
                for synset in synynomSet:
                    for item in synset.lemmas:
                        tempLemmas.append(item.name)

                for z in tempLemmas:
                    if(z in copyOfDevEnglish[i]): #If one of the synonyms/lemmas are in the target sentence, increase accuracy
                        tempAccuracy += 1
                        copyOfDevEnglish[i].remove(z)
                        break
            except:
                pass
    tempAccuracy /= len(generatedEnglish[i]) ################STILL DON'T KNOW HOW TO TAKE INTO ACCOUNT ALIGNMENT IN MEASURING ACCURACY FOR PART 1. Just using unigram precision right now (and capping at number of words in reference)
    accuracyList.append(tempAccuracy)

print("Strategy 6: ", accuracyList) #CONCLUSION: EVERYTHING IS WORSE!!!


##################################################################################################################################################################################################################################################
##################################################################################################################################################################################################################################################
##################################################################################################################################################################################################################################################


####################################### TEST SET RESULTS
print("TEST SET RESULTS")
########################## Without pre- or post-processing strategies applied ############################################
test_spanish_sentences = []
test_english_sentences = []
f = open("test.es") #Read from test file and stores accordingly
for line in iter(f):
    words = line.split()
    words = [x[0].lower()+x[1:] for x in words] #Make only the first character lowercase for spanish
    test_spanish_sentences.append(words)
f.close()

g = open("test.en") #Read from target test file and store accourdingly
for line in iter(g):
    words = line.split()
    words = [x.lower() for x in words]
    test_english_sentences.append(words)
g.close()

generatedEnglish = []
for sentence in test_spanish_sentences:
    tempList = []
    for word in sentence:
        try:
            tempList.append(lowercaseDictionary[word]) #Appends direct translation from dictionary
        except:
            tempList.append("NULL")  # When the word is NOT in the dictionary; add "NULL" instead
    generatedEnglish.append(tempList)

copyOfTestEnglish = test_english_sentences
accuracyList = []
for i in range(len(generatedEnglish)):
    tempAccuracy = 0
    for j in range(len(generatedEnglish[i])):
        if(generatedEnglish[i][j] in copyOfTestEnglish[i]): #If the current word is in the target sentence, increase accuracy count by 1
            tempAccuracy += 1
            copyOfTestEnglish[i].remove(generatedEnglish[i][j])
    tempAccuracy /= len(generatedEnglish[i]) ################STILL DON'T KNOW HOW TO TAKE INTO ACCOUNT ALIGNMENT IN MEASURING ACCURACY FOR PART 1. Just using unigram precision right now (and capping at number of words in reference)
    accuracyList.append(tempAccuracy)

print("Baseline: ", accuracyList)


###################### STRATEGY 1 - Lemmatize generated words ##########################
import nltk
lemma = nltk.wordnet.WordNetLemmatizer()

generatedEnglish = []
for sentence in test_spanish_sentences:
    tempList = []
    for word in sentence:
        try:
            tempList.append(  lemma.lemmatize(lowercaseDictionary[word])  )  #Lemmatizes generated words
        except:
            tempList.append("NULL")  # When the word is NOT in the dictionary
    generatedEnglish.append(tempList)

copyOfTestEnglish = test_english_sentences
accuracyList = []
for i in range(len(generatedEnglish)):
    tempAccuracy = 0
    for j in range(len(generatedEnglish[i])):
        if(generatedEnglish[i][j] in copyOfTestEnglish[i]): #If the current word is in the target sentence, increase accuracy count by 1
            tempAccuracy += 1
            copyOfTestEnglish[i].remove(generatedEnglish[i][j])
    tempAccuracy /= len(generatedEnglish[i]) ################STILL DON'T KNOW HOW TO TAKE INTO ACCOUNT ALIGNMENT IN MEASURING ACCURACY FOR PART 1. Just using unigram precision right now (and capping at number of words in reference)
    accuracyList.append(tempAccuracy)

print("Strategy 1: ", accuracyList) #CONCLUSION: EVERYTHING IS WORSE!!!


################### STRATEGY 2 - Part of Speech (Add verbs only if noun will precede it) #######################
import nltk

generatedEnglish = []
for sentence in test_spanish_sentences:
    tempList = []
    for word in sentence:
        try:
            try:
                partOfSpeech = nltk.tag.pos_tag([word]) #Get part of speech of current word
                if(partOfSpeech[0][1][0] == "V"):  # If it's a verb
                    for k in range(len(tempList)):
                        if (nltk.tag.pos_tag(tempList[k])[0][1][0] == "N"):  # Only adds verb if a noun precedes it
                            tempList.append(lowercaseDictionary[word])
                            break
                else:
                    tempList.append(lowercaseDictionary[word])  #If not verb, append regardless
            except:
                tempList.append(lowercaseDictionary[word])
        except:
            tempList.append("NULL")  # When the word is NOT in the dictionary
    generatedEnglish.append(tempList)

copyOfTestEnglish = test_english_sentences
accuracyList = []
for i in range(len(generatedEnglish)):
    tempAccuracy = 0
    for j in range(len(generatedEnglish[i])):
        if(generatedEnglish[i][j] in copyOfTestEnglish[i]): #If the current word is in the target sentence, increase accuracy count by 1
            tempAccuracy += 1
            copyOfTestEnglish[i].remove(generatedEnglish[i][j])
    tempAccuracy /= len(generatedEnglish[i]) ################STILL DON'T KNOW HOW TO TAKE INTO ACCOUNT ALIGNMENT IN MEASURING ACCURACY FOR PART 1. Just using unigram precision right now (and capping at number of words in reference)
    accuracyList.append(tempAccuracy)

print("Strategy 2: ", accuracyList) #CONCLUSION: EVERYTHING IS WORSE (0 percent accuracy on all)!!!


################### STRATEGY 3 - Stemming (Use Snowball stemmer on words) ##################################
from nltk.stem.snowball import SnowballStemmer
stemmer = SnowballStemmer("english")

generatedEnglish = []
for sentence in test_spanish_sentences:
    tempList = []
    for word in sentence:
        try:
            tempList.append( stemmer.stem(lowercaseDictionary[word])  )  #Stemmer version of generated words
        except:
            tempList.append("NULL")  # When the word is NOT in the dictionary; add "NULL" in place of it
    generatedEnglish.append(tempList)

copyOfTestEnglish = test_english_sentences
accuracyList = []
for i in range(len(generatedEnglish)):
    tempAccuracy = 0
    for j in range(len(generatedEnglish[i])):
        if(generatedEnglish[i][j] in copyOfTestEnglish[i]): #If the current word is in the target sentence, increase accuracy count by 1
            tempAccuracy += 1
            copyOfTestEnglish[i].remove(generatedEnglish[i][j])
    tempAccuracy /= len(generatedEnglish[i]) ################STILL DON'T KNOW HOW TO TAKE INTO ACCOUNT ALIGNMENT IN MEASURING ACCURACY FOR PART 1. Just using unigram precision right now (and capping at number of words in reference)
    accuracyList.append(tempAccuracy)

print("Strategy 3: ", accuracyList) #CONCLUSION: EVERYTHING IS WORSE (0 percent accuracy on all but last sentence (2.71%))!!!


###################### STRATEGY 4 - Use a tokenizer ##############################################
from nltk.tokenize.moses import MosesTokenizer
tokenizer = MosesTokenizer()

generatedEnglish = []
for sentence in test_spanish_sentences:
    tempList = []
    for word in sentence:
        try:
            tempList.append(  lowercaseDictionary[word]  )  #Appends generated words
        except:
            tempList.append("NULL")  # When the word is NOT in the dictionary; add "NULL" instead
    tempSentence = " ".join(tempList) #Joins into a sentence
    tempSentence = tokenizer.tokenize(tempSentence) #Tokenizes and americanizes using Stanford tokenizer

    generatedEnglish.append(tempSentence)

copyOfTestEnglish = test_english_sentences
accuracyList = []
for i in range(len(generatedEnglish)):
    tempAccuracy = 0
    for j in range(len(generatedEnglish[i])):
        if(generatedEnglish[i][j] in copyOfTestEnglish[i]): #If the current word is in the target sentence, increase accuracy count by 1
            tempAccuracy += 1
            copyOfTestEnglish[i].remove(generatedEnglish[i][j])
    tempAccuracy /= len(generatedEnglish[i]) ################STILL DON'T KNOW HOW TO TAKE INTO ACCOUNT ALIGNMENT IN MEASURING ACCURACY FOR PART 1. Just using unigram precision right now (and capping at number of words in reference)
    accuracyList.append(tempAccuracy)

print("Strategy 4: ", accuracyList) #CONCLUSION: EVERYTHING IS STILL WORSE THAN BASELINE!!!


##################### STRATEGY 5 - WSD (see if one of the meanings of a generated word is in the target sentence) ########################
import nltk
from nltk.corpus import wordnet as wn

generatedEnglish = []
for sentence in test_spanish_sentences:
    tempList = []
    for word in sentence:
        try:
            tempList.append(  lowercaseDictionary[word]  )  #Appends generated words
        except:
            tempList.append("NULL")  # When the word is NOT in the dictionary
    generatedEnglish.append(tempList)

copyOfTestEnglish = test_english_sentences
accuracyList = []
for i in range(len(generatedEnglish)):
    tempAccuracy = 0
    for j in range(len(generatedEnglish[i])):
        if(generatedEnglish[i][j] not in copyOfTestEnglish[i]): #If the current word is NOT in the target sentence, increase accuracy count by 1
            tempSynonymSet = []
            for ss in wn.synsets(generatedEnglish[i][j]): #Generates all definitions of current word
                tempSynonymSet.append(ss.definition())
            for z in range(len(copyOfTestEnglish[i])): #Generates all definitions of all words in target sentence
                tempTargetWord = copyOfTestEnglish[i][z]
                tempTargetWordSynonymSet = []
                for m in wn.synsets(tempTargetWord):
                    tempTargetWordSynonymSet.append(m.definition())

                for k in range(len(tempSynonymSet)):
                    if(tempSynonymSet[k] in tempTargetWordSynonymSet): #If 1 of the current word's meanings are among the target sentence words' meanings, increase accuracy count by 1
                        tempAccuracy += 1
                        break
        elif(generatedEnglish[i][j] in copyOfTestEnglish[i]):
            tempAccuracy += 1
            copyOfTestEnglish[i].remove(generatedEnglish[i][j])
    tempAccuracy /= len(generatedEnglish[i]) ################STILL DON'T KNOW HOW TO TAKE INTO ACCOUNT ALIGNMENT IN MEASURING ACCURACY FOR PART 1. Just using unigram precision right now (and capping at number of words in reference)
    accuracyList.append(tempAccuracy)

print("Strategy 5: ", accuracyList) #CONCLUSION: EVERYTHING IS WORSE!!!


######################## STRATEGY 6 - Producing all synonyms of a word not in the target sentence and seeing if any of those are ##################################
from nltk.corpus import wordnet
import nltk

generatedEnglish = []
for sentence in test_spanish_sentences:
    tempList = []
    for word in sentence:
        try:
            tempList.append(lowercaseDictionary[word]) #Appends direct translation word from dictionary
        except:
            tempList.append("NULL")  # When the word is NOT in the dictionary; add "NULL" instead
    generatedEnglish.append(tempList)

copyOfTestEnglish = test_english_sentences
accuracyList = []
for i in range(len(generatedEnglish)):
    tempAccuracy = 0
    for j in range(len(generatedEnglish[i])):
        if(generatedEnglish[i][j] in copyOfTestEnglish[i]): #If the current word is in the target sentence, increase accuracy count by 1
            tempAccuracy += 1
            copyOfTestEnglish[i].remove(generatedEnglish[i][j])
        else:
            try:
                tempLemmas = []

                synynomSet = wordnet.synsets(generatedEnglish[i][j]) #Generate all synonyms/lemmas of current word
                for synset in synynomSet:
                    for item in synset.lemmas:
                        tempLemmas.append(item.name)

                for z in tempLemmas:
                    if(z in copyOfTestEnglish[i]): #If one of the synonyms/lemmas is in the target sentence, increase accuracy count by 1
                        tempAccuracy += 1
                        copyOfTestEnglish[i].remove(z)
                        break
            except:
                pass
    tempAccuracy /= len(generatedEnglish[i]) ################STILL DON'T KNOW HOW TO TAKE INTO ACCOUNT ALIGNMENT IN MEASURING ACCURACY FOR PART 1. Just using unigram precision right now (and capping at number of words in reference)
    accuracyList.append(tempAccuracy)

print("Strategy 6: ", accuracyList) #CONCLUSION: EVERYTHING IS WORSE!!!