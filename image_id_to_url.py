from __future__ import print_function
from shutil import copy2 as copy_func
import json, sys, pdb, os, time
#import sqlite3
import vgm_utils

#FOR RELATIONSHIPS, chunk size should be 2500. For objects, keep it small, like 500 or 1000
#format: python image_data.json 50

_PUSH = '{'
_POP = '}'

def obj_update(obj_read,image_urls):
    if obj_read:
        j_obj = json.loads(obj_read)
        image_urls[j_obj['image_id']] = j_obj['url'].encode('ascii')


def main():
    start = time.time()
    # Set up the split characteristics, and the file names
    file_name = sys.argv[1]
    chunk_size, find_counter = int(sys.argv[2]),0
    parse_file = open(file_name)
    #Read the first character and ignore
    parse_file.read(1)
    obj_read, stream_read, obj_counter = '','',0
    
    # Delete all vgm files in current folder:
    
    #pdb.set_trace()
    image_urls={}
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
            obj_update(obj_read, image_urls)
            if find_counter%10000 == 0:
                print("Valid object found: "+str(find_counter) +  '  at ' + str(int(time.time()-start)), end='\n')
            obj_read=''
        
        # Now if we hit the threshold, we close the file, copy it, open the new one, and continue on the new one.
        # code for file_logic
        
        #This exists for debugging purposes -> to early stop the files for quicker verification
    print("Valid object found: "+str(find_counter) +  '  at ' + str(int(time.time()-start)), end='\n')
    parse_file.close()
    #o_file.close()
    #pdb.set_trace()
    #with open(sys.argv[3],'w') as write_file:
    #    json.dump(image_urls,write_file)

    while 1:
        image_to_find =  int(raw_input("Image ID:  "))
        if image_to_find in image_urls:
            print (image_urls[image_to_find]+'\n')
        else:
            print ("Uh oh, something went wrong\n")

if __name__ == "__main__":
    main()