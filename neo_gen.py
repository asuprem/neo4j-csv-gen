# This code generates the csv file to import with neo4j for the Visual Genome Dataset.
# Command for running:
# [scene_graphs.json] is either scene_graphs.json from VisualGenome v4 or similarly structured file.
#['splitsize'] is a comma-separated string dnoting how to split the output files: '100,1000,f'
#['prefixes'] is a comma separated string for prefixes: 'nano, small, full'
# python /path/to/neo_gen.py path/to/[scene_graphs.json] ['splitsize'] ['prefixes']

from __future__ import print_function
from shutil import copy2 as copy_func
import json, sys, pdb, os, time
import vgm_utils
_PUSH = '{'
_POP = '}'


def json_extractor(j_obj, split_name, split_idx):
    rel_file_name   = split_name[split_idx] +   '_relations.vgm'
    obj_file_name   = split_name[split_idx] +   '_objects.vgm'
    attr_file_name  = split_name[split_idx] +   '_attributes.vgm'

    j_obj = json.loads(j_obj)

    obj_integrity   = {}
    rel_integrity   = {}
    rel_integrity_tuple = {}
    attr_integrity  = {}

    for i in range(len(j_obj['objects'])):
        obj_integrity[j_obj['objects'][i]['object_id']] = [j_obj['objects'][i]['object_id'], \
                                                           j_obj['objects'][i]['synsets'], \
                                                           j_obj['objects'][i]['names'], \
                                                           (j_obj['objects'][i]['attributes'] if 'attributes' in j_obj['objects'][i] else [])]
    with open(obj_file_name, 'a+') as obj_file:
        for item in obj_integrity:
            try:
                obj_file.write( (str(item) + ',' + \
                                (obj_integrity[item][1][0] if obj_integrity[item][1] else '') + ',' + \
                                (obj_integrity[item][2][0] if obj_integrity[item][2] else '') + ',' + \
                                str(j_obj['image_id']) + '\n').encode('ascii', 'ignore'))
            except IndexError:
                continue
            except UnicodeEncodeError:
                continue
            with open(attr_file_name, 'a+') as attr_file:
                
                    for attribute in obj_integrity[item][3]:
                        try:
                            attr_file.write((str(item) + ',' + \
                                        attribute + '\n').encode('ascii', 'ignore'))
                        except UnicodeEncodeError:
                            continue
            
    for i in range(len(j_obj['relationships'])):
            in_tuple = (tuple(j_obj['relationships'][i]['synsets']), \
                        j_obj['relationships'][i]['object_id'], \
                        j_obj['relationships'][i]['subject_id'], \
                        j_obj['relationships'][i]['predicate'])
            rel_integrity_tuple[in_tuple] = j_obj['relationships'][i]['relationship_id']

    
    with open(rel_file_name, 'a+') as rel_file:
        for item in rel_integrity_tuple:
            try:
                rel_file.write( (str(rel_integrity_tuple[item]) + ',' + \
                                str(item[2]) + ',' + \
                                str(item[1]) + ',' + \
                                (item[0][0] if item[0] else '') + ',' + \
                                (item[3] if item[3] else '')+','+\
                                #str(find_counter) + ',' + \
                                str(j_obj['image_id']) + '\n').encode('ascii', 'ignore'))
    
            except IndexError:
                pdb.set_trace()
            except UnicodeEncodeError:
                continue

def main():
    start = time.time()
    # Set up the split characteristics, and the file names
    file_name = sys.argv[1]
    if len(sys.argv) == 2:
        split_size = ['f']
        split_name=['full']
    if len(sys.argv) == 3:
        split_size=sys.argv[2].split(',')
        split_name=sys.argv[2].split(',')
    if len(sys.argv) == 4:
        split_size=sys.argv[2].split(',')
        split_name=sys.argv[3].split(',')
        assert(len(split_size) == len(split_name))
    split_size = [int(item) if item.isdigit() else item for item in split_size]
    chunk_size, find_counter, split_idx = 5000,0,0
    parse_file = open(file_name)
    #Read the first character and ignore
    parse_file.read(1)
    obj_read, stream_read, obj_counter = '','',0
    # Delete all vgm files in current folder:
    #filelist = [ f for f in os.listdir(".") if f.endswith(".vgm") ]
    #for f in filelist:
    #    os.remove(f)
    
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
            if find_counter%500 == 0:
                print("Valid object found: "+str(find_counter) +  '  at ' + str(int(time.time()-start)), end='\n')
            json_extractor(obj_read, split_name, split_idx)        
            obj_read=''
        
        
        # Now if we hit the threshold, we close the file, copy it, open the new one, and continue on the new one.
        # code for file_logic
        if split_size[split_idx] != 'f' and find_counter == split_size[split_idx]:
            #i.e. we need to copy the existing file into a new one
            base_file = ['_relations.vgm', '_objects.vgm', '_attributes.vgm']
            src_file = [split_name[split_idx] + f_name for f_name in base_file]
            dst_file = [split_name[split_idx+1] + f_name for f_name in base_file]

            for file_idx,file_items in enumerate(src_file):
                copy_func(src_file[file_idx], dst_file[file_idx])
            split_idx+=1
        #This exists for debugging purposes -> to early stop the files for quicker verification
        #if find_counter > 1000:
        #    break
    parse_file.close()

if __name__ == '__main__':
    main()
