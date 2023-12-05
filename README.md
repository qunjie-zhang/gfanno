# Gfanno
Gene Family Annoation Pipline
```
   ______  ________    _     Gene Family Annotation Workflow                           
 .' ___  ||_   __  |  / \     Bioinformatics Lab of SCAU.            
/ .'   \_|  | |_ \_| / _ \     _ .--.   _ .--.   .--.   
| |   ____  |  _|   / ___ \   [ `.-. | [ `.-. |/ .'`\ \ 
\ `.___]  |_| |_  _/ /   \ \_  | | | |  | | | || \__. | 
 `._____.'|_____||____| |____|[___||__][___||__]'.__.'  
```
## Introduction
This software is used to identify candidate genes.
Here, we demonstrate the identification of the SCPLⅠA gene in Tieguanyin as an example, 
based on parameter thresholds for gene filtering.


## Install
### Preparation before use
Please ensure that you have installed BLAST and Hmmer software correctly before use.
You can execute the following two commands to test the software installation situation.

```shell
# Test blastp
blastp -version
# Test Hmmsearch
hmmsearch -h
```
### Environment
python >= 3.5

### Install Gfanno
There are several ways to run gfanno
- Installing using pypi
```shell
pip install gfanno
```
- Installing using source code
```shell
git clone https://github.com/qunjie-zhang/gfanno.git
cd gfanno
python setup.py install
```

## Quick Start
```shell
# Generate basic configuration file.
gfanno -g
# Release sample data, including HMM models and seed files.
gfanno --data

# Enter the fasta file path you need to use after the - f parameter
# This example uses a seed file. In actual use, the seed file is not passed in here.
gfanno -f seed/4CL.seed.fasta

```

## Usage
### Get Help Information
Use it as a terminal command. For all parameters, type `gfanno -h`.
```shell
Program:    gfanno (Gene Family Annoation Workflow)
Version:    1.00

    Useage: gfanno  <command> [options]

    Commands:
        -f / --fasta    Input fasta file path. This option is required.
        -o / --output   Output file path.
        -c / --config   Use the specified configuration file. This parameter is optional.
                        If you do not set this parameter, the program will use 'gfanno_config.ini' by default.
        -t / --target   Specifies the parameter category used in the configuration file. This option is required.
        -g / --generate Generate the default configuration file (gfanno_config.ini) under the current path.
                        Used to initialize the software operating environment or reset damaged configuration files
        -- / --data     Release built-in data sets in the current directory.
        -h / --help     Display this help message.
        -v / --version  Detailed version information
``` 
* `-f` is the input fasta file path,is a required parameter. 
* `-o` is the data output path. If the path does not exist, the program will automatically create it. The default is `output`
* `-c` This parameter is used to specify the path of the configuration file. By default, the configuration file is located in the current directory and is named `gfanno_config.ini`. In this case, you do not need to specify this parameter, as the program will use this file by default. If your configuration file has a different name or path, or if you want to use a specific configuration file, please use this parameter to inform the program about the configuration file you want to use.
* `-t` This is an optional parameter used to specify the parameter schemes used during software runtime. In the configuration file, you can define multiple runtime schemes. You can use this parameter to specify the names of the runtime schemes, allowing you to input multiple names separated by commas. If this parameter is not specified, all the schemes provided in the configuration file will be used by default.
* `-g` This parameter is used to generate the default configuration file in the current directory. The default name of this file is `gfanno_config.ini`. You can use this parameter to create a new configuration file for modification when the configuration file template is missing or when the file is corrupt.
* `--data` This is used to extract the built-in default dataset in the current path. It includes seed files and HMM models.


### Configuration file
Before starting, you need to prepare a configuration file to obtain relevant parameters when the software is running.
You can directly use the `gfanno -g` command to create the default configuration content configuration file `gfanno_config.ini` in the current path.
When special attention is required, you may create multiple sets of configuration files. Be careful to avoid accidental overwriting of files and loss of content.

You can create multiple configuration files to use with the software by using the -c parameter, or you can maintain a set of configuration files for use with the -t parameter to specify which ones will be run. It's important to note that the software has a configuration file validation feature. When the software is run, it will first check whether the configuration files being used are all valid. Data that doesn't meet the requirements will be flagged and the program will terminate

This is a demonstration scenario from the default configuration file:
```ini
# PPO
[PPO]
blastp_seed = seed/PPO.seed.fasta
hmm = hmm/PPO1_DWL.hmm,hmm/PPO1_KFDV.hmm
hmm_coverage = 70,70
domain = PPO1_KFDV,PPO1_DWL
blastp_identity = 50
blastp_qcovs = 50
```
In the configuration file, the hmm parameter, hmm_coverage parameter, and domain parameter can have multiple values separated by commas. However, it is important to note that the number of values they carry must be equal.

The configuration file supports comment text information starting with ‘;’ or ‘#’

## LICENSE
Copyright [2023] [Bioinformatics Laboratory of South China Agricultural University]

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

## Contact
If any questions, please create an issue on this repo, we will deal with it as soon as possible.
