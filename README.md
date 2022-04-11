# SCING: Single-Cell pIpeliNe Garden

Pronounced as "sing" /siŋ/

Unified framework for building and running single-cell computational pipelines

<pre>
 ______     ______     __     __   __     ______
/\  ___\   /\  ___\   /\ \   /\ "-.\ \   /\  ___\
\ \___  \  \ \ \____  \ \ \  \ \ \-.  \  \ \ \__ \
 \/\_____\  \ \_____\  \ \_\  \ \_\\"\_\  \ \_____\
  \/_____/   \/_____/   \/_/   \/_/ \/_/   \/_____/

</pre>

Pipeline          | Description                                              | Version
----------------- | ---------------------------------------------------------|---------
SEQC              | Single-cell & Single-nucleus RNA-seq 3' Preprocessor     | 0.2.11
SEQC Ada          | SEQC AutomateD Analysis                                  | 0.0.4
Sharp (♯)         | Demultiplexing Hashtag, CITE-seq, CellPlex, and ASAP-seq | 0.1.0
Velopipe          | RNA Velocity for SEQC                                    | 0.0.9
FastQC            | A high throughput sequence QC analysis tool              | 0.11.9
Transgenes        | Creating a reference package with transgenes             | 0.0.8
Cell Ranger GEX   | Single-cell gene expression (3' and 5')                  | 6.1.2
Cell Ranger V(D)J | Single-cell immune profiling (TCR/BCR)                   | 6.1.2
Cell Ranger ATAC  | Single-cell chromatin accessbility (ATAC)                | 2.0.0
Cell Ranger ARC   | Single-cell multiome ATAC + Gene Expression              | 2.0.0
Space Ranger      | Single-cell spatial gene expression                      | 1.3.1
CellPlex          | Cell multiplexing                                        | 6.1.2
mkref             | Creating a human+mouse hybrid genome                     | 0.0.6

Coming Soon

Pipeline          | Description
----------------- | --------------------------------------------------------------
ArchR             | Processing and analyzing single-cell ATAC-seq data
Mito Tracing      | Lineage tracing using mitochondrial mutations

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
cd scing
pip install .
```

If you are a developer of SCING, additionally install either JRE or JDK. Here are some options for installing JRE or JDK:

JRE (Java 8 packaged by Cyclus):

```bash
conda install -c cyclus java-jre
```

JDK (Zulu OpenJDK v11):

```bash
conda install -c conda-forge openjdk
```

On HPC:

```bash
module add java/11.0.12
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
ls -1 *.tar.gz | xargs -I {} bash -c "tar xvzf {} && rm -rf {}"
```
