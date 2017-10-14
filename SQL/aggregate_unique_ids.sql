-- This will generate unique IDS for each unique relation. This will be stored in a DB, and then called when generating counts.
-- RUN this on aggregate.db

-- initial commands
.headers off
.separator ','

-- (a) Import data
-- [insert sql statement(s) below]
CREATE TABLE IF NOT EXISTS aggregate_list(
    subject_synset TEXT,
    relation_synset TEXT,
    object_synset TEXT,

);

.mode csv
.import object_list.vgm objects_list

SELECT synset, count(synset)
from objects_list
group by synset;
