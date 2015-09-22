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
    weight = float(argv[4])
    seqnames = [line.rstrip() for line in open(argv[1], "r")]

    seeds = seeds2indices(seqnames, load_seeds(open(argv[2], "r")))
    c = len(seeds)

    # load data
    stderr.write("parsing coverage features\n")
    cov_data = binomial.Data(["0-0", "1-0", "2-0", "3-0"])
    load_data_file(open(argv[3], "r"), cov_data)

    data = UniversalData([cov_data])

    # construct inital (hard) responsibilities
    responsibilities = responsibilities_from_seeds(seeds, data.num_data)

    # create a random model
    model = UniversalModel([weight], [binomial.empty_model(c, 4)])

    # EM clustering
    priors = flat_priors(model.components)  # uniform (flat) priors
    models, priors, responsibilities = em(model, priors, data, responsibilities)

    # output results if clustering
    stdout.write("#%s\n" % "\t".join(model.names))
    print_predictions(responsibilities)