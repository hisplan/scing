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
Velopipe          | RNA Velocity for SEQC
FastQC            | A high throughput sequence QC analysis tool
STAR Transgenes   | Creating a genome index for the STAR aligner with transgenes
Cell Ranger GEX   | Single-cell gene expression (3' and 5')
Cell Ranger V(D)J | Single-cell immune profiling (TCR/BCR)
Cell Ranger ATAC  | Single-cell chromatin accessbility (ATAC)
Cell Ranger ARC   | Single-cell multiome ATAC + Gene Expression

Coming Soon

Pipeline          | Description
----------------- | --------------------------------------------------------------
ArchR             | Single-cell chromatin accessbility (ATAC)
mkref             | Creating a human+mouse hybrid genome
Space Ranger      | Single-cell spatial gene expression
CellPlex          | Cell multiplexing

## Prerequisites

To use SCING, you need:

- Cromwell: a workflow management system for scientific workflows developed by the Broad Institute
- Amazon Web Services, Google Cloud Platform, Microsoft Azure, or HPC (with LSF, Slurm, ...)

If you need information about how to install Cromwell on Cloud/HPC, please follow the instructions below:

- Amazon Web Services
  - Amazon Genomics Workflow: https://github.com/hisplan/cromwell-gwf-setup
  - Amazon Genomics CLI (AGC): TBD
- Google Cloud Platform: TBD
- Microsoft Azure: TBD
- HPC with LSF: TBD

## Install CLI (Command-Line Interface)

```bash
conda create -n scing python=3.8 pip
conda activate scing
git clone https://github.com/hisplan/scing.git
pip install .
```

If you are a developer of SCING, additionally install JRE or JDK. Here are some options to install JRE/JDK:

JRE (Java 8 packaged by Cyclus):

```
conda install -c cyclus java-jre
```

JDK (Zulu OpenJDK v11):

```
conda install -c conda-forge openjdk
```

## Build Containers

All the required docker containers are pre-built and publicly available/accessible via [quay.io/hisplan](https://quay.io/user/hisplan), thus building the containers are optional. If you want to build the docker containers on your own and push them to your own docker registry, please follow the instructions [here](./docs/build.md). Otherwise, skip to the Install section.

## Install Pipelines

Run the following command to install all the pipelines:

```bash
scing install --config=config.yaml --home $HOME/scing/bin
```

Go to `$HOME/scing/bin` and extract everything:

```bash
cd $HOME/scing/bin
ls -1 | xargs -I {} tar xvzf {}
```
