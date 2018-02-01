import operator
import random
import copy
import nltk

euroSpanishTrainList = [] #Holds words from spanish file
euroEnglishTrainList = [] #Holds words from english file

f = open("europarl-v7.es-en.es", encoding="utf8") #Reading spanish training file
for line in iter(f):
    words = line.split()
    words = [x[0].lower() + x[1:] for x in words] #Only make first character lower case because letters with accents are read as having weird sequences by python that may include capital letters
    euroSpanishTrainList.append(words)
f.close()

g = open("europarl-v7.es-en.en",  encoding="utf8") #Reading english training file
for line in iter(g):
    words = line.split()
    words = [x.lower() for x in words] #Make each word lower case
    euroEnglishTrainList.append(words)
g.close()


euroTrainDictionary = {} #Dictionary holding each foreign word and english words that appear in its context
for i in range(len(euroSpanishTrainList)):
    for j in range(len(euroSpanishTrainList[i])):
        if(euroSpanishTrainList[i][j] not in euroTrainDictionary):
            euroTrainDictionary[euroSpanishTrainList[i][j]] = {'TOTAL COUNTS': 0} #Dictionary for spanish unique words and associated english words will be made

        for z in range(len(euroEnglishTrainList[i])):
            if(euroEnglishTrainList[i][z] not in euroTrainDictionary[euroSpanishTrainList[i][j]]):
                euroTrainDictionary[euroSpanishTrainList[i][j]][euroEnglishTrainList[i][z]] = 1
                euroTrainDictionary[euroSpanishTrainList[i][j]]['TOTAL COUNTS'] += 1 #Total counts for english word in spanish word's context increases by 1
            else:
                euroTrainDictionary[euroSpanishTrainList[i][j]][euroEnglishTrainList[i][z]] += 1
                euroTrainDictionary[euroSpanishTrainList[i][j]]['TOTAL COUNTS'] += 1 #Total counts for english word in spanish word's context increases by 1

for key, items in euroTrainDictionary.items(): #Finds probabilities of each english word in context of given spanish word
    words = items
    TOTAL_COUNT = words['TOTAL COUNTS']
    for key2, items2 in words.items():
        if(key2 == 'TOTAL COUNTS'):
            continue
        else:
            euroTrainDictionary[key][key2] = items2/TOTAL_COUNT #Divides frequency of english word in context of spanish word to get probability

count = {}
total = {}
s_total = {}
convergence = 0 #Epoch number
#tempEuroTrainDictionary = {}
#tempEuroTrainDictionary != euroTrainDictionary
while(convergence <= 10):       ### LOWER THIS TO REDUCE RUN TIME; CURRENTLY TAKES ~15 MINUTES TO RUN 10 EPOCHS ALONE!!!!!!!!!!
    #tempEuroTrainDictionary = copy.deepcopy(euroTrainDictionary)

    for key, items in euroTrainDictionary.items():  # count(e|f) = 0 for all e, f
        words = items
        TOTAL_COUNT = words['TOTAL COUNTS']
        for key2, items2 in words.items():
            if (key2 == 'TOTAL COUNTS'):
                continue
            else:
                if (key not in count):
                    count[key] = {}
                else:
                    count[key][key2] = 0  # count(e|f) = 0 for all e, f
                total[key] = 0  # total(f) = 0 for all f

    for i in range(len(euroEnglishTrainList)):   #For all sentence pairs
        for j in range(len(euroEnglishTrainList[i])): #For all words in english
            s_total[euroEnglishTrainList[i][j]] = 0 #Initialize s_total

            for z in range(len(euroSpanishTrainList[i])): #For all words in spanish (foreign language)
                s_total[euroEnglishTrainList[i][j]] += euroTrainDictionary[euroSpanishTrainList[i][z]][euroEnglishTrainList[i][j]] #Modify s_total
            #Collect counts
        for j in range(len(euroEnglishTrainList[i])): #For all words in english
            for z in range(len(euroSpanishTrainList[i])): #For all words in spanish (foreign language)
                try:
                    count[euroSpanishTrainList[i][z]][euroEnglishTrainList[i][j]] += (euroTrainDictionary[euroSpanishTrainList[i][z]][euroEnglishTrainList[i][j]]  /  s_total[euroEnglishTrainList[i][j]] ) #Modify count dictionary
                except:
                    pass
                try:
                    total[euroSpanishTrainList[i][z]] += (euroTrainDictionary[euroSpanishTrainList[i][z]][euroEnglishTrainList[i][j]]  /  s_total[euroEnglishTrainList[i][j]] ) #Modify total dictionary
                except:
                    pass
    #Estimate probabilites
    for i in range(len(euroSpanishTrainList)):
        for z in range(len(euroSpanishTrainList[i])): #For all foreign words f
            for j in range(len(euroEnglishTrainList[i])): #For all words in english
                try:
                    euroTrainDictionary[euroSpanishTrainList[i][z]][euroEnglishTrainList[i][j]] = (count[euroSpanishTrainList[i][z]][euroEnglishTrainList[i][j]]  /  total[euroSpanishTrainList[i][z]]) #Modify training dictionary
                except:
                    pass
    convergence+=1




