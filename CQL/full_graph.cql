create index on :fullRelation(synset)
create index on :fullObject(synset)
create index on :fullObject(id)
create index on :fullRelation(id)

using periodic commit 500
load csv from "file:///full_objects.vgm" as line
create (a:fullObject {id:toInteger(line[0]), synset:line[1], name:line[2], img:toInteger(line[3])})

using periodic commit 500
load csv from "file:///full_attributes.vgm" as line with line
match (o:fullObject {id:toInteger(line[0])}) with o,line
create (a:fullAttribute {name:line[1]})-[:ATTR]->(o)

using periodic commit 500
load csv from "file:///full_relations.vgm" as line
match (s:fullObject {id:toInteger(line[1])}) with s,line
match  (o:fullObject {id:toInteger(line[2])}) with s,o,line
create (s)-[:SUBJ]->(r:fullRelation {id:toInteger(line[0]), synset:line[3], name:line[4], img:toInteger(line[5])})-[:OBJ]->(o)
