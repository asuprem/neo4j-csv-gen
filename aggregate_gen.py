from __future__ import print_function
import sqlite3, operator
import vgm_utils
import json , sys, pdb, time

conn_obj = sqlite3.connect('../ExtractedData/' + 'objects' + '.db')
conn_rel = sqlite3.connect('../ExtractedData/' + 'relations' + '.db')
rel_curs = conn_rel.cursor()
obj_curs = conn_obj.cursor()

object_ids = dict(obj_curs.execute('Select synset,id from synset_count'))
relation_ids = dict(rel_curs.execute('Select synset,id from synset_count'))


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
    
    with open(aggregate_name, 'a+') as aggregate_file:
        for item in rel_integrity:
            aggregate_file.write(','.join([str(tup) for tup in item]) + ',' + rel_integrity[item] + '\n')


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
