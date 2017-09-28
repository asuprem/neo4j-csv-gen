from __future__ import print_function
import sqlite3, operator
import vgm_utils
import json , sys, pdb, time
#python THISFILE scene_graphs.json aggregate_graph_full

conn_obj = sqlite3.connect('../ExtractedData/' + 'objects' + '.db')
conn_rel = sqlite3.connect('../ExtractedData/' + 'relations' + '.db')
rel_curs = conn_rel.cursor()
obj_curs = conn_obj.cursor()


# these are global uniques
object_ids = dict(obj_curs.execute('Select synset,id from synset_count'))
relation_ids = dict(rel_curs.execute('Select synset,id from synset_count'))

'''
 to do:

 create four new contexts:
     ssag_subjrel_ids - these are relatioship ids for ssag format. There are multiple copies of each relation. Relations are Unique by their association with a subject, i.e. there are multiple instances of eat, but only one instance of man eat, or woman eat
     ssag_obj_ids - these are the basic unique object ids, imported from objectdb.synset_count
     osag_obj_ids - these are the basic unique object ids, imported from objectdb.synset_count
     osag_obj_rel_ids - these are relationship ids for osag format. There are, again, multiple copies of each relation. Relations are unique based on their relation with a POS object (as opposed to subject), i.e. multiple instances of eat, but one each of eats chicken, or eats apple.

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
def json_extractor(obj_read, aggregate_name):
    j_obj = json.loads(obj_read)
    obj_integrity = {}
    rel_integrity = {}
    #Get the new IDS for the objects.
    for i in range(len(j_obj['objects'])):
        if j_obj['objects'][i]['synsets'] and j_obj['objects'][i]['synsets'][0] in object_ids:
            obj_integrity[j_obj['objects'][i]['object_id']] = object_ids[j_obj['objects'][i]['synsets'][0]]
            
    
    for i in range(len(j_obj['relationships'])):
        if j_obj['relationships'][i]['synsets'] and j_obj['relationships'][i]['synsets'][0] in relation_ids:
            if j_obj['relationships'][i]['subject_id'] in obj_integrity and j_obj['relationships'][i]['object_id'] in obj_integrity:
                in_tuple = (relation_ids[j_obj['relationships'][i]['synsets'][0]], \
                            obj_integrity[j_obj['relationships'][i]['subject_id']], \
                            obj_integrity[j_obj['relationships'][i]['object_id']])
                rel_integrity[in_tuple] = j_obj['relationships'][i]['synsets'][0]
    
    # Here we need to 

    


    with open(aggregate_name, 'a+') as aggregate_file:
        for item in rel_integrity:
            aggregate_file.write(','.join([str(tup) for tup in item]) + ',' + rel_integrity[item] + '\n')

    #Format -> relation ID; subj_ID; obj_ID; rel_synset


def main():
    start = time.time()
    # Set up the split characteristics, and the file names
    #path to scene_graphs.json
    file_name = sys.argv[1]
    #name of output aggregate_file
    aggregate_name = sys.argv[2] + '.vgm'
    chunk_size, find_counter = 5000,0
    parse_file = open(file_name)
    #Read the first character and ignore
    parse_file.read(1)
    obj_read, stream_read, obj_counter = '','',0
    # Delete all vgm files in current folder:
    
    while True:
        now_read=parse_file.read(chunk_size)
        parse_read = stream_read + (now_read if now_read else '')        
        # If there is nothing left to parse
        if not parse_read:
            break
        
        obj_counter, json_obj, stream_read  = vgm_utils.par_check(obj_counter, parse_read, obj_read)
        obj_read = obj_read + json_obj

        if obj_counter == 0:
            find_counter+=1
            if find_counter%500 == 0:
                print("Valid object found: "+str(find_counter) +  '  at ' + str(int(time.time()-start)), end='\n')
            json_extractor(obj_read, aggregate_name)        
            obj_read=''

        #This exists for debugging purposes -> to early stop the files for quicker verification
        #if find_counter > 1000:
        #    break
    parse_file.close()

if __name__ == '__main__':
    main()
