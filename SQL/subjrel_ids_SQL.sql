-- initial commands
.headers off
.separator ','


DROP TABLE IF EXISTS temp_count;
CREATE TABLE temp_count(
    rel_id INTEGER,
    obj_id INTEGER,
    rel_synset TEXT
);

DROP TABLE IF EXISTS subj_rel;
CREATE TABLE subj_rel(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subj_id INTEGER,
    rel_id INTEGER
);


CREATE INDEX subjrel_subj on subj_rel(subj_id);
CREATE INDEX subjrel_rel on subj_rel(rel_id);

.mode csv
.import subj_rel_groups.vgm temp_count

INSERT INTO subj_rel(subj_id,rel_id) SELECT obj_id,rel_id FROM temp_count;
DROP TABLE temp_count;

SELECT * FROM  subj_rel;

