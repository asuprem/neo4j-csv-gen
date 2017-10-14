match (o:aggregateObject)-[:SUBJ]->(r:aggregateRelation) where r.synset='pull.v.01' return o;


match (r:aggregateRelation)-[:OBJ]->(o:aggregateObject) where r.synset='pull.v.01' return o;
