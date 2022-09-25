#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd

from collections import defaultdict
from functools import reduce
import json

# import pandas as pd
import numpy as np

import json
import pickle
# import pandas as pd
import math

import os
import json



########patient2disease_json
path_base="../../../../src/result"

path_disease_result=path_base+"/"+"diseaserank/result"
path_gene_result=path_base+"/"+"generank/result"
########################################################################################
path_gene_finally="../../../../src/utils/GeneRankResult/finally"


with open(path_disease_result + "/" + "Phen2Disease_patient_result.json") as fp:
    phen2disease_patient = json.load(fp)

with open(path_disease_result + "/" + "Phen2Disease_double_result.json") as fp:
    phen2disease_double = json.load(fp)

# with open(path_disease_result + "/" + "Phen2Disease_disease_result.json") as fp:
#     phen2disease_disease = json.load(fp)


phen2disease_integrated_sum = defaultdict(dict)

for patient in phen2disease_double:
    for gene in phen2disease_double[patient]:
        phen2disease_integrated_sum[patient][gene] = phen2disease_patient[patient][gene] + \
                                                            phen2disease_double[patient][gene]

######diseasescore2genescore_json

with open("../../../../data/association/Gene-Disease/disease2genecard2021.json") as fp:
        disease2card = json.load(fp)

with open("../../../../data/association/Gene-Disease/genecard2disease2021.json") as fp:
        card2disease = json.load(fp)

    ########################################################################################

similarity_matrix = phen2disease_integrated_sum

similarity_matrix_combine = defaultdict(dict)
similarity_matrix_new = defaultdict(dict)

for patient in similarity_matrix:
    for disease in similarity_matrix[patient]:
        if disease in disease2card.keys():
            for genecard in disease2card[disease]:
                similarity_matrix_new[patient][genecard] = 0

for patient in similarity_matrix_new:
    for genecard in similarity_matrix_new[patient]:
        score_list = []
        if genecard in card2disease.keys():
            for disease in card2disease[genecard]:
                if disease in similarity_matrix[patient]:
                    # print(similarity_matrix[disease_1][disease_2])
                    score_list.append(similarity_matrix[patient][disease])
        # print(score_list)
        if np.array(score_list).shape[0] == 0:
            genescore = 0
        else:
            genescore = np.array(score_list).max()
        similarity_matrix_new[patient][genecard] = similarity_matrix_new[patient][genecard] + genescore

for patient in similarity_matrix_new:
    for genecard in similarity_matrix_new[patient]:
        similarity_matrix_combine[patient][genecard] = similarity_matrix_new[patient][genecard]

with open(path_gene_finally + "/" + "Phen2Disease_integrated_result.json", 'w') as fp:
    json.dump(similarity_matrix_combine, fp, indent=2)




