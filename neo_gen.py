from __future__ import print_function
import json, sys
_PUSH = '{'
_POP = '}'

file_name = sys.argv[1]
chunk_size = 5000
find_counter = 0
parse_file = open(file_name)
#Read the first character and ignore
parse_file.read(1)
obj_read = ''
stream_read = ''
obj_counter = 0


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
    for i in range(len(j_obj['objects'])):
        obj_integrity[j_obj['objects'][i]['object_id']] = [j_obj['objects'][i]['object_id'], \
                                                           j_obj['objects'][i]['synsets'], \
                                                           j_obj['objects'][i]['names']]
    with open("objects.vgm", 'a+') as obj_file:
        for item in obj_integrity:
            try:
                obj_file.write( (str(item) + ',' + \
                                (obj_integrity[item][1][0] if obj_integrity[item][1] else '') + ',' + \
                                (obj_integrity[item][2][0] if obj_integrity[item][2] else '') + '\n').encode('ascii', 'ignore'))
            except IndexError:
                continue
            except UnicodeEncodeError:
                continue
    
    for i in range(len(j_obj['relationships'])):
            rel_integrity[j_obj['relationships'][i]['relationship_id']] = [j_obj['relationships'][i]['relationship_id'], \
                                                           j_obj['relationships'][i]['synsets'], \
                                                           j_obj['relationships'][i]['object_id'], \
                                                           j_obj['relationships'][i]['subject_id'], \
                                                           j_obj['relationships'][i]['predicate']]
    with open("relations.vgm", 'a+') as rel_file:
        for item in rel_integrity:
            rel_file.write( (str(item) + ',' + \
                            str(rel_integrity[item][3]) + ',' + \
                            str(rel_integrity[item][2]) + ',' + \
                            (rel_integrity[item][1][0] if rel_integrity[item][1] else '') + ',' + \
                            (rel_integrity[item][4] if rel_integrity[item][2] else '')+','+\
                            str(find_counter) + '\n').encode('ascii', 'ignore'))
    

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
parse_file.close()