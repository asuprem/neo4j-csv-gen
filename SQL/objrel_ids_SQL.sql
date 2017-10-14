-- initial commands
.headers off
.separator ','


DROP TABLE IF EXISTS temp_count;
CREATE TABLE temp_count(
    rel_id INTEGER,
    obj_id INTEGER,
    rel_synset TEXT
);

DROP TABLE IF EXISTS obj_rel;
CREATE TABLE obj_rel(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    obj_id INTEGER,
    rel_id INTEGER
);


CREATE INDEX objrel_subj on obj_rel(obj_id);
CREATE INDEX objrel_rel on obj_rel(rel_id);

.mode csv
.import obj_rel_groups.vgm temp_count

INSERT INTO obj_rel(obj_id,rel_id) SELECT obj_id,rel_id FROM temp_count;
DROP TABLE temp_count;

SELECT * FROM  obj_rel;

