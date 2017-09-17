# This code generates the csv file to import with neo4j for the Visual Genome Dataset.
# Command for running:
# [scene_graphs.json] is either scene_graphs.json from VisualGenome v4 or similarly structured file.
#['splitsize'] is a comma-separated string dnoting how to split the output files: '100,1000,f'
#['prefixes'] is a comma separated string for prefixes: 'nano, small, full'
# python /path/to/neo_gen.py path/to/[scene_graphs.json] ['splitsize'] ['prefixes']

from __future__ import print_function
import json, sys, pdb
_PUSH = '{'
_POP = '}'


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


def json_extractor(j_obj):
    j_obj = json.loads(j_obj)
    obj_integrity = {}
    rel_integrity = {}
    attr_integrity = {}
    for i in range(len(j_obj['objects'])):
        obj_integrity[j_obj['objects'][i]['object_id']] = [j_obj['objects'][i]['object_id'], \
                                                           j_obj['objects'][i]['synsets'], \
                                                           j_obj['objects'][i]['names'], \
                                                           (j_obj['objects'][i]['attributes'] if 'attributes' in j_obj['objects'][i] else [])]
    with open("objects_med.vgm", 'a+') as obj_file:
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
            with open("attributes_med.vgm", 'a+') as attr_file:
                
                    for attribute in obj_integrity[item][3]:
                        try:
                            attr_file.write((str(item) + ',' + \
                                        attribute + '\n').encode('ascii', 'ignore'))
                        except UnicodeEncodeError:
                            continue
            
    for i in range(len(j_obj['relationships'])):
            rel_integrity[j_obj['relationships'][i]['relationship_id']] = [j_obj['relationships'][i]['relationship_id'], \
                                                           j_obj['relationships'][i]['synsets'], \
                                                           j_obj['relationships'][i]['object_id'], \
                                                           j_obj['relationships'][i]['subject_id'], \
                                                           j_obj['relationships'][i]['predicate']]
    with open("relations_med.vgm", 'a+') as rel_file:
        for item in rel_integrity:
            try:
                rel_file.write( (str(item) + ',' + \
                                str(rel_integrity[item][3]) + ',' + \
                                str(rel_integrity[item][2]) + ',' + \
                                (rel_integrity[item][1][0] if rel_integrity[item][1] else '') + ',' + \
                                (rel_integrity[item][4] if rel_integrity[item][2] else '')+','+\
                                str(find_counter) + ',' + \
                                str(j_obj['image_id']) + '\n').encode('ascii', 'ignore'))
            except IndexError:
                continue
            except UnicodeEncodeError:
                continue

def main():

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
    chunk_size, find_counter, split_idx = 5000,0,0
    parse_file = open(file_name)
    #Read the first character and ignore
    parse_file.read(1)
    obj_read, stream_read, obj_counter = '','',0
    
    pdb.set_trace()

    while True:
        now_read=parse_file.read(chunk_size)
        parse_read = stream_read + (now_read if now_read else '')        
        # If there is nothing left to parse
        if not parse_read:
            break
        
        obj_counter, json_obj, stream_read  = par_check(obj_counter, parse_read, obj_read)
        obj_read = obj_read + json_obj

        if obj_counter == 0:
            find_counter+=1
            print("Valid object found: "+str(find_counter), end='\r')
            json_extractor(obj_read)        
            obj_read=''
        
        #This exists for debugging purposes -> to early stop the files for quicker verification
        # Now if we hit the threshold, we close the file, copy it, open the new one, and continue on the new one.
        if find_counter > 100:
            break
    parse_file.close()

if __name__ == '__main__':
    main()
