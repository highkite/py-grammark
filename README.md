This is a python library, that implements the rules defined by grammark (https://github.com/markfullmer/grammark).
All credit goes to markfullmer.

The contributions of this work can be summarized as follows:

* Key words, that are used by the grammar rules are collected in JSON files. This makes it hopefully easier to manage expressions and the JSON files can be used in other projects.
* The grammar rules are defined in (informal) logic. It is presented in the next section of this README. This makes the workings of grammark more transparent. However, I reverse engineered those rules from the angular app and it is absolutely possible that I made mistakes.
* The different checks implemented by grammark, e.g., passive voice, wordiness, academic style..., are provided as functions in the Python package. The functions return the ratings, as proposed by grammark and offsets indicating the problematic positions.

# An (Informal) Definition of the Grammar Rules

In the following we define the workings of the different tools provided by grammark.

Thereby, $W$ represents the set of words, that is built by parsing the text provided by the user (see section *Parsing the Text* for a detailed discussion).
Furthermore, $|w|$ represents the size of word $w \in W$ and we use $w[a:b]$ for $a,b \in \mathbb{N}$ to represent substrings, where $a,b$ represent positions in the string, where the substring starts and ends, respectively.
$pre(w) \in W$ indicates the predecessing word, that occurs before $w$ in the original text provided by the user.
We write $upper(w)$ for $w \in W$ to denote the word $w$ where the first letter is capitalized.

Note that $w \in W$ represents not necessarily a single word, but can be also a sequence of words if we try to match several consecutive words.

We use $s(w)$ to denote the sentence, that contains the word $w \in W$ and $s(w)[i]$ to select words in the sentence by index $i \in \mathbb{N}$.

## Passive voice

Let $I$ be the set of irregulars and $H$ be the set of helpers with sets as defined in `src/resources/passive_voice.json`:

The passive voice check hits, if for a word $w \in W$

$(w[|w| - 1:|w|] = "ed" \lor w \in I) \land pre(w) \in H$

In text: Every word that ends with "ed" or is an irregular verb and the predecessing word is a helper word.

## Wordiness

Let $K$ be the set of keywords. It is constructed by the first elements of the set keywords in file `src/resources/wordiness.json`

The wordiness check hits, if for a word $w \in W$

$\forall k \in K: w = k \lor w = upper(k)$

In text: We look if one of the elements in $K$ occurs in the text. We do this also for the situation, that it has a capitalized first letter.

## Nominalizations

Let $E$ be the set of postfixes taken from the file `src/resources/normalizations.json`

The nominalization check hits if for a word $w \in W$

$\exists a,b \in \mathbb{N}: w[a:b] \in E \land |w| > 7$

In text: The rule checks if the word $w$ ends with a postfix contained in $E$ and if its length is greater than seven.

## Sentences

Let $K$ be the set of keywords as defined in file `src/resources/sentences.json`

The sentences check hits if for a word $w \in W$

$|s(w)| > 50 \lor s(w)[0] \in K$

Here $|s(w)|$ denotes the number of words in the sentence.

## Transitions

Let $K$ be the set of keywords from the file `src/resources/transitions.json`

The transition check hits, if for a word $w \in W$

$\forall k \in K: w = k \lor w = upper(k)$

In text: We look if one of the elements in $K$ occurs in the text. We do this also for the situation, that it has a capitalized first letter.

## Academic

Let $K$ be the set of keywords from the file `src/resources/academic.json`

The academic check hits, if for a word $w \in W$

$\forall k \in K: w = k \lor w = upper(k)$

In text: We look if one of the elements in $K$ occurs in the text. We do this also for the situation, that it has a capitalized first letter.

## Grammar

Let $K$ be the set of keywords from the file `src/resources/grammar.json`

The grammar check hits, if for a word $w \in W$

$\forall k \in K: w = k \lor w = upper(k)$

In text: We look if one of the elements in $K$ occurs in the text. We do this also for the situation, that it has a capitalized first letter.

## Egcorns

Let $K$ be the set of keywords from the file `src/resources/eggcorns.json`

The grammar check hits, if for a word $w \in W$

$\forall k \in K: w = k \lor w = upper(k)$

In text: We look if one of the elements in $K$ occurs in the text. We do this also for the situation, that it has a capitalized first letter.

## Parsing the Text

# Installation

Install package with pip:

```
pip install py-grammark
```

# Development

# Build

```
python3 -m build
```

# Run tests

```
python3 -m unittest tests.test_grammark.TestGrammark
```
