import numpy as np
import pandas as pd
from pathlib import Path
import math
from scipy import stats

####### HELPER CLASSES ########
# gamma prior on lambda
class LambdaPrior:
    def __init__(self, alpha, beta):
        self.fn = stats.gamma(alpha, loc = 0, scale = 1)
        self.alpha = alpha
        self.beta = beta
        self.proposeDistr = stats.norm # initialize

    # Generate candidate lambda using proposal distribution around last good lambda
    def sample(self, lastLambda, proposeStdDev):
        return lastLambda + self.proposeDistr.rvs(loc=0, scale=proposeStdDev)

    def logpdf(self, x):
        return self.fn.logpdf(x)

    def mean(self):
        return self.fn.mean()

# Exponential to model cumulative rainfall
class ExpModel:
    def __init__(self, data):
        self.fn = stats.expon
        self.data = data

    def likelihood(self, candidateLambda):
        return self.fn.logpdf(self.data, scale=1.0 / candidateLambda).sum()

# Data structure that holds the posterior distribution
class Posterior:
    def __init__(self, nIts):
        self.postr = pd.DataFrame({'posterior': np.zeros(nIts),
                                   'lambda': np.zeros(nIts),
                                   'prior': np.zeros(nIts),
                                   'likelihood': np.zeros(nIts)})

        self.nAccepts = 0

    # Append candidate lambda to posterior if posterior probability is high enough
    def append(self, i, candidateLambda, prior, likelihood):
        posterior = prior + likelihood

        if i == 0:
            self.postr.iloc[i] = {'posterior': posterior,
                                  'lambda': candidateLambda,
                                  'prior': prior,
                                  'likelihood': likelihood}
        else:
            ratio = posterior - self.postr.iloc[i - 1]['posterior']
            r = math.log(np.random.rand())
            if r < ratio:
                self.postr.iloc[i] = {'posterior': posterior,
                                      'lambda': candidateLambda,
                                      'prior': prior,
                                      'likelihood': likelihood}
                self.nAccepts += 1
            else:
                self.postr.iloc[i] = self.postr.iloc[i - 1]

    def getLambda(self, i):
        return self.postr.iloc[i]['lambda']

# Make proposal distribution narrower or wider depending on acceptance rate
class AdaptableProposalStdDev:
    def __init__(self, initialStdDev, batchSize):
        self.stdDev = initialStdDev
        self.batchSize = batchSize
        self.acceptRate = []
        self.targetAcceptRate = 0.44 # in 1 dimension

    def adapt(self, nAccepts, i):
        self.acceptRate.append(nAccepts/self.batchSize)
        deltaSign = 1 if (self.acceptRate[-1]) > self.targetAcceptRate else -1
        delta = math.exp(deltaSign * math.pow(i, -0.5))
        #print(f'Proposal Std: before: {proposeStdDev}, after: {proposeStdDev*delta}')
        self.stdDev *= delta

def getAndCleanPrecip():
    r = np.random.randn()

    # data came from https://www.ncdc.noaa.gov/cdo-web/datatools/lcd
    # https://www1.ncdc.noaa.gov/pub/data/cdo/documentation/GHCND_documentation.pdf
    df = pd.read_csv('/Users/marisa/git/practice/data/Middlesex_Daily_10yr.csv')
    keysIwant = [s for s in df.keys() if 'Precip' in s]
    col = 'DailyPrecipitation'
    df[(df[col]=="T") | (df[col]=="Ts")] = "0.0"

    mySeries = df[pd.notna(df[col])][col]
    df2 = mySeries.str.extract(r'([0-9.]*)([a-zA-Z]*)', expand=True)
    df2 = df2.rename(index=str, columns={0: "precipNum", 1: "precipFlag"})
    df2['precipNum'] = df2['precipNum'].astype('float64')
    return df2

def baseProjectDir():
    return Path(__file__).resolve()

if __name__== "__main__":
    getAndCleanPrecip()
