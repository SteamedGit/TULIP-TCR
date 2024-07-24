# TULIP-TCR Fork

## This repo is a fork of TULIP-TCR with requirements and various helper scripts. See the [original repo](https://github.com/barthelemymp/TULIP-TCR) for more info

## Installation
The version of python and packages are not documented in the original repo. I've supplied a requirements file that worked for Python 3.10.14.


## Usage Guide

### Data
Your training data needs these columns
```
MHC,allele_processed,peptide,CDR3a,CDR3b
```
And any eval sets also need a ```binder``` column
Missing values are indicated with a ```<MIS>```
### Training
To train a model from scratch use
```
python full_learning_new.py --train_dir <path to train csv> --test_dir <path to an eval csv> --modelconfig <path to a decoupled config> --save <checkpoint save directory> --batch_size b 
```


### Predictions
The prediction script computes scores and ranks for each peptide in your eval set individually and writes them into seperate csvs in a specified folder.

```
python predict.py --test_dir <path to csv> --load <path to .bin or .safetensors> --modelconfig <path to model config> --output <folder to write peptide score csvs to> --batch_size b
```

The ```--mhc_tokenizer``` arg is to accomodate models trained with --noMHC, these need the ```nomhctok``` tokenizer

Note that there is incompatibility between the configs that TULIP-TCR uses for training vs predictions. For example, the default config for training appears to be ```configs/shallow0_decoupled.config.json```, but this config cannot be used with the supplied predictions script. Rather you have to use ```configs/shallow.config.json```. The same goes for the medium configs.

Example usage:
```
python predict.py --test_dir data/VDJ_test_2.csv --load model_weights/pytorch_model.bin --modelconfig configs/shallow.config.json --output data_output/pretrained --batch_size 512 
```

### Evaluation
To calculate global auc roc you can use 

```calculate_global_auc.py --predictions_dir <path to score csvs> --targets_dir <path to eval data>```


## From the original readme

## data
the data folder contains the data to reproduce results of the paper.
Seenpeptides.zip: contains the data to reproduce the experiments on seen peptide. (model for this part is directly the one in model_weights)
Unseenpeptides.zip: contains the data to reproduce the experiments on unseen peptide.
RepertoireMining.zip: contains the data to reproduce the repertoire mining of neoantigen.
The largest training will be in the Seenpeptides.zip
The data should be a csv as in `data/VDJ_test_2.csv`  and have the column CDR3a, CDR3b, MHC, peptide, and binder. binder will only be used to compute aucs, so you can put only ones if you just want to train or predict.



## scripts
We give 3 scripts 
 - full_learning_new.py / run_full_leaning.sh implement the training from scratch of the model
 - finetuning.py / run_finetuning.py finetune the model on a subset
 - predict.py rank TCRs for a given epitope. You can run it with: `python predict.py --test_dir data/VDJ_test_2.csv --output data/`


## Colab:
tulip.ipynb enables playing with TULIP from colab

## HLA remark:
For rare HLA, TULIP works better with `--nomhc` option. 
TO DO: predict HLA indepndantly and remove it from epitope prediction.


## Code options:
`--skipMiss`: enables the mopdel to directly learn the encoded representation of a missing sequence. Without it, the model learn the embedding of `<MIS>` and pass it to the encoder. This option is largely recommended, as it avoid having the missing sequences taking a too large importance in the training the encoders.

`--train_dir` and `--test_dir`: path to the train and test csv files.

`--modelconfig`:path to json including the config of the model.

`--save` and `--load`: path to the save the model and path to the saved model if we want to start from a pretrained model.

`--lr`L learning rate

`--weight_decay`: weight decay for the adam optimized

`--nomhc`: enables to skip the mhc. As a general rule, the mhc tokenizer is beneficial for peptides presented on HLA, for which TULIP has seen a variety of peptide.

`--num_epochs`: number of epochs

`--masking_proba`: it is a new form of regularization (not used in the paper). default is 0.0. If not null, this is the proba to randomly mask the alpha or the beta chain during training. This is made to mitigate some experimental biases on bulk vs single cell. (for example, if for a peptide we only have TCR missing their alpha chain, we would like to avoid TULIP to learn a signal between missing alpha chain and this peptide). This regularization was proven usefull when using TULIP has a geneartive model. 





