from __future__ import print_function
from shutil import copy2 as copy_func
import json, sys, pdb, os, time
#import sqlite3
import vgm_utils

_PUSH = '{'
_POP = '}'

'''
def par_iterate(par_i_str):
    for idx,item in enumerate(par_i_str):
        if item == '{':
            return par_i_str[idx:]
    return ''

def par_check(i_counter, i_str, obj_read):
    # This code checsk aprenthesis and returns a complete json object for extraction
    if not obj_read:
        #i.e. we are starting again, so there may be gaps:
        i_str = par_iterate(i_str)
    for idx, item in enumerate(i_str):
        if item == _PUSH:
            i_counter+=1
        if item == _POP:
            i_counter-=1
        if i_counter == 0:
            try:
                temp_json = json.loads(obj_read+i_str[:idx+1])
                return i_counter, i_str[:idx+1], par_iterate(i_str[idx+1:])
            except ValueError:
                i_counter+=1
    return i_counter, i_str, ''
'''
def obj_update(obj_read, o_file):
    j_obj = json.loads(obj_read)
    j_synsets =  [i['synsets'] for i in j_obj[extract_type]]
    synset_write=''
    for synset_list in j_synsets:
        for synset in synset_list:
            o_file.write(synset+'\n')

def main():
    start = time.time()
    # Set up the split characteristics, and the file names
    file_name = sys.argv[1]
    extract_type = sys.argv[2]
    chunk_size, find_counter = 5000,0
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
    parse_file.close()
    o_file.close()



if __name__ == "__main__":
    main()