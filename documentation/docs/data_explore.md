# Data explore on College Distance dataset

## Introduction

---------

Given the [dataset](https://vincentarelbundock.github.io/Rdatasets/csv/AER/CollegeDistance.csv) with cross-section data
from the High School and Beyond survey conducted by the Department of Education (USA) in 1980, with a follow-up in 1986.
The survey included students from approximately 1,100 high schools.

The goal is to create an ML model that will predict the `base year composite tets score` or just the `score` feature in
the dataset.

## Details

---------

[All given information comes from this page](https://vincentarelbundock.github.io/Rdatasets/doc/AER/CollegeDistance.html)

Rouse (1995) computed years of education by assigning 12 years to all members of the senior class. Each additional year
of secondary education counted as a one year. Students with vocational degrees were assigned 13 years, AA degrees were
assigned 14 years, BA degrees were assigned 16 years, those with some graduate education were assigned 17 years, and
those with a graduate degree were assigned 18 years.

Stock and Watson (2007) provide separate data files for the students from Western states and the remaining students.
CollegeDistance includes both data sets, subsets are easily obtained (see also examples).

### Source

Online complements to Stock and Watson (2007).

### References

Rouse, C.E. (1995). Democratization or Diversion? The Effect of Community Colleges on Educational Attainment. Journal of
Business & Economic Statistics, 12, 217–224.

Stock, J.H. and Watson, M.W. (2007). Introduction to Econometrics, 2nd ed. Boston: Addison Wesley.

### Data format

A data frame containing 4739 observations based on 14 variables (15 including `rownames` feature).

Features explained:

+ `gender`: factor indicating gender.
    * Possible values: `female` or `male`.
+ `ethnicity`: factor indicating ethnicity.
    * Possible values: `afam` (African-American), `hispanic` or `other`.
+ `score`: base year composite test score. These are achievement tests given to high school seniors in the sample.
    * Possible values: non-negative floating point number.
+ `fcollege`: factor. Is the father a college graduate?
    * Possible values: `yes` or `no`.
+ `mcollege`: factor. Is the mother a college graduate?
    * Possible values: `yes` or `no`.
+ `home`: factor. Does the family own their home?
    * Possible values: `yes` or `no`.
+ `urban`: factor. Is the school in an urban area?
    * Possible values: `yes` or `no`.
+ `unemp`: county unemployment rate in 1980.
    * Possible values: non-negative floating point number.
+ `wage`: state hourly wage in manufacturing in 1980.
    * Possible values: non-negative floating point number.
+ `distance`: distance from 4-year college (in 10 miles).
    * Possible values: non-negative floating point number.
+ `tuition`: average state 4-year college tuition (in 1000 USD).
    * Possible values: non-negative floating point number.
+ `education`: number of years of education.
    * Possible values: non-negative integer.
+ `income`: factor. Is the family income above USD 25,000 per year?
    * Possible values: `low` or `high`.
+ `region`: factor indicating region.
    * Possible values: `west` or `other`.


