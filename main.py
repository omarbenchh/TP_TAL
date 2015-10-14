from collections import Counter
import re
import csv

from textblob import *

f = open('germinal.txt', 'r')
textInput = f.read()

myRegex = re.compile('\n*\n \n\n.*partie\n\n \n\n')
parties = re.split(myRegex, textInput)

myRegexChap = re.compile('\n\n \n\n[IXVLMC]*[IXVLMC]\n\n')
chapitres = []



for count, element in enumerate(parties):
    chapitres.append(re.split(myRegexChap, element))

myRegexPara = re.compile('\n\n')
paragraphes = []
paragraphe = []
for partie in chapitres:
    for count, element in enumerate(partie):
        paragraphe.append(re.split(myRegexPara, element))
    paragraphes.append(paragraphe)
    paragraphe = []

phrase = []
phrasesParagraphe = []
paragrapheChapitre = []
for partie in paragraphes:
    for chapitre in partie:
        for count, element in enumerate(chapitre):
            phrase.append(TextBlob(element.decode('UTF-8')).sentences)
        phrasesParagraphe.append(phrase)
        phrase = []
    paragrapheChapitre.append(phrasesParagraphe)
    phrasesParagraphe = []
test = []
mywords = []

for index1, part in enumerate(paragrapheChapitre):
    if index1 != 0:
        with open('Segments\\partie' + str(index1) + '.csv', 'wb') as csvfile:
            fieldnames = ['Mots', 'Partie', 'Chapitre', 'Paragraphe', 'Phrase']
            monFichierCSV = csv.DictWriter(csvfile, fieldnames=fieldnames)
            monFichierCSV.writeheader()
            for index2, chap in enumerate(part):
                for index3, parag in enumerate(chap):
                    for index4, phra in enumerate(parag):
                        test.append(paragrapheChapitre[index1][index2][index3][index4].words)
                        for index5, mots in enumerate(test):
                            for index6, tmp in enumerate(mots):
                                mywords.append(str(tmp.encode('UTF-8')))
                                monFichierCSV.writerow({'Mots': str(tmp.encode('UTF-8')), 'Partie': index1,
                                                        'Chapitre': index2 + 1, 'Paragraphe': index3 + 1,
                                                        'Phrase': index4 + 1})
                        test = []
        counts = Counter(mywords)
        with open('NoRep\\partie' + str(index1) + '_noRepeat.csv', 'wb') as csvfile:
            fieldnames = ['Mots', 'Effectif', 'Longueur', 'Partie']
            monFichierCSV2 = csv.DictWriter(csvfile, fieldnames=fieldnames)
            monFichierCSV2.writeheader()
            for singleWord in counts:
                monFichierCSV2.writerow({'Mots': str(singleWord),
                                         'Effectif': counts[singleWord],
                                         'Longueur': len(singleWord), 'Partie': index1})
        mywords = []

myRegexNoms = re.compile('[^\.\-\xe0!?] [A-Z][a-z]+')
noms = myRegexNoms.findall(textInput)
noms2 = []
for nom in noms:
    noms2.append(nom[2:])
noms = set(noms2)
with open('listeNoms.csv', 'wb') as csvfile:
    fieldnames = ['Noms']
    monFichierCSV0 = csv.DictWriter(csvfile, fieldnames=fieldnames)
    monFichierCSV0.writeheader()
    for nom in noms:
        monFichierCSV0.writerow({'Noms': str(nom)})