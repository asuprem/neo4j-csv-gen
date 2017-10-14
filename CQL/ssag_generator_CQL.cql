create index on :ssagObject(id);
create index on :ssagRelation(id);
create index on :ssagObject(synset);
create index on :ssagRelation(synset);

using periodic commit 500
load csv from "file:///aggregate_object_ids.vgm" as line
create (a:ssagObject {id:toInteger(line[0]), synset:line[1], name:line[1]});

using periodic commit 500
load csv from "file:///ssag_subj.vgm" as line
match (s:ssagObject {id:toInteger(line[0])})
create (s)-[:SUBJ]->(r:ssagRelation {id:toInteger(line[1]), synset:line[2]});

using periodic commit 500
load csv from "file:///ssag_obj.vgm" as line
match (s:ssagObject {id:toInteger(line[0])}),(r:ssagRelation {id:toInteger(line[1])})
create (r)-[:OBJ]->(s);

