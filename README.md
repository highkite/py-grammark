This is a python library, that implements the rules defined by grammark (https://github.com/markfullmer/grammark).
All credit goes to markfullmer.

The contributions of this work can be summarized as follows:
* Key words, that are used by the grammar rules are collected in JSON files. This makes it hopefully easier to manage expressions and the JSON files can be used in other projects.
* The grammar rules are defined in (informal) logic. It is presented in the next section of this README. This makes the workings of grammark more transparent. However, I reverse engineered those rules from the angular app and it is absolutely possible that I made mistakes.
* The different checks implemented by grammark, e.g., passive voice, wordiness, academic style..., are provided as functions in the Python package. The functions return the ratings, as proposed by grammark and offsets indicating the problematic positions.

# An (Informal) Definition of the Grammar Rules

In the following we define the workings of the different tools provided by grammark.

## Passive voice

