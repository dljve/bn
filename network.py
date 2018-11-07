# -*- coding: utf-8 -*-
import pandas as pd
import pgmpy as pgm
import numpy as np
from scipy import stats

"""
Load in data
"""
mat = pd.read_csv("student-mat.csv", delimiter=';')
por = pd.read_csv("student-por.csv", delimiter=';')

mat['subject'] = pd.Series(np.full((mat.shape[0],), fill_value='mat', dtype=object), index=mat.index)
por['subject'] = pd.Series(np.full((por.shape[0],), fill_value='por', dtype=object), index=por.index)

df = pd.concat([mat, por])

df.head()

"""
PgmPy
"""

def test_independence(df, var1, var2, condition_vars=None):
    """
    Test for the independence condition (var1 _|_ var2 | condition_vars) in df.

    Parameters
    ----------
    df: pandas Dataframe
        The dataset on which to test the independence condition.

    var1: str
        First variable in the independence condition.

    var2: str
        Second variable in the independence condition

    condition_vars: list
        List of variable names in given variables.

    Returns
    -------
    chi_stat: float
        The chi-square statistic for the test.

    p_value: float
        The p-value of the test

    dof: int
        Degrees of Freedom

    Examples
    --------
    >>> df = pd.read_csv('adult.csv')
    >>> chi, p, dof = test_independence(df, var1='Age', var2='Immigrant')
    >>> print("chi =", chi, "\np =", p, "\ndof =",dof)
    chi = 57.7514122288
    p = 8.60514815766e-12
    dof = 4
    >>> chi, p, dof = test_independence(df, var1='Education', var2='HoursPerWeek',
    ...                                 condition_vars=['Age', 'Immigrant', 'Sex'])
    >>> print("chi=", chi, "\np=", p, "\ndof=",dof)
    chi = 1360.65856663 
    p = 0.0 
    dof = 171
    """
    N = df.shape[0]
    
    if not condition_vars:
        observed = pd.crosstab(df[var1], df[var2])
        chi_stat, p_value, dof, expected = stats.chi2_contingency(observed)
        if chi_stat < dof:
            RMSEA = 0
        else:
            RMSEA = np.sqrt((chi_stat/dof-1)/(N-1))
    else:
        observed_combinations = df.groupby(condition_vars).size().reset_index()
        chi_stat = 0
        dof = 0
        for combination in range(len(observed_combinations)):
            df_conditioned = df.copy()
            for condition_var in condition_vars:
                df_conditioned = df_conditioned.loc[df_conditioned.loc[:, condition_var] == observed_combinations.loc[combination, condition_var]]
            observed = pd.crosstab(df_conditioned[var1], df_conditioned[var2])
            chi, _, freedom, _ = stats.chi2_contingency(observed)
            chi_stat += chi
            dof += freedom        
        
        if chi_stat < dof:
            RMSEA = 0
        else:
            RMSEA = np.sqrt((chi_stat/dof-1)/(N-1))
            
        p_value = 1.0 - stats.chi2.cdf(x=chi_stat, df=dof)

    return chi_stat, p_value, dof, RMSEA

### For defining the network in python, the package pgmpy can be used but it will work only for directed graphs.
from pgmpy.models import BayesianModel