########################################## IBM Model 1 First Attempt #################################################

############################### europarl-v7 ##################################
f = open("europarl-v7_Generated.txt", "w", encoding="utf8")

for i in range(len(euroSpanishTrainList)):
    tempList = []
    for j in range(len(euroSpanishTrainList[i])):
        try:
            tempTestWord = euroSpanishTrainList[i][j]
            euroTrainDictionary[tempTestWord]['TOTAL COUNTS'] = -1000 #Lowers TOTAL COUNTS variable of spanish words from dictionary so maximum value selected is accurate

            maxValue = max(euroTrainDictionary[tempTestWord].values()) #Finds maximum frequency among english words for current spanish word
            maxKeys = [k for k, v in euroTrainDictionary[tempTestWord].items() if v == maxValue] #Selects english words with maximum frequency

            selectedTranslatedWord = random.choice(maxKeys) #Randomly selects one of the english words with the max frequency
            tempList.append(selectedTranslatedWord)
        except:
            tempList.append(euroSpanishTrainList[i][j]) #Keeps spanish word if translation not found in dictionary
    tempString = " ".join(tempList) #Joins generated words together
    f.write(tempString+"\n") #Generates sentence
f.close()

##################################### newstest 2012 ################################
foreignTestSentences = []
f = open("newstest2012.es",  encoding="utf8")
for line in iter(f):
    words = line.split()
    words = [x[0].lower() + x[1:] for x in words]
    foreignTestSentences.append(words)
f.close()

g = open("newstest2012_Generated.txt", "w", encoding="utf8")

for i in range(len(foreignTestSentences)):
    tempList = []
    for j in range(len(foreignTestSentences[i])):
        try:
            tempTestWord = foreignTestSentences[i][j]
            euroTrainDictionary[tempTestWord]['TOTAL COUNTS'] = -1000 #Lowers TOTAL COUNTS variable of spanish words from dictionary so maximum value selected is accurate

            maxValue = max(euroTrainDictionary[tempTestWord].values()) #Finds maximum frequency among english words for current spanish word
            maxKeys = [k for k, v in euroTrainDictionary[tempTestWord].items() if v == maxValue] #Selects english words with maximum frequency

            selectedTranslatedWord = random.choice(maxKeys) #Randomly selects one of the english words with the max frequency
            tempList.append(selectedTranslatedWord)
        except:
            tempList.append(foreignTestSentences[i][j]) #Keeps spanish word if translation not found in dictionary
    tempString = " ".join(tempList) #Joins generated words together
    g.write(tempString+"\n") #Generates sentence
g.close()

####################################### newstest 2013 ################################
foreignTestSentences = []
f = open("newstest2013.es",  encoding="utf8")
for line in iter(f):
    words = line.split()
    words = [x[0].lower() + x[1:] for x in words]
    foreignTestSentences.append(words)
f.close()

