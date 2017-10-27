# This is a simple synset-to-vector conversion. 
# For each synset, we get their lemmas, and take the Glove Vector for those lemmas. Then we average
# the GloVe vectors for the lemmas for each synset to get the synset GloVe vector
# This is really not the best method for synset embeddings, as we are simplifying complex 
# language phenomena, namely word disambiguation.

import sys
from nltk.corpus import wordnet as wn
import operator
import time
import pdb
import sqlite3
import vgm_utils
import gensim


def main():

    objectsdb_path   = '../ExtractedData/' + 'objects'   + '.db'
    relationsdb_path = '../ExtractedData/' + 'relations' + '.db'
    aggregatedb_path = '../ExtractedData/' + 'aggregate' + '.db'
    embeddings_path = '../ExtractedData/embeddings.vgm'
    #embeddings_file

    object_ids = vgm_utils.get_node_ids(objectsdb_path)
    relation_ids = vgm_utils.get_node_ids(relationsdb_path)

    l_counter = 0
    start = time.time()
    print 'Loading model:'
    model = gensim.models.KeyedVectors.load_word2vec_format('../ExtractedData/lexvec.enwiki+newscrawl.300d.W+C.pos.vectors')
    print 'Complete at ' + str(time.time()-start) + '. Beginning Work...'
    for object_id in object_ids:
        lemmas = wn.synset(object_id.encode('ascii')).lemma_names()
        lemmas = [item.encode('ascii').lower() for item in lemmas]
        pdb.set_trace()


if __name__ == '__main__':
    main()