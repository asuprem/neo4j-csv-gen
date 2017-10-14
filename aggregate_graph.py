from __future__ import print_function
import sqlite3, operator
import vgm_utils
import json , sys, pdb, time
from itertools import product
#python THISFILE aggregate_graph_full.vgm aggregate ssag osag


conn_obj = sqlite3.connect('../ExtractedData/' + 'objects' + '.db')
conn_rel = sqlite3.connect('../ExtractedData/' + 'relations' + '.db')
rel_curs = conn_rel.cursor()
obj_curs = conn_obj.cursor()


# these are global uniques
object_ids = dict(obj_curs.execute('Select synset,id from synset_count'))
relation_ids = dict(rel_curs.execute('Select synset,id from synset_count'))
subjrel_ret = rel_curs.execute('Select subj_id, rel_id,id from subj_rel').fetchall()
objrel_ret =rel_curs.execute('Select obj_id, rel_id,id from obj_rel').fetchall()
ssag_subjrel_ids = {(val[0],val[1]):val[2] for val in subjrel_ret}   #val[0] is SUBJID; val[1] is RELID
osag_objrel_ids = {(val[0],val[1]):val[2] for val in objrel_ret}   #val[0] is OBJID; val[1] is RELID

'''
 to do:

 create four new contexts:
     >ssag_subjrel_ids - these are relatioship ids for ssag format. There are multiple copies of each relation. Relations are Unique by their association with a subject, i.e. there are multiple instances of eat, but only one instance of man eat, or woman eat
     >ssag_obj_ids - these are the basic unique object ids, imported from objectdb.synset_count
     >osag_obj_ids - these are the basic unique object ids, imported from objectdb.synset_count
     >osag_objrel_ids - these are relationship ids for osag format. There are, again, multiple copies of each relation. Relations are unique based on their relation with a POS object (as opposed to subject), i.e. multiple instances of eat, but one each of eats chicken, or eats apple.

When reading each image in the json_extract, we will:
    output the TWO general aggregate file, which contains each relationship in two lines:
            SUBJ, REL in aggregate_subject
            REL - OBJ in aggregate_object
            These should be sorted and uniqfied
    output the aggregate-ssag files
            SUBJ, REL in ssag_subject (UNIQUE RELATIONS, UNIQUE SUBJECTS)
            OBJ, REL in ssag_object (NON UNIQUE RELATIONS; UNIQUE OBJECTS)
    output the aggregate-osag files
            SUBJ, REL in osag_subject (NON UNIQUE RELATIONS, UNIQUE SUBJECTS)
            OBJ, REL in osag_object (UNIQUE RELATIONS; UNIQUE OBJECTS)
    To generate the files, we take the current relation under consideration and:
        get the agrgegate relation ID
        get the ssag subject-relation ID
        get the osag object-relation ID
        get the subject ID
        get the object ID

        aggregate_subject gets:
            subject ID, aggregate relation ID      <--SHOULD BE UNIQFIED
        aggregate_object gets
            object ID, aggregate relation ID       <--SHOULD BE UNIQFIED
        ssag_subject gets
            subject ID, ssag subject-relation ID   <--SHOULD BE UNIQFIED
        ssag_object gets
            object ID,  ssag subject-relation ID   <--SHOULD BE UNIQFIED
        osag_subject gets
            subject ID, osag object-relation ID   <--SHOULD BE UNIQFIED
        osag_object gets
            object ID,  osag object-relation ID   <--SHOULD BE UNIQFIED
        
        NEED SOME DOCUMENTATION ON THIS AS WELL
'''

# Here we get the new IDS and write them to the aggregate graph file
def aggregate_extract(line, file_ops):
    line = line.split(',') #<--Relationship, subject, object, rel synset
    rel_synset = line[3]
    subj_id = line[1]
    obj_id = line[2]
    rel_id = line[0]
    ssag_rel_id = str(ssag_subjrel_ids[(int(subj_id),int(rel_id))])
    osag_rel_id = str(osag_objrel_ids[(int(obj_id),int(rel_id))])

    #aggregate_subj
    file_ops[0].write(','.join([subj_id,rel_id,rel_synset]))
    #aggregate_obj
    file_ops[1].write(','.join([obj_id,rel_id,rel_synset]))
    #ssag_subj
    file_ops[2].write(','.join([subj_id,ssag_rel_id,rel_synset]))
    #ssag_obj
    file_ops[3].write(','.join([obj_id,ssag_rel_id,rel_synset]))
    #osag_subj
    file_ops[4].write(','.join([subj_id,osag_rel_id,rel_synset]))
    #osag_obj
    file_ops[5].write(','.join([obj_id,osag_rel_id,rel_synset]))
    

def main():
    start = time.time()
    #path to aggregate_graph_full.vgm (from reduced_relationship_gen.py)
    aggregate_full = sys.argv[1]
    #name of output aggregate_file (aggregate_subj, aggregate_obj)
    #name of output ssag (ssag_subj, ssag_obj)
    #name of output osag (osag_subj, osag_obj) <-----IN THIS ORDER
    file_names = [''.join(i) for i in product(sys.argv[2:5],['_subj.vgm', '_obj.vgm'])]
    file_ops = [open(file_name, 'a+') for file_name in file_names]
    with open (aggregate_full,'r') as aggregate:
        for line in aggregate:
            aggregate_extract(line, file_ops)
    

if __name__ == '__main__':
    main()
