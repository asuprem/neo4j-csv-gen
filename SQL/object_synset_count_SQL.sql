-- initial commands
.headers off
.separator ','

-- (a) Import data
-- [insert sql statement(s) below]
DROP TABLE IF EXISTS temp_count;
CREATE TABLE temp_count(
    synset TEXT,
    count INTEGER
);

DROP TABLE IF EXISTS synset_count;
CREATE TABLE synset_count(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
	synset TEXT,
    count INTEGER
);

CREATE INDEX obj_count_index on synset_count(synset);

.mode csv
.import object_count.vgm temp_count

INSERT INTO synset_count(synset,count) SELECT * FROM temp_count;
DROP TABLE temp_count;
