-- initial commands
.headers off
.separator ','

-- (a) Import data
-- [insert sql statement(s) below]
CREATE TABLE IF NOT EXISTS relations_list(
    synset TEXT
);

.mode csv
.import relation_list.vgm relations_list

SELECT synset, count(synset)
from relations_list
group by synset;
