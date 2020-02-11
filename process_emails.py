import os
import pickle
import re
import operator
from nltk import word_tokenize
from data_div import measureAllDistance

"""
dict = {}

def parse_email(sentence):
    for sentence in sentence:
        sentence = re.sub(r'[^\w\s]','',sentence)
        tokens = word_tokenize(sentence)
        for token in tokens:
            count = dict.get(token.lower(), 0)
            dict[token.lower()] = count + 1

folders = os.listdir('maildir')



# Iterate all names
for name in folders:
    sent_folder = './maildir/' + name + '/sent/'
    emails = os.listdir(sent_folder)
    print(sent_folder)

    # Process all emails
    for email in emails:
        print(sent_folder + ' ' +email)
        with open(sent_folder + email, 'r') as f:
                lines = f.read().split('\n\n')[1:]
                parse_email(lines)

# Save the count dict
filename = "count.txt"
outfile = open(filename,'wb')
pickle.dump(dict, outfile)
outfile.close()

# Load the dict from disk
filename = "count.txt"
infile = open(filename,'rb')
dict = pickle.load(infile)
infile.close()


sorted_dict = sorted(dict.items(), key=operator.itemgetter(1), reverse=True)[:15000]
top_words = [word[0] for word in sorted_dict]




filename = "top_words.txt"
outfile = open(filename,'wb')
pickle.dump(top_words, outfile)
outfile.close()



filename = "top_words.txt"
infile = open(filename, 'rb')
top_words = pickle.load(infile)
infile.close()

person_to_words = {}
person_to_number_of_samples = [0] * 150
index = -1

def parse_top_words(sentence, name, index):
    for sentence in sentence:
        sentence = re.sub(r'[^\w\s]','',sentence)
        tokens = word_tokenize(sentence)
        for token in tokens:
            if token.lower() not in top_words:
                continue
            person_to_number_of_samples[index] += 1
            count = person_to_words[name].get(token.lower(), 0)
            person_to_words[name][token.lower()] = count + 1

folders = os.listdir('maildir')

# Iterate all names
for name in folders:
    sent_folder = './maildir/' + name + '/sent/'
    emails = os.listdir(sent_folder)
    print(sent_folder)
    index += 1
    # Process all emails
    for email in emails:
        print(sent_folder + ' ' +email)
        with open(sent_folder + email, 'r') as f:
                lines = f.read().split('\n\n')[1:]
                person_to_words[name] = {}
                parse_top_words(lines, name, index)


filename = "person_to_words.txt"
outfile = open(filename,'wb')
pickle.dump(person_to_words, outfile)
outfile.close()

filename2 = "sampleSizes.txt"
outfile2 = open(filename2, 'wb')
pickle.dump(person_to_number_of_samples, outfile2)
outfile2.close()
"""

filename = "person_to_words.txt"
infile = open(filename,'rb')
dict = pickle.load(infile)
infile.close()

filename = "top_words.txt"
infile = open(filename,'rb')
top_words = pickle.load(infile)
infile.close()


i = -1
dist = [[0] * 15000] * 150
for _, sizes in dict.items():
    i += 1
    for word, _ in sizes.items():
        dist[i][top_words.index(word)] += 1


measureAllDistance(dist)

"""
file = "client_data_dist.txt"
outfile = open(file, 'wb')
pickle.dump(dist, outfile, protocol=2)
outfile.close()
"""