g = open("newstest2013_Generated.txt", "w", encoding="utf8")

for i in range(len(foreignTestSentences)):
    tempList = []
    for j in range(len(foreignTestSentences[i])):
        try:
            tempTestWord = foreignTestSentences[i][j]
            euroTrainDictionary[tempTestWord]['TOTAL COUNTS'] = -1000 #Lowers TOTAL COUNTS variable of spanish words from dictionary so maximum value selected is accura

            maxValue = max(euroTrainDictionary[tempTestWord].values()) #Finds maximum frequency among english words for current spanish word
            maxKeys = [k for k, v in euroTrainDictionary[tempTestWord].items() if v == maxValue] #Selects english words with maximum frequency

            selectedTranslatedWord = random.choice(maxKeys) #Randomly selects one of the english words with the max frequency
            tempList.append(selectedTranslatedWord)
        except:
            tempList.append(foreignTestSentences[i][j]) #Keeps spanish word if translation not found in dictionary
    tempString = " ".join(tempList) #Joins generated words together
    g.write(tempString+"\n") #Generates sentence
g.close()







#################################### IBM Model 1 with STRATEGY: ADD VERBS ONLY IF NOUN PRECEDES IT ##################################################

############################### europarl-v7 ##################################
f = open("europarl-v7_Generated_Strategy.txt", "w", encoding="utf8")

for i in range(len(euroSpanishTrainList)):
    tempList = []
    for j in range(len(euroSpanishTrainList[i])):
        try:
            tempTestWord = euroSpanishTrainList[i][j]
            partOfSpeech = nltk.tag.pos_tag([tempTestWord])  # POS-tag for potential improvement
            if (partOfSpeech[0][1][0] == "V"):  # If it's a verb
                for k in range(len(tempList)):
                    if (nltk.tag.pos_tag(tempList[k])[0][1][0] == "N"):  # Only adds verb if a noun precedes it
                        euroTrainDictionary[tempTestWord]['TOTAL COUNTS'] = -1000  #Lowers TOTAL COUNTS variable of spanish words from dictionary so maximum value selected is accura

                        maxValue = max(euroTrainDictionary[tempTestWord].values()) #Finds maximum frequency among english words for current spanish word
                        maxKeys = [k for k, v in euroTrainDictionary[tempTestWord].items() if v == maxValue] #Selects english words with maximum frequency

                        selectedTranslatedWord = random.choice(maxKeys) #Randomly selects one of the english words with the max frequency
                        tempList.append(selectedTranslatedWord)
                        break
            else:
                euroTrainDictionary[tempTestWord]['TOTAL COUNTS'] = -1000  #Lowers TOTAL COUNTS variable of spanish words from dictionary so maximum value selected is accura

                maxValue = max(euroTrainDictionary[tempTestWord].values()) #Finds maximum frequency among english words for current spanish word
                maxKeys = [k for k, v in euroTrainDictionary[tempTestWord].items() if v == maxValue] #Selects english words with maximum frequency

                selectedTranslatedWord = random.choice(maxKeys) #Randomly selects one of the english words with the max frequency
                tempList.append(selectedTranslatedWord)
        except:
            tempList.append(euroSpanishTrainList[i][j]) #Keeps spanish word if translation not found in dictionary
    tempString = " ".join(tempList) #Joins generated words together
    f.write(tempString+"\n") #Generates sentence
f.close()


##################################### newstest 2012 ################################
foreignTestSentences = []
f = open("newstest2012.es",  encoding="utf8")
for line in iter(f):
    words = line.split()
    words = [x[0].lower() + x[1:] for x in words]
    foreignTestSentences.append(words)
f.close()

