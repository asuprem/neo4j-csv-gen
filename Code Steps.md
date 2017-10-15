## `NOTES`

- `p/t/` denotes `path/to`. It has been shortened for readability

# Visual Genome Dataset

- `objects.json`        : Contains list of objects per image **[UNUSED]**
- `relationships.json`  : Contains relations per image (with their associated objects) **[UNUSED]**
- `scene_graphs.json`   : Contains scene graphs per image. Similar to relationships.json

# Scene graphs

- `[TYPE]_objects.vgm`
- `[TYPE]_relations.vgm`
- `[TYPE]_attributes.vgm`

`[TYPE]` refers to the contents of the scene graph files. `[TYPE]` can contain the following descriptors:

- **nano**   :    1000 scene graphs
- **small**  :  10,000 scene graphs
- **medium** :  50,000 scene graphs
- **large**  : 100,000 scene graphs
- **full**   : 108,000 scene graphs (ie. all scene graphs)

# <span style='color:white; background-color:olive;padding-left:20px;padding-right:20px'>Generate the Scene Graphs with:</span>

    python [neo_gen.py] [scene_graphs.json] [splitsize] [prefixes]

where:
- `[neo_gen.py]` is the path to `neo_gen.py`
- `[scene_graphs]` is the path to `scene_graphs.json`
- `[splitsize]` is a string denoting how to split the output files
    - `'1,10,f'` means create one file with `1` image, a second file with `10` images (inclusive of the first) and a third file with `all` images (inclusive of the first ten)
- `[prefixes]` is a string denoting names of the splits. Should have the same comma separated length as `splitsize`
    - with the above example, we can use `'nano,small,full'`

### Sample:

    python neo_gen.py scene_graphs.json '1,10,50,f' 'nano,small,medium,full'

# <span style='color:white; background-color:olive;padding-left:20px;padding-right:20px'>Remove quotes from generated VGM files</span>
    sed -i 's/\"//g' *.vgm

Note that this should be run within the folder where the `vgm` files are (these would be in the same directory where `neo_gen.py` is run).

# <span style='color:white; background-color:olive;padding-left:20px;padding-right:20px'>Extracting objects, object count, and unique objects with IDS</span>

    $ awk -F "\"*,\"*" '{print $2}' p/t/full_objects.vgm > p/t/object_list.vgm
    $ sort p/t/object_list.vgm -o p/t/object_list.vgm
    $ sed -i '/^$/d' p/t/object_list.vgm
    $ sqlite3 p/t/objects.db < [object_extractor_SQL.txt] > p/t/object_count.vgm
    $ sqlite3 p/t/objects.db < [object_synset_count_SQL.txt]

`[object_extractor_SQL]` is the path to the *object_extractor_SQL.txt* file. Similarly, `[object_synset_count_SQL]` is the path to the *object_synset_count_SQL.txt* file.

# <span style='color:white; background-color:olive;padding-left:20px;padding-right:20px'>Extracting relations, relation count, and unique relations with IDS</span>


    $ awk -F "\"*,\"*" '{print $4}' p/t/full_relations.vgm > p/t/relation_list.vgm
    $ sort p/t/relation_list.vgm -o p/t/relation_list.vgm
    $ sed -i '/^$/d' p/t/relation_list.vgm
    $ sqlite3 p/t/relations.db < [relation_extractor_SQL.txt] > p/t/relation_count.vgm
    $ sqlite3 p/t/relations.db < [relation_synset_count_SQL.txt]

`[relation_extractor_SQL]` is the path to the *relation_extractor_SQL.txt* file. Similarly, `[relation_synset_count_SQL]` is the path to the *relation_synset_count_SQL.txt* file.



# <span style='color:white; background-color:olive;padding-left:20px;padding-right:20px'>Generating full aggregate scene graph</span>

    $ python [reduced_relationship_gen.py] [scene_graphs.json] [aggregate_full]
    $ sort -u -t ',' -k1,1 -k2,2 -k3,3 aggregate_full.vgm -o aggregate_full.vgm

where:
- `[reduced_relationship_gen]` is the path to `reduced_relationship_gen.py`
- `[scene_graphs]` is the path to `scene_graphs.json`
- `[aggregate_full]` is the path to the `aggregate_full` file (the output file). Just the file name is required. The program will append the appropriate extension to the end.

### Sample:

    python p/t/reduced_relationship_gen.py p/t/scene_graphs.json p/t/aggregate_full


