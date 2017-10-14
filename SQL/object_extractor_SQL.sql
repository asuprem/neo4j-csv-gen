-- initial commands
.headers off
.separator ','

-- (a) Import data
-- [insert sql statement(s) below]
CREATE TABLE IF NOT EXISTS objects_list(
    synset TEXT
);

.mode csv
.import object_list.vgm objects_list

SELECT synset, count(synset)
from objects_list
group by synset;
