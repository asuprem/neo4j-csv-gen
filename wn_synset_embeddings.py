# This is a simple synset-to-vector conversion. 
# For each synset, we get their lemmas, and take the Glove Vector for those lemmas. Then we average
# the GloVe vectors for the lemmas for each synset to get the synset GloVe vector
# This is really not the best method for synset embeddings, as we are simplifying complex 
# language phenomena, namely word disambiguation.

# How to run: 
# $ python synset_to_glove.py
#make sure the db files are where they are supposed to be

import sys
from nltk.corpus import wordnet as wn
import operator
import time
import pdb
import sqlite3
import vgm_utils
import gensim
import numpy as np

def main():

    objectsdb_path   = '../ExtractedData/' + 'objects'   + '.db'
    relationsdb_path = '../ExtractedData/' + 'relations' + '.db'
    aggregatedb_path = '../ExtractedData/' + 'aggregate' + '.db'
    embeddings_path = '../ExtractedData/wn_embeddings.vgm'
    embeddings_file = open(embeddings_path,'w')

    object_ids = vgm_utils.get_node_ids(objectsdb_path)
    relation_ids = vgm_utils.get_node_ids(relationsdb_path)

    all_syn = [item for item in wn.all_synsets()]

    l_counter = 0
    start = time.time()
    print 'Loading model:'
    model = gensim.models.KeyedVectors.load_word2vec_format('../ExtractedData/GoogleNews-vectors-negative300.bin',binary=True,unicode_errors='ignore')
    print 'Complete at ' + str(time.time()-start) + '. Beginning Work...'
    for _synset in all_syn:
        this_vec = np.zeros(300).astype('float32')
        lemmas = _synset.lemma_names()
        lemmas = [item.encode('ascii').lower() for item in lemmas]
        lemma_scores = []
        if len(lemmas) == 1:
            lemma_scores.append(1)
        else:
            lemma_scores.append(0.8)
            try:
                extra_scores = [0.2/(len(lemmas)-1)]*(len(lemmas)-1)
            except:
                pdb.set_trace()
        for lemma,score in zip(lemmas,lemma_scores):
            if lemma not in model:
                forms = lemma.split('_')
                word_vec = np.zeros(300).astype('float32')
                for word in forms:
                    if word in model:
                        word_vec+=model[word]
                if np.count_nonzero(word_vec):
                    this_vec+=score*word_vec
            else:
                this_vec+=score*model[lemma]
        #this_vec/=len(lemmas)
        write_line =  str(_synset)[8:-2].encode('ascii')+','+','.join([str(num) for num in this_vec]) + '\n'
        embeddings_file.write(write_line)
        l_counter+=1
        if l_counter%100 == 0:
            print 'Completed with ' + str(l_counter)+ ' objects at ' + str(time.time()-start)
    print 'Compelted with All synsets. Starting on Relations'
    embeddings_file.close()

if __name__ == '__main__':
    main()