bnmodel = [
    ('absences', 'G3'),
    ('activities', 'freetime'),
    ('age', 'activities'),
    ('age', 'romantic'),
    ('age', 'studytime'),
    ('failures', 'G3'),
    ('failures', 'paid'),
    ('failures', 'schoolsup'),
    ('failures', 'studytime'),
    ('famrel', 'famsup'),
    ('famrel', 'paid'),
    ('famsup', 'G3'),
    ('famsup', 'paid'),
    ('famsup', 'studytime'),
    ('Fedu', 'Fjob'),
    ('Fedu', 'higher'),
    ('Fjob', 'famrel'),
    ('freetime', 'G3'),
    ('goout', 'freetime'),
    ('freetime', 'studytime'),
    ('goout', 'romantic'),
    ('health', 'absences'),
    ('health', 'G3'),
    ('health', 'studytime'),
    ('higher', 'famsup'),
    ('higher', 'school'),
    ('higher', 'studytime'),
    ('IQ', 'G3'),
    ('IQ', 'higher'),
    ('IQ', 'studytime'),
    ('Medu', 'higher'),
    ('Medu', 'Mjob'),
    ('Mjob', 'famrel'),
    ('paid', 'freetime'),
    ('paid', 'G3'),
    ('paid', 'studytime'),
    ('romantic', 'freetime'),
    ('school', 'schoolsup'),
    ('school', 'traveltime'),
    ('schoolsup', 'freetime'),
    ('schoolsup', 'G3'),
    ('schoolsup', 'studytime'),
    ('studytime', 'G3'),
    ('subject', 'absences'),
    ('subject', 'failures'),
    ('subject', 'famsup'),
    ('subject', 'G3'),
    ('subject', 'paid'),
    ('subject', 'schoolsup'),
    ('subject', 'studytime'),
    ('traveltime', 'absences'),
    ('traveltime', 'freetime'),
    ('absences', 'failures'),
    # cycles
    # ('studytime', 'activities'),
    # ('activities', 'studytime'),
    # ('freetime', 'goout'),
    # ('failures', 'absences'),
    # ('freetime', 'activities'),
    # ('studytime', 'freetime'),
]

model = BayesianModel(bnmodel)

# To test any implied condition in the network, the method `is_active_trail` can be used. Next line tests for 
# the condition (Education _|_ MaritalStatus | Age)

var1 = 'subject'
var2 = 'G3'
observed = []
active = model.is_active_trail(var1, var2, observed=observed) # is dependent

# The `get_independencies` method lists all the implied conditions in the model.
#model.get_independencies()


# To perform chi-square test on any of the conditional independencies, the method `test_independence` defined
# above can be used. To test for (Education _|_ HoursPerWeek | 'Age', 'Immigrant', 'Sex')


independent, dependent, questionable = [], [], []

for (var1,var2) in bnmodel:
    if var1 == 'IQ' or var2 == 'IQ':
        continue
    chi_stat, p_value, dof, RMSEA = test_independence(df=df, var1=var1, var2=var2, condition_vars=observed)
    
    if RMSEA < 0.05:
        independent.append((var1, var2, chi_stat, p_value, dof, RMSEA))
    elif RMSEA < 0.09:
        questionable.append((var1, var2, chi_stat, p_value, dof, RMSEA))
    else:
        dependent.append((var1, var2, chi_stat, p_value, dof, RMSEA))
        
    
print("Independent")
for (var1, var2, chi_stat, p_value, dof, RMSEA) in independent:
    print("{} _|_ {}\t{}\t{}\t{}\t{}".format(var1, var2, chi_stat, p_value, dof, RMSEA))

print("Questionable")
for (var1, var2, chi_stat, p_value, dof, RMSEA) in questionable:
    print("{} _|_ {}\t{}\t{}\t{}\t{}".format(var1, var2, chi_stat, p_value, dof, RMSEA))

print("Dependent")
for (var1, var2, chi_stat, p_value, dof, RMSEA) in dependent:
    print("{} _|_ {}\t{}\t{}\t{}\t{}".format(var1, var2, chi_stat, p_value, dof, RMSEA))
        

"""
Test all independences
"""

"""
import re

with open("relations.txt") as f:
    for line in f.readlines():
        r = r'^(.*?) ⊥ (.*?)\s?(\|.*)?$'
        var1, var2, obs = re.findall(r,line)[0]
        if obs:
            obs = obs.split('| ')[1].split(', ')
            continue
        else:
            obs = []
        if var1 == 'IQ' or var2 == 'IQ' or 'IQ' in obs:
            continue
            
        active = model.is_active_trail(var1, var2, observed=obs) # is dependent
        chi_stat, p_value, dof = test_independence(df=df, var1=var1, var2=var2, condition_vars=obs)
        
        if p_value <= 0.05 and not active:
            print("Correct (independent)", line, chi_stat, p_value, dof)
        elif p_value > 0.05 and not active:
            print("Error (not indepedent)", line, chi_stat, p_value, dof)
"""

