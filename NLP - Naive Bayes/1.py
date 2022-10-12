from __future__ import unicode_literals
from hazm import *
import pandas as pd
import numpy as np
import math

train_data = pd.read_csv("comment_train.csv")
p_recommendation = len(train_data[train_data['recommend'] == 'recommended']) / len(train_data['recommend'])
t_recommendation = len(train_data[train_data['recommend'] == 'recommended'])
###  Preprocessing Comments
#  Recommended Comments
normalizer = Normalizer()
stemmer = Stemmer()
lemmatizer = Lemmatizer()
positive_comment_words = []
for i in train_data[ train_data['recommend'] == 'recommended' ]['comment']:
    #a = normalizer.normalize(i)
    a = word_tokenize(i)
    for j in a:
        #positive_comment_words.append( stemmer.stem(j) )
        positive_comment_words.append( lemmatizer.lemmatize(j) )

total = len(positive_comment_words)
comment_words_prob = {}
for i in positive_comment_words:
    if i in comment_words_prob:
        comment_words_prob[i] += 1
    else:
        comment_words_prob[i] = 1

for i in comment_words_prob:
    comment_words_prob[i] = (comment_words_prob[i]+1) / (t_recommendation+total)

# Not Recommended Comemnets
negative_comment_words = []
for i in train_data[ train_data['recommend'] == 'not_recommended' ]['comment']:
    #a = normalizer.normalize(i)
    a = word_tokenize(i)
    for j in a:
        #negative_comment_words.append(stemmer.stem( j ) )
        negative_comment_words.append( lemmatizer.lemmatize(j) )

total = len(negative_comment_words)
ncomment_words_prob = {}
for i in negative_comment_words:
    if i in ncomment_words_prob:
        ncomment_words_prob[i] += 1
    else:
        ncomment_words_prob[i] = 1

for i in ncomment_words_prob:
    ncomment_words_prob[i] = (ncomment_words_prob[i]+1) / (t_recommendation+total) 
#  Recommended Titles
positive_title_words = []
for i in train_data[ train_data['recommend'] == 'recommended' ]['title']:
    #a = normalizer.normalize(i)
    a = word_tokenize(i)
    for j in a:
        #positive_title_words.append( stemmer.stem(j))
        positive_title_words.append( lemmatizer.lemmatize(j) )

total = len(positive_title_words)
title_words_prob = {}
for i in positive_title_words:
    if i in title_words_prob:
        title_words_prob[i] += 1
    else:
        title_words_prob[i] = 1

for i in title_words_prob:
    title_words_prob[i] = (title_words_prob[i]+1) / (t_recommendation +total)

#  Not Recommended Titles
negative_title_words = []
for i in train_data[ train_data['recommend'] == 'recommended' ]['title']:
    #a = normalizer.normalize(i)
    a = word_tokenize(i)
    for j in a:
        #negative_title_words.append( stemmer.stem(j) )
        negative_title_words.append( lemmatizer.lemmatize(j) )

total = len(negative_title_words)
ntitle_words_prob = {}
for i in negative_title_words:
    if i in ntitle_words_prob:
        ntitle_words_prob[i] += 1
    else:
        ntitle_words_prob[i] = 1

for i in ntitle_words_prob:
    ntitle_words_prob[i] = (ntitle_words_prob[i]+1) / (t_recommendation+total)


### Prediction Phase

test_data = pd.read_csv("comment_test.csv")
correct = 0
recom_correct = 0
recom_pred = 0
for j in range( 1, len( test_data ) ):
    ##comment_words = normalizer.normalize( test_data['comment'][j]) .split(' ')
    comment_words = word_tokenize(test_data['comment'][j])
    recommend_prob = 0
    not_recommend_prob = 0
    for i in comment_words:
        #st = stemmer.stem(i) 
        st = lemmatizer.lemmatize(i)
        if st in comment_words_prob:
            recommend_prob += math.log(comment_words_prob[st])
        else:
            recommend_prob -= 10000
        if st in ncomment_words_prob:
            not_recommend_prob += math.log(ncomment_words_prob[st])
        else:
            not_recommend_prob -= 10000
    
    #title_words = normalizer.normalize( test_data['title'][j] ).split(' ')
    title_words = test_data['title'][j]
    for i in title_words:
        #st = stemmer.stem(i) 
        st = lemmatizer.lemmatize(i)
        if st in title_words_prob:
            recommend_prob += math.log(title_words_prob[st])
        else:
            recommend_prob -= 10000
        if st in ntitle_words_prob:
            not_recommend_prob += math.log(ntitle_words_prob[st])
        else:
            not_recommend_prob -= 10000
    
    recommend_prob += math.log(p_recommendation)
    not_recommend_prob += math.log(1-p_recommendation)

    if recommend_prob > not_recommend_prob:
        recom_pred += 1
    if test_data['recommend'][j] == 'recommended' and recommend_prob > not_recommend_prob:
        correct += 1
        recom_correct += 1
    if test_data['recommend'][j] == 'not_recommended' and recommend_prob < not_recommend_prob:
        correct += 1
    if (test_data['recommend'][j] == 'not_recommended' and recommend_prob > not_recommend_prob ) or (test_data['recommend'][j] == 'recommended' and recommend_prob < not_recommend_prob):
        print("Title =", test_data['title'][j])
        print("Comment =", test_data['comment'][j])


accuracy = correct / len(test_data)
precision = recom_correct / recom_pred
recall = recom_correct /  len(test_data[test_data['recommend'] == 'recommended'])
f1 = 2 * (precision*recall) / (precision+recall)
print("Accuracy =", accuracy)
print("Precision =", precision)
print("Recall =", recall)
print("F1 =", f1)
print()