#!/usr/bin/env python3

u"""
Takes a label matrix one-zero entries and probability class assignments and calculates an evaluation statistic.
S_group = log(\sum_i=1_C \product_{d \element C_i} p(d|C_i))
"The log-probability that all data of the same group (known to belong together) appear in the same cluster.
"""

__author__ = "johannes.droege@uni-duesseldorf.de"

import sys
import numpy as np
from common import print_probmatrix, print_probvector


if __name__ == "__main__":
    try:
        filein2 = open(sys.argv[2], "r")
    except IndexError:
        filein2 = sys.stdin

    joint_clustering_probs = None
    group_size = None

    for line1, line2 in zip(open(sys.argv[1], "r"), filein2):

        empty = (not line1, not line2)

        if all(empty):
            continue

        if any(empty):
            sys.stderr.write("Cannot have empty line in one out of two inputs.\n")
            sys.exit(1)

        comment = (line1[0] == "#", line2[0] == "#")

        if all(comment):
            continue

        if any(comment):
            sys.stderr.write("Cannot have comment line in one out of two inputs.\n")
            sys.exit(2)

        fields = line1.rstrip().split("\t")
        labelvec = np.asarray(np.exp(-np.asarray(fields, dtype=float)), dtype=bool)  # bool row vector
        assert(labelvec.sum() == 1.)

        fields = line2.rstrip().split("\t")
        predictionvec = -np.asarray(fields, dtype=float)  # logprob row vector

        try:
            group_size[labelvec] += 1
            joint_clustering_probs[labelvec] += predictionvec
        except TypeError:
            group_size = np.zeros(len(labelvec))
            joint_clustering_probs = np.zeros((len(labelvec), len(predictionvec)))
            joint_clustering_probs[labelvec] += predictionvec

    # normalize sizes
    group_size_normalized = (group_size/group_size.sum())[np.newaxis, :]
    # print_probmatrix(group_size_normalized)
    prob_together_pergroup = np.exp(joint_clustering_probs).sum(axis=1, keepdims=True)
    # print_probmatrix(prob_together_pergroup)
    expected_prob_overall = np.dot(group_size_normalized, prob_together_pergroup)
    sys.stdout.write("%.2f\n" % np.log(expected_prob_overall))
