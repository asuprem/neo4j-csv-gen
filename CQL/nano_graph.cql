create index on :nanoRelation(synset);
create index on :nanoObject(synset);
create index on :nanoObject(id);
create index on :nanoRelation(id);

using periodic commit 500
load csv from "file:///nano_objects.vgm" as line
create (a:nanoObject {id:toInteger(line[0]), synset:line[1], name:line[2], img:toInteger(line[3])});

using periodic commit 500
load csv from "file:///nano_attributes.vgm" as line with line
match (o:nanoObject {id:toInteger(line[0])}) with o,line
create (a:nanoAttribute {name:line[1]})-[:ATTR]->(o);

using periodic commit 500
load csv from "file:///nano_relations.vgm" as line
match (s:nanoObject {id:toInteger(line[1])}) with s,line
match  (o:nanoObject {id:toInteger(line[2])}) with s,o,line
create (s)-[:SUBJ]->(r:nanoRelation {id:toInteger(line[0]), synset:line[3], name:line[4], img:toInteger(line[5])})-[:OBJ]->(o);
