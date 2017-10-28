from __future__ import print_function
import sqlite3, operator
import vgm_utils
import json , sys, pdb, time, os
#python lookup_creator.py ../ExtractedData/scene_graphs.json ../ExtractedData/aggregate_image_ids.vgm

conn_obj = sqlite3.connect('../ExtractedData/' + 'objects' + '.db')
conn_rel = sqlite3.connect('../ExtractedData/' + 'relations' + '.db')
conn_agg = sqlite3.connect('../ExtractedData/' + 'aggregate' + '.db')
rel_curs = conn_rel.cursor()
obj_curs = conn_obj.cursor()
aggregate_curs = conn_agg.cursor()


# these are global uniques
object_ids = dict(obj_curs.execute('Select synset,id from synset_count'))
relation_ids = dict(rel_curs.execute('Select synset,id from synset_count'))
temp_aggregate_ids = aggregate_curs.execute('Select rel_id,subj_id,obj_id,id from aggregate_id').fetchall()
aggregate_ids = {(item[0],item[1],item[2]):item[3] for item in temp_aggregate_ids}
temp_aggregate_ids = None


def json_extractor(obj_read, file_dict):
    pdb.set_trace()
    j_obj = json.loads(obj_read)
    obj_integrity = {}
    rel_integrity = {}
    #Get the new IDS for the objects.
    for i in range(len(j_obj['objects'])):
        if j_obj['objects'][i]['synsets'] and j_obj['objects'][i]['synsets'][0] in object_ids:
            obj_integrity[j_obj['objects'][i]['object_id']] = object_ids[j_obj['objects'][i]['synsets'][0]]
            
    pdb.set_trace()
    for i in range(len(j_obj['relationships'])):
        if j_obj['relationships'][i]['synsets'] and j_obj['relationships'][i]['synsets'][0] in relation_ids:
            if j_obj['relationships'][i]['subject_id'] in obj_integrity and j_obj['relationships'][i]['object_id'] in obj_integrity:
                # Here we are converting the subject/object IDs to their aggregate_ids (i.e. 1 id for each each unique subj/obj)
                in_tuple = (relation_ids[j_obj['relationships'][i]['synsets'][0]], \
                            obj_integrity[j_obj['relationships'][i]['subject_id']], \
                            obj_integrity[j_obj['relationships'][i]['object_id']])
                # Need to prevent the overwrite, i.e. if the same relation is seen, append, not replace
                if in_tuple in rel_integrity:
                    pdb.set_trace()
                rel_integrity[in_tuple] = aggregate_ids[in_tuple]
    # Here we need to 
    pdb.set_trace()
    for item in rel_integrity:
        #file_path = os.path.join(aggregate_folder_name,str(rel_integrity[item])+'.vgmImage')
        if rel_integrity[item] not in file_dict:
            file_dict[rel_integrity[item]] = [str(j_obj['image_id'])]
        else:
            file_dict[rel_integrity[item]].append(str(j_obj['image_id']))

        #with open(file_path, 'a+') as aggregate_file:
        #file_dict[file_path].write(str(j_obj['image_id']) + '\n')
    pdb.set_trace()




def main():
    file_dict={}
    start = time.time()
    #path to scene_graphs.json
    file_name = sys.argv[1]
    #name of output dump file
    aggregate_file_name = sys.argv[2]
    chunk_size, find_counter = 5000,0
    parse_file = open(file_name)
    #Read the first character and ignore
    parse_file.read(1)
    obj_read, stream_read, obj_counter = '','',0
    # Delete all vgm files in current folder:
    #if not os.path.exists(aggregate_folder_name):
    #    os.makedirs(aggregate_folder_name)
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
                #break
                print("Valid object found: "+str(find_counter) +  '  at ' + str(int(time.time()-start)), end='\n')
            json_extractor(obj_read, file_dict)        
            obj_read=''

        #This exists for debugging purposes -> to early stop the files for quicker verification
        #if find_counter > 1000:
        #    break
    parse_file.close()
    
    with open(aggregate_file_name, 'w') as out_file:
        json.dump(file_dict, out_file)

    #for item in file_dict:
    #    file_path = os.path.join(aggregate_folder_name,str(item)+'.vgmImage')
    #    with open(file_path,'w') as file_write:
    #        file_write.write('\n'.join(file_dict[item]))
    
if __name__ == '__main__':
    main()
