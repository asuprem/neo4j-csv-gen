create index on :osagObject(id);
create index on :osagRelation(id);
create index on :osagObject(synset);
create index on :osagRelation(synset);

using periodic commit 500
load csv from "file:///aggregate_object_ids.vgm" as line
create (a:osagObject {id:toInteger(line[0]), synset:line[1], name:line[1]});

using periodic commit 500
load csv from "file:///osag_obj.vgm" as line
match (s:osagObject {id:toInteger(line[0])})
create (r:osagRelation {id:toInteger(line[1]), synset:line[2]})-[:OBJ]->(s);

using periodic commit 500
load csv from "file:///osag_subj.vgm" as line
match (s:osagObject {id:toInteger(line[0])}),(r:osagRelation {id:toInteger(line[1])})
create (s)-[:SUBJ]->(r);
