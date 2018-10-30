"""Module hosting classes that return fake data

[description]
"""
import pandas as pd
import numpy as np
import datetime as dt
from abc import ABC, abstractmethod, abstractproperty
from .faker import ConceptKeys  # named tuple of ids and names


class TwoD(ABC):
    # simulate 2d data

    def __init__(self, ts, colname=None):

        self.ts = ts # 2d timeseries
        self.colname = colname
        self.colname = self._gen_colname() # to label data

    @abstractproperty
    def conceptkeys(self):
        """Should return a ConceptKeys tuple for every class

        concept_id should be mandated but shortname and FSN should be optional

        Decorators:
            abstractproperty
        """
        pass

    def _gen_colname(self):
        """Generate a suitable column name for the time series
        """
        if self.colname is not None:
            return self.colname
        elif self.conceptkeys.shortName is not None:
            return self.conceptkeys.shortName
        else:
            return str(self.conceptkeys.concept_id)


class Lactate(TwoD):

    @property
    def conceptkeys(self):
        return ConceptKeys(3047181, 'lactate', 'Lactate [Moles/volume] in Blood')

    # - [ ] @TODO: (2018-10-30) use mixins for these simulations
    def simulate(self, cadence=None):
        ts = self.ts
        vals = [np.random.lognormal() for i in ts]
        return pd.DataFrame.from_dict({'timestamp': ts, self.colname: vals})


class HeartRate(TwoD):

    @property
    def conceptkeys(self):
        return ConceptKeys(4239408, 'hrate', 'Heart rate (observable entity)')

    def simulate(self, cadence=None):
        ts = self.ts
        vals = [np.random.normal(90, 15) for i in ts]
        return pd.DataFrame.from_dict({'timestamp': ts, self.colname: vals})



# - [ ] @TODO: (2018-10-30) convert to a test
# ts = pd.date_range('2018-10-29', '2018-10-30', freq='4H')
# hr.conceptkeys.shortName
# hr = HeartRate(ts)
# hr.simulate()
# lac = Lactate(ts)
# lac.simulate()
