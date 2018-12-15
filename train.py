import argparse
import os
import json

from GameEnvironment import train
from config_sanity import check_train_config

parser = argparse.ArgumentParser(description='Algorithm trainer')
parser.add_argument("networks", type=str, help="Network name suffix")
parser.add_argument("config", type=str, help="Configuration file for training")
parser.add_argument('-t', '--threads', type=int, default=10, help="Number of threads")
parser.add_argument('-c', '--cpu', action='store_true', help="Use CPU for computations")
parser.add_argument('-e', '--preload_eviction', action='store_true', help="Load pretrained eviction")
parser.add_argument('-a', '--preload_admission', action='store_true', help="Load pretrained admission")
parser.add_argument('-v', '--verbose', action='store_true', help="Verbose sanity check")
parser.add_argument('-s', '--show', action='store_true', help="Show testing results")

args = parser.parse_args()

configuration = check_train_config(args.config, verbose=False)
if configuration is None:
    exit(0)

if args.cpu:
    print '=============Ignoring GPU============='
    os.environ["CUDA_VISIBLE_DEVICES"]="-1"
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

train(configuration, 'models/adm_' + args.networks, 'models/evc_' + args.networks,
      args.preload_admission, args.preload_eviction,
      n_threads=args.threads, verbose=args.verbose, show=not args.show)

