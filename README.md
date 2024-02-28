# Neural-MBFL
This project is the experimental code for Neural-Mutation Based Fault Localization.
Neural-MBFL is a novel fault localization approach based on neural mutation. 

We utilize mutation techniques based on CodePTM at the token level, using μbert for mutant generation, replacing traditional mutation techniques in MBFL.
Below is an experimental framework diagram of our project:
![framework diagram](framework.png)

## Requirements
- `python 3.7.0`
- [*CodeBERT*](https://github.com/microsoft/CodeBERT) dependencies:
  - `pip install torch`
  - `pip install transformers`
- `defects4J environment`

## Directory Structure

### Mutation Geneartion:
Scripts for generating mutants and the code for μbert
- mbert
- mBert4d4j-automulti.py
- environment.yml

### Test Execution and Mutation Analysis:
Execution of mutants to gather execution information, etc.
- cleanProjectRunTest.py
- runMutantFaultyFile-automulti.py

### Fault Localization and Ranking Techniques: 
Analysis of mutant execution information for fault localization and scripts for calculating some evaluation metrics
- AchangeFileToJson.py
- BclacSusNew.py
- CclacRank.py
- DclacAllTypeRank.py
- DclacAllTypeRank2.py
- EclacCorrectTopn.py
- EclacSusMutant.py
- FclacAllTop-n.py
- GclacMAP.Py

### Result Analysis:
Scripts related to the analysis of RQs (Research Questions) in the paper
- RQ1MutantNum
- RQ1ToPN
- RQ2Venn
- RQ3RepairPatterns
