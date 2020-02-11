import os
import pickle
import re
from nltk import word_tokenize
import operator
"""
dict = {}

def parse_blog(sentence):
        tokens = word_tokenize(sentence)
        for token in tokens:
            count = dict.get(token.lower(), 0)
            dict[token.lower()] = count + 1

folders = os.listdir('blogs')


count1 = -1
# Iterate all names
for blog in folders:
    blog_path = './blogs/' + blog
    count1 += 1
    if count1 % 500 == 0:
        print(count1)
    # Process the blog content
    with open(blog_path, 'rb') as f:
        lines = f.read()
        lines = str(lines, 'utf-8', 'replace')
        lines = re.sub(r'[^\w\s]','', lines)
        lines = re.sub('<[^<]+?>', '', lines)
        parse_blog(lines)

# Save the count dict
filename = "blog_count.txt"
outfile = open(filename,'wb')
pickle.dump(dict, outfile)
outfile.close()


filename = "blog_count.txt"
infile = open(filename, 'rb')
dict = pickle.load(infile)
infile.close()

sorted_dict = sorted(dict.items(), key=operator.itemgetter(1), reverse=True)[:15000]
top_words = [word[0] for word in sorted_dict]


data_dist = [[0] * 15000] * 19320

def parse_top_words(sentence, index):
        tokens = word_tokenize(sentence)

        for token in tokens:
            if token.lower() not in top_words:
                continue
            data_dist[index][top_words.index(token.lower())] += 1

folders = os.listdir('blogs')


count2 = -1
idx = -1
# Iterate all names
for blog in folders:
    blog_path = './blogs/' + blog

    count2 += 1
    if count2 % 500 == 0:
        print(count2)
    idx += 1
    # Process the blog content
    with open(blog_path, 'rb') as f:
        lines = f.read()
        lines = str(lines, 'utf-8', 'replace')
        lines = re.sub(r'[^\w\s]','', lines)
        lines = re.sub('<[^<]+?>', '', lines)
        parse_top_words(lines, idx)


# Save the count dict
filename = "blog_data_dist.txt"
outfile = open(filename,'wb')
pickle.dump(data_dist, outfile)
outfile.close()

data_size = [sum(i) for i in data_dist]
print(data_size[:20])

filename = "blog_data_size.txt"
outfile = open(filename, 'wb')
pickle.dump(data_size, outfile)
outfile.close()

"""


