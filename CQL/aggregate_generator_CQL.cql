create index on :aggregateObject(id);
create index on :aggregateRelation(id);
create index on :aggregateObject(synset);
create index on :aggregateRelation(synset);

using periodic commit 500
load csv from "file:///aggregate_object_ids.vgm" as line
create (a:aggregateObject {id:toInteger(line[0]), synset:line[1], name:line[1]});

using periodic commit 500
load csv from "file:///aggregate_relation_ids.vgm" as line
create (a:aggregateRelation {id:toInteger(line[0]), synset:line[1], name:line[1]});

using periodic commit 500
load csv from "file:///aggregate_subj.vgm" as line
match (s:aggregateObject {id:toInteger(line[0])}), (r:aggregateRelation {id:toInteger(line[1])})
create (s)-[:SUBJ]->(r);

using periodic commit 500
load csv from "file:///aggregate_obj.vgm" as line
match (s:aggregateObject {id:toInteger(line[0])}),(r:aggregateRelation {id:toInteger(line[1])})
create (r)-[:OBJ]->(s);


