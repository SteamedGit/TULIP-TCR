import pandas as pd
import argparse
import os
from sklearn.metrics import roc_auc_score
import numpy as np
import datetime


def main():
    parser = argparse.ArgumentParser()


    parser.add_argument(
        "--predictions_dir",
        "-p",
        default=None,
        type=str,
        required=True,
        help="The predictions dir.",
    )

    parser.add_argument(
        "--targets_file",
        "-t",
        default=None,
        type=str,
        required=True,
        help="The targets file.",
    )

    args=parser.parse_args()



    peptide_files = os.listdir(f"{args.predictions_dir}")
    RESULTS={}

    targets_df = pd.read_csv(args.targets_file)

    scores = []
    labels =[]
    for peptide_file in peptide_files:
        df = pd.read_csv(f"{args.predictions_dir}/{peptide_file}",index_col=False)
        df.drop(columns=["Unnamed: 0"],inplace=True)
        pep_targets = targets_df[targets_df['peptide']==peptide_file.split('.')[0]]
        for cdr3a,cdr3b,binder in zip(pep_targets['CDR3a'],pep_targets['CDR3b'],pep_targets['binder']):
            score = list(df[((df['CDR3a']==cdr3a)&(df['CDR3b']==cdr3b))]['score'])[0]
            scores.append(score)
            labels.append(binder)

    global_auc = roc_auc_score(labels, scores)
    print(global_auc)


if __name__=="__main__":
    main()