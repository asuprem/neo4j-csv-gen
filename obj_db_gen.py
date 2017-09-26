from __future__ import print_function
from shutil import copy2 as copy_func
import json, sys, pdb, os, time
#import sqlite3
import vgm_utils

#FOR RELATIONSHIPS, chunk size should be 2500. For objects, keep it small, like 500 or 1000
#format: python /path/to/obj_db_geb.py objects/relations.json objects/relationsips

_PUSH = '{'
_POP = '}'

def obj_update(obj_read, o_file, extract_type):
    j_obj = json.loads(obj_read)
    j_synsets =  [i['synsets'] for i in j_obj[extract_type]]
    synset_write=''
    for synset_list in j_synsets:
        if synset_list:
            for synset in synset_list:
                o_file.write(synset+'\n')

def main():
    start = time.time()
    # Set up the split characteristics, and the file names
    file_name = sys.argv[1]
    extract_type = sys.argv[2]
    chunk_size, find_counter = int(sys.argv[3]),0
    parse_file = open(file_name)
    #Read the first character and ignore
    parse_file.read(1)
    obj_read, stream_read, obj_counter = '','',0
    f_name = extract_type + '_synsets_all.vgm'
    o_file = open(f_name, 'w')
    o_file.close()
    o_file = open(f_name,'a+')
    # Delete all vgm files in current folder:
    
    #pdb.set_trace()
    
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
            obj_update(obj_read, o_file, extract_type)
            if find_counter%500 == 0:
                print("Valid object found: "+str(find_counter) +  '  at ' + str(int(time.time()-start)), end='\n')
            obj_read=''
        
        
        # Now if we hit the threshold, we close the file, copy it, open the new one, and continue on the new one.
        # code for file_logic
        
        #This exists for debugging purposes -> to early stop the files for quicker verification
    print("Valid object found: "+str(find_counter) +  '  at ' + str(int(time.time()-start)), end='\n')
    parse_file.close()
    o_file.close()



if __name__ == "__main__":
    main()