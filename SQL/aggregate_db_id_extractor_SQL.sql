-- initial commands
.headers off
.separator ','


DROP TABLE IF EXISTS temp_count;
CREATE TABLE temp_count(
    rel_id INTEGER,
    subj_id INTEGER,
    obj_id INTEGER,
    rel_synset TEXT
);

DROP TABLE IF EXISTS aggregate_id;
CREATE TABLE aggregate_id(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subj_id INTEGER,
    obj_id INTEGER,
    rel_id INTEGER
);


CREATE INDEX aggregate_subj on aggregate_id(subj_id);
CREATE INDEX aggregate_obj on aggregate_id(obj_id);
CREATE INDEX aggregate_rel on aggregate_id(rel_id);

.mode csv
.import aggregate_full.vgm temp_count

INSERT INTO aggregate_id(subj_id,obj_id,rel_id) SELECT subj_id,obj_id,rel_id FROM temp_count;
DROP TABLE temp_count;

SELECT * FROM  aggregate_id;

