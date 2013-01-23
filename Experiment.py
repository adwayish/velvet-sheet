# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import pandas as pd

# <markdowncell>

# #Velvet Experiment Sheet

# <codecell>

"""
set up experiment parameters
k : kmer length
cvCut : kmer coverage

return to vlevlet manual for more about them. 
"""

conf = {}
conf['k'] = [15,21,31]
conf['cvCut'] = [8,10]
conf['expCov']= map(lambda(x): x*2,conf['cvCut'])
conf['output']= "output"
conf['seq'] = "EClen60cov20.fna"

#### Utils
def mkname(k,cvCut): return '_'.join([conf['output'],str(k),str(cvCut)])
conf['ls']= [mkname(k,cv) for k in conf['k'] for cv in conf['cvCut']]

# <codecell>

# clean
for f in conf['ls']:
    !rm -rf {f}

# <codecell>

"""
Run the main rotuin to generate data files
this include runing velvet binaries (vleveth and vlevetg) 
for conf[k] x conf[cvCut] times.
"""
for k in conf['k']: 
    !echo {conf['output']} {str(k)} -short {conf['seq']}
    !velveth {conf['output']} {str(k)} -short {conf['seq']};
    for cvCut in conf['cvCut']:
        f = mkname(k,cvCut)
        !cp -R {conf['output']} {f}
        !velvetg {f} -cov_cutoff {str(cvCut)};
    !rm -rf {conf['output']}

# <codecell>

"""
Collect Data files into dataframe with the following columns
k cvCut n50 totalLgth contigs_ls_2 mean max min
"""
def collect(f):
    """
    recieve a file path, returns a row of the required information.
    """
    stats = pd.read_table('/'.join([f,"stats.txt"]))
    sumLgth = (stats['lgth'] + (conf['k']-1)).sum()
    minLgth = (stats['lgth'] + (conf['k']-1)).min()
    maxLgth = (stats['lgth'] + (conf['k']-1)).max()
    meanLgth= (stats['lgth'] + (conf['k']-1)).mean()
    medianLgth=(stats['lgth'] + (conf['k']-1)).median()
    [sumLgth,minLgth,maxLgth,meanLgth,medianLgth]
    
    

