# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

from pandas import DataFrame
import pandas as pd

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

class Config: pass
cf = Config()
cf.kmers = [15,21,27,31] 
cf.cvCuts  = [5,10,15]   
cf.expCov = map(lambda(x): x*2,cf.cvCuts)
cf.output = "data"
cf.seq = "EClen60cov20.fna"

def mkname(k,cvCut): return '_'.join([cf.output +'/',str(k),str(cvCut)])

# <codecell>

def init(conf):
    return DataFrame([(
                       kmer,
                       cvCut,
                       mkname(kmer,cvCut)
                       ) for kmer in conf.kmers for cvCut in conf.cvCuts],
                       columns=['kmer','cvCut','dirname'])

exp = init(cf)

# <codecell>

# clean
!rm -rf {cf.output}
!mkdir {cf.output}

# <codecell>

"""
Run the main rotuin to generate data files
this include runing velvet binaries (vleveth and vlevetg) 
for conf[k] x conf[cvCut] times.
"""
for k in exp.kmer: 
    !velveth temp {str(k)} -short {cf.seq};
    for cvCut in exp.cvCut:
        f = mkname(k,cvCut)
        !cp -R temp {f}
        !velvetg {f} -cov_cutoff {str(cvCut)};
    !rm -rf temp

# <codecell>

"""
Collect data from files into dataframe has the following columns
k cvCut n50 totalLgth contigs_ls_2 mean max min
"""

def collect(info):
    """
    recieve a file path, returns a row of the required information.
    """
    stats = pd.read_table('/'.join([info['dirname'],"stats.txt"]))
    lgth = (stats['lgth'].order(ascending=False) + (info['kmer']-1))
    return (info['kmer'],
            info['cvCut'],
            lgth.sum(),
            lgth.min(),
            lgth.max(),
            lgth.mean(),
            lgth.median(),
            lgth[lgth.cumsum() >= lgth.sum()/2].irow(0)) # n50

l = [collect(exp.ix[info]) for info in exp.index]
d = DataFrame(l,columns=['kmer','cvCut','sum','min','max','mean','median','n50'])
d

