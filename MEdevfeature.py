
import nltk

# tagger = pycrfsuite.Tagger()
# tagger.open('crf.model')

f = open("dev.csv", 'r')
f_iter = iter(f)

bio_tag = []
sent_id = 114784
sentence = []
tmp_s = []
pos_tag = []
tmp2 = []

for w in f_iter:
    s = ''.join([i if ord(i) < 128 else ' ' for i in w]).strip()
    s1 = s.split('"')
    s2 = []
    if len(s1) == 1 or s[-1] == '"':
        s = s.split(',')
        if s[-1] == '':
            s[-1] = 'z'
    else:
        s2.extend(s1[0].split(",")[0:3])
        s2.append(s1[1])
        s = s2
    s_id = int(s[2])
    if s_id == sent_id:
        tmp_s.append(s[3])
    else:
        tmp = nltk.pos_tag(tmp_s)
        sentence.append(tmp)
        tmp_s = []
        sent_id = s_id
        tmp_s.append(s[3])

tmp = nltk.pos_tag(tmp_s)
sentence.append(tmp)


def word2features(doc, i):
    word = doc[i][0]
    postag = doc[i][1]
    feature_list = []

    # Common features for all words
    features = [
        'token=' + word,
        'postag=' + postag,
        'word[-3:]=' + word[-3:],
        'word[-2:]=' + word[-2:],
        'cap=%s' % word.isupper(),
        'alpha=%s' % word.isalpha(),
        'numeric=%s' % word.isnumeric()
    ]

    # Features for words that are not
    # at the beginning of a document
    if i > 0:
        word1 = doc[i-1][0]
        postag1 = doc[i-1][1]
        features.extend([
            'PrevPos=' + postag1
        ])
    else:
        # Indicate that it is the 'beginning of a document'
        features.append('BOS=BOS')
    if i > 1:
        postag2 = doc[i-2][1]
        features.extend([
            'Prev2Pos=' + postag2
        ])
    # Features for words that are not
    # at the end of a document
    if i < len(doc)-1:
        word1 = doc[i+1][0]
        postag1 = doc[i+1][1]
        features.extend([
            'Nextpostag=' + postag1
        ])
    else:
        # Indicate that it is the 'end of a document'
        features.append('EOS=EOS')
    if i< len(doc)-2:
        postag2 = doc[i+2][1]
        features.extend([
            'Next2postag=' + postag2
        ])
    return features


# A function for extracting features in documents
def extract_features(doc):
    return [word2features(doc, i) for i in range(len(doc))]


# A function fo generating the list of labels for each document
def get_labels(doc):
    return [label[0] for (token, postag, label) in doc]


X = [extract_features(doc) for doc in sentence]
X2 = [i for i in X]

devAns = open("test.feature","w")

for i in range(len(X)):
    for j in range(len(X[i])):
        cur = X[i][j]
        tempStr = "\t".join(cur)+"\t"
        prevBIO = ""
        prev2BIO = ""
        if j-1>0:
            prevBIO = "prevBIO=@@" +"\t"
        if j-2>0:
            prev2BIO = "prev2BIO=@@"+ "\t"
        tempStr+= prevBIO + prev2BIO  +"\n"
        devAns.write(tempStr)
devAns.close()
# f2 = open('result.txt', 'w')
# f2.write(str(tagger.tag(X2)))
# f2.close()
