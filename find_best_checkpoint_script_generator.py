import argparse
import os





def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--test_dir",
        default=None,
        type=str,
        required=True,
        help="The test data dir.",
    )
    parser.add_argument(
        "--modelconfig",
        default="configs/shallow.config.json",
        type=str,
        help="path to json including the config of the model" ,
    )
    parser.add_argument(
        "--checkpoints_dir",
        default=None,
        type=str,
        required=True,
        help="path to the model pretrained to load" ,
    )
    parser.add_argument(
        "--output",
        default=None,
        type=str,
        help="path to save results" ,
    )
    parser.add_argument(
        "--batch_size",
        default=512,
        type=int,
        help="batch_size" ,
    )
    parser.add_argument(
        "--mhc_tokenizer",
        default="mhctok/",
        type=str,
        help="Tokenizer for the mhcs. If trained with noMHC must use nomhctok."
    )
    args = parser.parse_args()
    checkpoints = filter(lambda x: 'txt' not in x and 'sh' not in x,os.listdir(args.checkpoints_dir))
    bash_script = "#!/bin/bash\n"
    for checkpoint in list(sorted(checkpoints,key=lambda x: int(x))):
        pred_cmd  = (f"python predict.py --test_dir {args.test_dir} "
        f"--load {args.checkpoints_dir}{checkpoint}/model.safetensors "
        f"--modelconfig {args.modelconfig} --output {args.output} --batch_size {args.batch_size} "
        f"--mhc_tokenizer {args.mhc_tokenizer}")

        glob_auc_cmd = (f"python calculate_global_auc.py -p {args.output} -t {args.test_dir} >> {args.checkpoints_dir}/{args.test_dir.split('_5to1_')[-1].split('.csv')[0]}_results.txt")

        cleanup_cmd = f"rm  {args.output}*"
        bash_script+=pred_cmd+'\n'+glob_auc_cmd+'\n'+cleanup_cmd+'\n\n'
    with open(f"{args.checkpoints_dir}/{args.test_dir.split('_5to1_')[-1].split('.csv')[0]}_checkpoint_eval.sh","w") as f:
        f.write(bash_script)
    
if __name__=="__main__":
    main()