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
    embeddings_path = '../ExtractedData/local_embeddings.vgm'
    embeddings_file = open(embeddings_path,'w')

    object_ids = vgm_utils.get_node_ids(objectsdb_path)
    relation_ids = vgm_utils.get_node_ids(relationsdb_path)

    l_counter = 0
    start = time.time()
    print 'Loading model:'
    model = gensim.models.KeyedVectors.load_word2vec_format('../ExtractedData/GoogleNews-vectors-negative300.bin',binary=True,unicode_errors='ignore')
    print 'Complete at ' + str(time.time()-start) + '. Beginning Work...'
    for object_id in object_ids:
        this_vec = np.zeros(300).astype('float32')
        lemmas = wn.synset(object_id.encode('ascii')).lemma_names()
        lemmas = [item.encode('ascii').lower() for item in lemmas]
        for lemma in lemmas:
            if lemma not in model:
                forms = lemma.split('_')
                word_vec = np.zeros(300).astype('float32')
                for word in forms:
                    if word in model:
                        word_vec+=model[word]
                if np.count_nonzero(word_vec):
                    this_vec+=word_vec
            else:
                this_vec+=model[lemma]
        this_vec/=len(lemmas)
        write_line =  object_id.encode('ascii')+','+','.join([str(num) for num in this_vec]) + '\n'
        embeddings_file.write(write_line)
        l_counter+=1
        if l_counter%100 == 0:
            print 'Completed with ' + str(l_counter)+ ' objects at ' + str(time.time()-start)
    print 'Compelted with Objects. Starting on Relations'
    l_counter = 0
    for object_id in relation_ids:
        this_vec = np.zeros(300).astype('float32')
        lemmas = wn.synset(object_id.encode('ascii')).lemma_names()
        lemmas = [item.encode('ascii').lower() for item in lemmas]
        for lemma in lemmas:
            if lemma not in model:
                forms = lemma.split('_')
                word_vec = np.zeros(300).astype('float32')
                for word in forms:
                    if word in model:
                        word_vec+=model[word]
                if np.count_nonzero(word_vec):
                    this_vec+=word_vec
            else:
                this_vec+=model[lemma]
        this_vec/=len(lemmas)
        write_line =  object_id.encode('ascii')+','+','.join([str(num) for num in this_vec]) + '\n'
        embeddings_file.write(write_line)
        l_counter+=1
        if l_counter%100 == 0:
            print 'Completed with ' + str(l_counter)+ ' objects'+ str(time.time()-start)
    embeddings_file.close()

if __name__ == '__main__':
    main()