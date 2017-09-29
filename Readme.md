# Python files

## `vgm_utils.py`
**vgm_utils.py** contains several utility functions that are used in the other files. 

## `aggregate_gen.py`
**aggregate_gen.py** generates the aggregate graph files for importing into Neo4j. It requires two _sqlite3_ databases named *objects.db* and *relations.db*. They contain:

- `synset_count` in _objects.db_ : Contains counts for (more importantly) each unique noun synset present in the Visual Genome dataset, as well as their unique IDs,. These unique noun synsets are imported into a python `dict` for rapid ID assignment.

- `synset_count` in _relations.db_ : Contains counts for (more importantly) each unique relation/predicate synset present in the Visual Genome dataset, as well as their unique IDs,. These unique predicate synsets are imported into a python `dict` for rapid ID assignment.

The syntax for running the program is:

    python [aggregate_path] [scene_path] [aggregate_path]
    
where
- `aggregate_path` is the path to the *aggregate_gen.py* file
- `scene_path` is the path to the *scene_graphs.json* file from the Visual Genome Dataset
- `out_path` is the name of the output file. Should be `aggregate_graph.vgm`


## `json_explorer.py`
**json_explorer.py** is used for streaming json files (in the same way it is implemented in `vgm_utils`) for prototyping and testing purposes.

## `neo_gen.py`
This generates the requisite small and large graphs for the database. 


## `synset_all_gen.py`
This generates files for all synsets. NEED TO EDIT
MAY NOT BE NECESSARY