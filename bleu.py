#coding: UTF-8
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import argparse
import os
import math
import codecs
parser = argparse.ArgumentParser(
    description="Calculate BLEU scores for the input hypothesis and reference files")
parser.add_argument(
    "-hyp",
    nargs=1,
    dest="pf_hypothesis",
    type=str,
    help="The path of the hypothesis file.")
parser.add_argument(
    "-ref",
    nargs='+',
    dest="pf_references",
    type=str,
    help="The path of the references files.")
args = parser.parse_args()




def bleu_count(hypothesis, references, max_n=4):
    ret_len_hyp = 0
    ret_len_ref = 0
    ret_clip_count = [0]*max_n
    ret_count = [0]*max_n
    for i in range(len(hypothesis)):
        hyp, ref = hypothesis[i], references[i]
        x = hyp.split()
        y = [r.split() for r in ref]
        x_len = len(x)
        y_len = [len(s) for s in y]
        n_ref = len(ref)

        closest_diff = 9999
        closest_length = 9999
        ref_ngram = dict()

        for i in range(n_ref):
            diff = abs(y_len[i]-x_len)
            if diff < closest_diff:
                closest_diff = diff
                closest_length = y_len[i]
            elif diff==closest_diff and y_len[i] < closest_length:
                closest_length = y_len[i]

            for n in range(max_n):
                sent_ngram = dict()
                for st in range(0, y_len[i]-n):
                    ngram = "%d"%(n+1)
                    for k in range(n+1):
                        j = st+k
                        ngram += " %s"%(y[i][j])
                    if ngram not in sent_ngram:
                        sent_ngram[ngram]=0
                    sent_ngram[ngram]+=1
                for ngram in sent_ngram.keys():
                    if ngram not in ref_ngram or ref_ngram[ngram]<sent_ngram[ngram]:
                        ref_ngram[ngram] = sent_ngram[ngram]

        ret_len_hyp += x_len
        ret_len_ref += closest_length

        for n in range(max_n):
            hyp_ngram = dict()
            for st in range(0, x_len-n):
                ngram = "%d"%(n+1)
                for k in range(n+1):
                    j = st+k
                    ngram += " %s"%(x[j])
                if ngram not in hyp_ngram:
                    hyp_ngram[ngram]=0
                hyp_ngram[ngram]+=1
            for ngram in hyp_ngram.keys():
                if ngram in ref_ngram:
                    ret_clip_count[n] += min(ref_ngram[ngram], hyp_ngram[ngram])
                ret_count[n] += hyp_ngram[ngram]

    return ret_clip_count, ret_count, ret_len_hyp, ret_len_ref

def corpus_bleu(hypothesis, references, max_n=4):
    assert(len(hypothesis) == len(references))
    clip_count, count, total_len_hyp, total_len_ref = bleu_count(hypothesis, references, max_n=max_n)
    brevity_penalty = 1.0
    bleu_scores = []
    bleu = 0
    for n in range(max_n):
        if count[n]>0:
            bleu_scores.append(clip_count[n]/count[n])
        else:
            bleu_scores.append(0)
    if total_len_hyp < total_len_ref:
        brevity_penalty = math.exp(1 - total_len_ref/total_len_hyp)
    def my_log(x):
        if x == 0:
            return -9999999999.0
        elif x < 0:
            raise Exception("Value Error")
        return math.log(x)
    log_bleu = 0.0
    for n in range(max_n):
        log_bleu += my_log(bleu_scores[n])
    bleu = brevity_penalty*math.exp(log_bleu / float(max_n))
    return [bleu]+bleu_scores, [brevity_penalty, total_len_hyp/total_len_ref, total_len_hyp, total_len_ref]

def file_exist(pf):
    if os.path.isfile(pf):
        return True
    return False

if args.pf_hypothesis!=None or args.pf_references!=None:
    if args.pf_hypothesis==None:
        raise Exception("Missing references files...")
    if args.pf_references==None:
        raise Exception("Missing hypothesis files...")

    n = None
    data = []
    for pf in args.pf_hypothesis+args.pf_references:
        if not file_exist(pf):
            raise Exception("File Not Found: %s"%(pf))
        f = codecs.open(pf, encoding="utf-8")
        data.append(f.readlines())
        if n==None:
            n = len(data[-1])
        elif n != len(data[-1]):
            raise Exception("Not parrallel: %s %d-%d"%(pf, n, len(data[-1])))
        f.close()

    hyp_data = data[0]
    ref_data = list(map(list, zip(*data[1:])))

    bleu, addition = corpus_bleu(hyp_data, ref_data)

    print("BLEU = %.2f, %.1f/%.1f/%.1f/%.1f (BP=%.3f, ratio=%.3f, hyp_len=%d, ref_len=%d)"%(bleu[0]*100, bleu[1]*100, bleu[2]*100, bleu[3]*100, bleu[4]*100, addition[0], addition[1], addition[2], addition[3]))
