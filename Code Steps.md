# Visual Genome Dataset

- `objects.json`        : Contains list of objects per image **[UNUSED]**
- `relationships.json`  : Contains relations per image (with their associated objects) **[UNUSED]**
- `scene_graphs.json`   : Contains scene graphs per image. Similar to relatioships.json

# Scene graphs

- `[TYPE]_objects.vgm`
- `[TYPE]_relations.vgm`
- `[TYPE]_attributes.vgm`

`[TYPE]` refers to the contents of the scene graph files. `[TYPE]` contains the following descriptors:

- **nano**   :    1000 scene graphs
- **small**  :  10,000 scene graphs
- **medium** :  50,000 scene graphs
- **large**  : 100,000 scene graphs
- **full**   : 108,000 scene graphs (ie. all scene graphs)

### <span style='color:white; background-color:olive;padding-left:20px;padding-right:20px'>Generate the Scene Graphs with:</span>

    python [neo_gen] [scene_graphs] [splitsize] [prefixes]

where:
- `[neo_gen.py]` is the path to `neo_gen.py`
- `[scene_graphs]` is the path to `scene_graphs.json`
- `[splitsize]` is a string denoting how to split the output files
    - `'1,10,f'` means create one file with `1` image, a second file with `10` images (inclusive of the first) and a third file with `all` images (inclusive of the first ten)
- `[prefixes]` is a string denoting names of the splits. Should have the same comma separated length as `splitsize`
    - with the above example, we can use `'nano,small,full'`

### Sample:

    python ../neo_gen scene_graphs.json '1,10,50,f' 'nano,small,medium,full'

### <span style='color:white; background-color:olive;padding-left:20px;padding-right:20px'>Remove quotes from generated VGM files</span>
    sed -i 's/\"//g' *.vgm

### <span style='color:white; background-color:olive;padding-left:20px;padding-right:20px'>Extracting objects, object count, and unique objects with IDS</span>

    $ awk -F "\"*,\"*" '{print $2}' path/to/full_objects.vgm > path/to/object_list.vgm
    $ sort object_list.vgm -o object_list.vgm
    sed -i '/^$/d' object_list.vgm
    $ sqlite3 objects.db < object_extractor_SQL.txt > object_count.vgm
    $ sqlite3 objects.db < object_synset_count_SQL.txt

### <span style='color:white; background-color:olive;padding-left:20px;padding-right:20px'>Extracting relations, relation count, and unique relations with IDS</span>


    $ awk -F "\"*,\"*" '{print $4}' path/to/full_relations.vgm > path/to/relation_list.vgm
    $ sort relation_list.vgm -o relation_list.vgm
    $ sed -i '/^$/d' relation_list.vgm
    $ sqlite3 relations.db < relation_extractor_SQL.txt > relation_count.vgm
    $ sqlite3 relations.db < relation_synset_count_SQL.txt

### <span style='color:white; background-color:olive;padding-left:20px;padding-right:20px'>Generating aggregate scene graph</span>

    $ python path/to/aggregate_gen.py path/to/scene_graphs.json path/to/aggregate_graph
    $ sort -u -t ',' -k1,1 -k2,2 -k3,3 aggregate_graph.vgm -o aggregate_graph.vgm


# <span style='color:white; background-color:olive;padding-left:20px;padding-right:20px'>Importing into Neo4J</span>
```
:schema
match (n) return distinct labels(n)


create index on :nanoRelation(synset)
create index on :nanoObject(synset)
create index on :nanoObject(id)
create index on :nanoRelation(id)

using periodic commit 500
load csv from "file:///nano_objects.vgm" as line
create (a:nanoObject {id:toInteger(line[0]), synset:line[1], name:line[2], img:toInteger(line[3])})

using periodic commit 500
load csv from "file:///nano_attributes.vgm" as line
match (o:nanoObject {id:toInteger(line[0])})
create (a:nanoAttribute {name:line[1]})-[:ATTR]->(o)

using periodic commit 500
load csv from "file:///nano_relations.vgm" as line
match (s:nanoObject {id:toInteger(line[1])}), (o:nanoObject {id:toInteger(line[2])})
create (s)-[:SUBJ]->(r:nanoRelation {id:toInteger(line[0]), synset:line[3], name:line[4], img:toInteger(line[5])})-[:OBJ]->(o)
```


--
```
aggregateRelation
aggregateObject

create index on :aggregateRelation(synset)
create index on :aggregateObject(synset)
create index on :aggregateObject(id)
create index on :aggregateRelation(id)

using periodic commit 500
load csv from "file:///aggregate_object_ids.vgm" as line
create (a:aggregateObject {id:toInteger(line[0]), synset:line[1], name:line[1]})

using periodic commit 500
load csv from "file:///aggregate_relation_ids.vgm" as line
create (a:aggregateRelation {id:toInteger(line[0]), synset:line[1], name:line[1]})

using periodic commit 500
load csv from "file:///aggregate_graph.vgm" as line
match (s:aggregateObject {id:toInteger(line[1])}), 
(o:aggregateObject {id:toInteger(line[2])}), 
(r:aggregateRelation{id:toInteger(line[0])}) 
create (s)-[:SUBJ]->(r)-[:OBJ]->(o)
```
---
```
create index on :fullRelation(synset)
create index on :fullObject(synset)
create index on :fullObject(id)
create index on :fullRelation(id)

using periodic commit 500
load csv from "file:///full_objects.vgm" as line
create (a:fullObject {id:toInteger(line[0]), synset:line[1], name:line[2], img:toInteger(line[3])})

using periodic commit 500
load csv from "file:///full_attributes.vgm" as line
match (o:fullObject {id:toInteger(line[0])})
create (a:fullAttribute {name:line[1]})-[:ATTR]->(o)

using periodic commit 500
load csv from "file:///full_relations.vgm" as line
match (s:fullObject {id:toInteger(line[1])}), (o:fullObject {id:toInteger(line[2])})
create (s)-[:SUBJ]->(r:fullRelation {id:toInteger(line[0]), synset:line[3], name:line[4], img:toInteger(line[5])})-[:OBJ]->(o)
```
--
```
match (n:aggregateObject {synset:'man.n.01'}),(m:aggregateObject {synset:'woman.n.01'})
return (n)-[:SUBJ]->(:aggregateRelation)-[:OBJ]->(m)