f = open("newstest2012_Generated_Strategy.txt", "w", encoding="utf8")
for i in range(len(foreignTestSentences)):
    tempList = []
    for j in range(len(foreignTestSentences[i])):
        try:
            tempTestWord = foreignTestSentences[i][j]
            partOfSpeech = nltk.tag.pos_tag([tempTestWord]) #POS-tag for potential improvement
            if(partOfSpeech[0][1][0] == "V"): #If it's a verb
                for k in range(len(tempList)):
                    if( nltk.tag.pos_tag(tempList[k])[0][1][0] == "N" ): #Only adds verb if a noun precedes it
                        euroTrainDictionary[tempTestWord]['TOTAL COUNTS'] = -1000  #Lowers TOTAL COUNTS variable of spanish words from dictionary so maximum value selected is accura

                        maxValue = max(euroTrainDictionary[tempTestWord].values()) #Finds maximum frequency among english words for current spanish word
                        maxKeys = [k for k, v in euroTrainDictionary[tempTestWord].items() if v == maxValue] #Selects english words with maximum frequency

                        selectedTranslatedWord = random.choice(maxKeys) #Randomly selects one of the english words with the max frequency
                        tempList.append(selectedTranslatedWord)
                        break
            else:
                euroTrainDictionary[tempTestWord]['TOTAL COUNTS'] = -1000 #Lowers TOTAL COUNTS variable of spanish words from dictionary so maximum value selected is accura

                maxValue = max(euroTrainDictionary[tempTestWord].values()) #Finds maximum frequency among english words for current spanish word
                maxKeys = [k for k, v in euroTrainDictionary[tempTestWord].items() if v == maxValue] #Selects english words with maximum frequency

                selectedTranslatedWord = random.choice(maxKeys) #Randomly selects one of the english words with the max frequency
                tempList.append(selectedTranslatedWord)
        except:
            tempList.append(foreignTestSentences[i][j]) #Keeps spanish word if translation not found in dictionary
    tempString = " ".join(tempList) #Joins generated words together
    f.write(tempString+"\n") #Generates sentence
f.close()

##################################### newstest 2013 ################################
foreignTestSentences = []
f = open("newstest2013.es",  encoding="utf8")
for line in iter(f):
    words = line.split()
    words = [x[0].lower() + x[1:] for x in words]
    foreignTestSentences.append(words)
f.close()

f = open("newstest2013_Generated_Strategy.txt", "w", encoding="utf8")
for i in range(len(foreignTestSentences)):
    tempList = []
    for j in range(len(foreignTestSentences[i])):
        try:
            tempTestWord = foreignTestSentences[i][j]
            partOfSpeech = nltk.tag.pos_tag([tempTestWord]) #POS-tag for potential improvement
            if(partOfSpeech[0][1][0] == "V"): #If it's a verb
                for k in range(len(tempList)):
                    if( nltk.tag.pos_tag(tempList[k])[0][1][0] == "N" ): #Only adds verb if a noun precedes it
                        euroTrainDictionary[tempTestWord]['TOTAL COUNTS'] = -1000  #Lowers TOTAL COUNTS variable of spanish words from dictionary so maximum value selected is accura

                        maxValue = max(euroTrainDictionary[tempTestWord].values()) #Finds maximum frequency among english words for current spanish word
                        maxKeys = [k for k, v in euroTrainDictionary[tempTestWord].items() if v == maxValue] #Selects english words with maximum frequency

                        selectedTranslatedWord = random.choice(maxKeys) #Randomly selects one of the english words with the max frequency
                        tempList.append(selectedTranslatedWord)
                        break
            else:
                euroTrainDictionary[tempTestWord]['TOTAL COUNTS'] = -1000  #Lowers TOTAL COUNTS variable of spanish words from dictionary so maximum value selected is accura

                maxValue = max(euroTrainDictionary[tempTestWord].values()) #Finds maximum frequency among english words for current spanish word
                maxKeys = [k for k, v in euroTrainDictionary[tempTestWord].items() if v == maxValue] #Selects english words with maximum frequency

                selectedTranslatedWord = random.choice(maxKeys) #Randomly selects one of the english words with the max frequency
                tempList.append(selectedTranslatedWord)
        except:
            tempList.append(foreignTestSentences[i][j]) #Keeps spanish word if translation not found in dictionary
    tempString = " ".join(tempList) #Joins generated words together
    f.write(tempString+"\n") #Generates sentence
f.close()