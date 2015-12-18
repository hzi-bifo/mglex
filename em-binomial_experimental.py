#!/usr/bin/env python3
# -*- coding: utf-8 -*-

u"""
This is the main program which runs the EM algorithm for coverage clustering.
"""

__author__ = "johannes.droege@uni-duesseldorf.de"

from common import *
import composition
import binomial
from em import *
from sys import exit, stderr


if __name__ == "__main__":
    from sys import argv, stdin, stdout, stderr
    import signal

    signal.signal(signal.SIGPIPE, signal.SIG_DFL)  # handle broken pipes

    # parse command line options
    sharp = float(argv[5])
    seqnames = load_seqnames(open(argv[1], "r"))
    data_size = np.fromiter(load_data_sizes(open(argv[2], "r")), dtype=size_type)[:, np.newaxis]
    seeds = seeds2indices(seqnames, load_seeds(open(argv[3], "r")))
    c = len(seeds)

    # load data
    stderr.write("parsing coverage features\n")
    cov_data = binomial.Data(sizes=data_size)
    load_data_file(open(argv[4], "r"), cov_data)

    data = UniversalData([cov_data], sizes=data_size)

    # construct inital (hard) responsibilities
    responsibilities = responsibilities_from_seeds(seeds, data.num_data)

    # create a random model
    model = UniversalModel(100,
                           [binomial.empty_model(c, cov_data.num_features)])

    # EM clustering
    priors = flat_priors(model.num_components)  # uniform (flat) priors
    models, priors, responsibilities = em(model, priors, data, responsibilities, sharp)

    # output results if clustering
    stdout.write("#%s\n" % "\t".join(model.names))
    print_predictions(responsibilities)