# nanoAOD-tools-AXOL1TL
Tools for working with L1NanoAOD for AXOL1TL trigger

## Checkout instructions: standalone

You need to setup python 2.7 and a recent ROOT version first.

    git clone https://github.com/cms-nanoAOD/nanoAOD-tools.git NanoAODTools
    cd NanoAODTools
    bash standalone/env_standalone.sh build
    source standalone/env_standalone.sh

Repeat only the last command at the beginning of every session.

Please never commit neither the build directory, nor the empty init.py files created by the script.

## Checkout instructions: CMSSW

    cd $CMSSW_BASE/src
    git clone https://github.com/cms-nanoAOD/nanoAOD-tools.git PhysicsTools/NanoAODTools
    cd PhysicsTools/NanoAODTools
    cmsenv
    scram b

## Other dependencies: AXOL1TL Emulator

See here for instructions to use standalone anomaly detection emulation: https://gitlab.cern.ch/ssummers/run3_ugt_ml

All that is necessary is the ability to import the Python module

    import ugt_hls_emulator as ugt


## Processing individual files

To generate a friend tree file (tree that only include anomaly score branch), run the following command

    python scripts/nano_postproc.py <output directory> <input l1nano file> -I PhysicsTools.NanoAODTools.postprocessing.modules.l1ad_inference axol1tlModuleConstr -s <file postfix> -b scripts/keep_and_drop_input.txt --friend

To generate a full L1NanoAOD file with a new anomaly score branch, run the following

    python scripts/nano_postproc.py <output directory> <input l1nano file> -I PhysicsTools.NanoAODTools.postprocessing.modules.l1ad_inference axol1tlModuleConstr -s <file postfix> --bi scripts/keep_and_drop_input.txt --bo scripts/keep_and_drop_output.txt

A more in-depth explanation of the script features:
* the `-s`,`--postfix` option is used to specify the suffix that will be appended to the input file name to obtain the output file name. It defaults to *_Friend* in friend mode, *_Skim* in full mode.
* the `-c`,`--cut` option is used to pass a string expression (using the same syntax as in TTree::Draw) that will be used to select events. It cannot be used in friend mode.
* the `-J`,`--json` option is used to pass the name of a JSON file that will be used to select events. It cannot be used in friend mode.
* if run with the `--full` option (default), the output will be a full nanoAOD file. If run with the `--friend` option, instead, the output will be a friend tree that can be attached to the input tree. In the latter case, it is not possible to apply any kind of event selection, as the number of entries in the parent and friend tree must be the same.
* the `-b`,`--branch-selection` option is used to pass the name of a file containing directives to keep or drop branches from the output tree. The file should contain one directive among `keep`/`drop` (wildcards allowed as in TTree::SetBranchStatus) or `keepmatch`/`dropmatch` (python regexp matching the branch name) per line, as shown in the [this](python/postprocessing/examples/keep_and_drop.txt) example file.
  * `--bi` and `--bo` allows to specify the keep/drop file separately for input and output trees.  
* the `--justcount` option will cause the script to printout the number of selected events, without actually writing the output file.

Please run with `--help` for a complete list of options.

