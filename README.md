# SCING: Single-Cell pIpeliNe Garden

Pronounced as "sing" /siŋ/

<pre>
 ______     ______     __     __   __     ______
/\  ___\   /\  ___\   /\ \   /\ "-.\ \   /\  ___\
\ \___  \  \ \ \____  \ \ \  \ \ \-.  \  \ \ \__ \
 \/\_____\  \ \_____\  \ \_\  \ \_\\"\_\  \ \_____\
  \/_____/   \/_____/   \/_/   \/_/ \/_/   \/_____/

</pre>

Pipeline          | Description
----------------- | --------------------------------------------------------------
SEQC              | Single-cell & Single-nucleus RNA-seq 3' Preprocessor
SEQC Ada          | SEQC AutomateD Analysis
Sharp (♯)         | Demultiplexing Hashtag, CITE-seq, CellPlex, and ASAP-seq
Velopipe          | RNA Velocity using SEQC
FastQC            | A high throughput sequence QC analysis tool
STAR Transgenes   | Creating a genome index for the STAR aligner with transgenes
Cell Ranger V(D)J | Single-cell immune profiling (TCR/BCR)

Soon

Pipeline          | Description
----------------- | --------------------------------------------------------------
Cell Ranger ATAC  | Single-cell chromatin accessbility (ATAC)

## Prerequisites

To use SCING, you need:

- Cromwell: a workflow management system for scientific workflows developed by the Broad Institute
- Amazon Web Services, Google Cloud Platform, Microsoft Azure, or HPC (with LSF, Slurm, ...)

If you need information about how to install Cromwell on Cloud/HPC, please follow the instructions below:

- Amazon Web Services: https://github.com/hisplan/cromwell-gwf-setup
- Google Cloud Platform: TBD
- Microsoft Azure: TBD
- HPC with LSF: TBD

## Build

All the required docker containers are pre-built and publicly available/accessible via [quay.io/hisplan](https://quay.io/user/hisplan), thus building the containers are optional. If you want to build the docker containers on your own and push them to your own docker registry, please follow the instructions [here](./docs/build.md). Otherwise, skip to the Install section.

## Install CLI (Command-Line Interface)

```bash
conda create -n scing python=3.8 pip
conda activate scing
conda install -c cyclus java-jre
git clone https://github.com/hisplan/scing.git
pip install .
```

## Install Pipelines

Run the following command to install all the pipelines:

```bash
scing install --config=build.yaml --home $HOME/scing/bin
```

Go to `$HOME/scing/bin` and extract everything:

```bash
cd $HOME/scing/bin
ls -1 | xargs -I {} tar xvzf {}
```