# <span style='color:white; background-color:olive;padding-left:20px;padding-right:20px'>Generating unique ids for aggregate relations</span>
    
    $ sqlite3 p/t/aggregate.db < p/t/aggregate_db_id_extractor.SQL > p/t/temp_count.vgm
    $ python lookup_creator.py p/t/scene_graphs.json p/t/aggregate_image_ids.vgm

where:
- `aggregate.db` is the aggregate database. It will be populated here.
- `temp_count.vgm` is the 'error' output for the discerning user.
- `lookup_creator.py` generates the json file `aggregate_image_ids.vgm`

### Sample:

    python lookup_creator.py p/t/scene_graphs.json p/t/aggregate_image_ids.vgm

# <span style='color:white; background-color:olive;padding-left:20px;padding-right:20px'>Generating SSAG, OSAG IDs</span>

    $ cut -d ',' -f1,2,4 p/t/aggregate_full.vgm  > p/t/subj_rel_groups.vgm
    $ sort -u -t ',' -k1,1 -k2,2 p/t/subj_rel_groups.vgm -o p/t/subj_rel_groups.vgm
    $ cut -d ',' -f1,3,4 p/t/aggregate_full.vgm  > p/t/obj_rel_groups.vgm
    $ sort -u -t ',' -k1,1 -k2,2 p/t/obj_rel_groups.vgm -o p/t/obj_rel_groups.vgm
    $ sqlite3 p/t/relations.db < p/t/subjrel_ids_SQL.txt > p/t/temptest.vgm
    $ sqlite3 p/t/relations.db < p/t/objrel_ids_SQL.txt > p/t/temptest.vgm

`temptext.vgm` can be deleted afterwards. It is used to provide integrity information to the discerning user.
# <span style='color:white; background-color:olive;padding-left:20px;padding-right:20px'>Generating Aggregate, SSAG, and OSAG</span>

    $ python [aggregate_graph.py] [aggregate_full.vgm] [aggregate] [ssag] [osag]

This will generate the following files:
- `aggregate_subj.vgm` : The complete aggregate graph with unique subject relations between nouns and predicates
- `aggregate_obj.vgm` : The complete aggregate graph with unique object relations between predicate and nouns
- `ssag_subj.vgm` : Subject-source aggregate graph. Unique subject relations. 
- `ssag_obj.vgm` : Subject-source aggregate graph. Nonunique object relations.
- `osag_subj.vgm` : Object-source aggregate graph. Nonunique subject relations.
- `osag_obj.vgm` : Object-source aggregate graph. Unique object relations.

### Sample:

    python p/t/aggregate_graph.py p/t/aggregate_full.vgm aggregate ssag osag

# <span style='color:white; background-color:olive;padding-left:20px;padding-right:20px'>Cleaning Aggregate, OSAG, SSAG</span>

    $ sort -u -t ',' -k1,1 -k2,2 p/t/aggregate_subj.vgm -o p/t/aggregate_subj.vgm
    $ sort -u -t ',' -k1,1 -k2,2 p/t/aggregate_obj.vgm -o p/t/aggregate_obj.vgm
    $ sort -u -t ',' -k1,1 -k2,2 p/t/ssag_subj.vgm -o p/t/ssag_subj.vgm
    $ sort -u -t ',' -k1,1 -k2,2 p/t/ssag_obj.vgm -o p/t/ssag_obj.vgm
    $ sort -u -t ',' -k1,1 -k2,2 p/t/osag_subj.vgm -o p/t/osag_subj.vgm
    $ sort -u -t ',' -k1,1 -k2,2 p/t/osag_obj.vgm -o p/t/osag_obj.vgm

# <span style='color:white; background-color:olive;padding-left:20px;padding-right:20px'>Importing Aggregate graphs into Neo4J</span>

    $ cat p/t/aggregate_generator_CQL.cypher | cypher-shell -u USERNAME -p PASSWORD
    $ cat p/t/ssag_generator_CQL.cypher | cypher-shell -u USERNAME -p PASSWORD
    $ cat p/t/osag_generator_CQL.cypher | cypher-shell -u USERNAME -p PASSWORD

NOTE: Neo4J must be running. 

# <span style='color:white; background-color:olive;padding-left:20px;padding-right:20px'>Importing scene graphs into Neo4J</span>

    $ cat p/t/full_graph.cypher | cypher-shell -u USERNAME -p PASSWORD
    $ cat p/t/nano_graph.cypher | cypher-shell -u USERNAME -p PASSWORD

NOTE: Neo4J must be running. 

