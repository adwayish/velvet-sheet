# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import pandas as pd
from collections import namedtuple

# <markdowncell>

# #Velvet Experiment Sheet

# <codecell>

###
# set up experiment parameters
# kmers : kmer length
# cvCut : coverage threshold per contig 
#
# refer to vlevlet manual for more details. 
###

class Experiment: pass
ex = Experiment()
ex.kmers = [1,2,3,4] 
ex.cvCut  = [8,10]   
ex.expCov = map(lambda(x): x*2,ex.cvCut)
ex.output = "output"
ex.seq = "EClen60cov20.fna"

def mkname(k,cvCut): return '_'.join([ex.output,str(k),str(cvCut)]) 

# build the iteration list
Iteration = namedtuple('Iteration','kmer cvCut dirname')
ex.iterations =[Iteration(kmer,cvCut,mkname(kmer,cvCut)) for kmer in ex.kmers for cvCut in ex.cvCut]

# <codecell>

# clean
for f in ex.dirs:
    !rm -rf {f}

# <codecell>

"""
Run the main rotuin to generate data files
this include runing velvet binaries (vleveth and vlevetg) 
for conf[k] x conf[cvCut] times.
"""
for k in ex.kmers: 
    !velveth {ex.output} {str(k)} -short {ex.seq};
    for cvCut in ex.cvCut:
        f = mkname(k,cvCut)
        !cp -R {ex.output} {f}
        !velvetg {f} -cov_cutoff {str(cvCut)};
    !rm -rf {ex.output}

# <codecell>

"""
Collect data from files into dataframe has the following columns
k cvCut n50 totalLgth contigs_ls_2 mean max min
"""
def collect(f,kmer):
    """
    recieve a file path, returns a row of the required information.
    """
    stats = pd.read_table('/'.join([f,"stats.txt"]))
    stats['lgth'] = (stats['lgth'] + (kmer-1))
    sumLgth = stats['lgth'].sum()
    minLgth = stats['lgth'].min()
    maxLgth = stats['lgth'].max()
    meanLgth= stats['lgth'].mean()
    medianLgth=stats['lgth'].median()
    [sumLgth,minLgth,maxLgth,meanLgth,medianLgth] 

