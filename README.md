# BLEU4Python
A light-weight python version of moses BLEU.

## Use Python Now
Moses version of BLEU calculation is widely used in academic researches and well accepted by scholarly community. As python seems to be the main force of deep learning development language, people may want the python version of this algorithm, which performs exactly the same way with the perl one.

Here is what you are looking for. A python code to work the same way as the moses' `multi-bleu.perl`. What's more, it can also be used as a module of python. Just `import bleu` and use `bleu.corpus_bleu`, etc. to do your work in detail.

## Features
* Can be used like moses BLEU
* Perform well in python 2&3
* Easily extend to BLEU-n score
* Call it in python code without creating files
* A fast realization of timestep-concerned sentence bleu

## How to Use
* If there are files you want to test:
    * `python multi_bleu.py [-h] [-hyp PATH_OF_HYPOTHESIS][-ref PATH_OF_REFERENCES [REFERENCES_1, REFERENCES_2, REFERENCES_3 ...]]`
    * There should be only **ONE** hypothesis file and **MORE THAN ZERO** reference file(s).
    * This will print to screen the BLEU scores like `BLEU = 48.39, 76.9/56.0/42.1/32.0 (BP=0.986, ratio=0.986, hyp_len=19588, ref_len=19865)`. Just same as moses.
* If you want to use in python code:
    * `import bleu`
    * If not specified, all the `hypothesis` should be a 1-dimension string list, and all the `references` should be a 2-dimension string list.
    * `bleu.bleu_count(hypothesis, references, max_n=4)` does the most important count work for BLEU. It returns `clip_count (correct), count (total), len_hyp, len_ref(sum of closest_length)`
    * `bleu.corpus_bleu(hypothesis, references, max_n=4)` does the complete BLEU calculation. It returns `BLEU([final bleu, p_1, p_2, ..., p_max_n]), additional message([BP, ratio, hyp_len, ref_len]) `
    * `bleu.incremental_bleu_count(hypothesis, references, max_n=4)` does an incremental count for BLEU, which means it will return the correct count for every timestep(prefix) of every hypothesis.
    * `bleu.incremental_sent_bleu(hypothesis, references, max_n=4)` does the bleu calculation work according to the result of `bleu.incremental_bleu_count`. And return all the bleu scores according to the timestep(prefix). **ATTENTION**: In this function, `hypothesis` should be a string and `references` should be a string list.
    * `bleu.incremental_test_corpus_bleu(hypothesis, references, max_n=4)` is just a test function for `bleu.incremental_bleu_count`. However, it behaves the same way as `bleu.corpus_bleu`, except for more time(a little) and memories.

## Something Wrong?
* Make sure your files are UTF-8 formatted. And you should convert all your strings to unicode before calling any of the above functions.
* If there is any Error (Exception) Message, Read it.
* Contact the author via Issues or E-mail.

**Note:** ALL distributions and uses should refer to this repository.
