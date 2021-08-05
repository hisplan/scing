# SCING: Single-Cell pIpeliNe Garden

Pronounced as "sing" /siŋ/

<pre>
 ______     ______     __     __   __     ______
/\  ___\   /\  ___\   /\ \   /\ "-.\ \   /\  ___\
\ \___  \  \ \ \____  \ \ \  \ \ \-.  \  \ \ \__ \
 \/\_____\  \ \_____\  \ \_\  \ \_\\"\_\  \ \_____\
  \/_____/   \/_____/   \/_/   \/_/ \/_/   \/_____/

</pre>

Pipeline   | Description
---------- | --------------------------------------------------------------
SEQC       | Single-Cell & Single-Nucleus RNA-seq 3' Preprocessor
SEQC Ada   | SEQC Automated Analysis
Sharp (♯)  | Demultiplexing Hashtag, CITE-seq, Cell Plex, and ASAP-seq
Velopipe   | RNA Velocity using SEQC
FastQC     | A high throughput sequence QC analysis tool

## Build

All the required docker containers are pre-built and publicly accessible via [quay.io/hisplan](https://quay.io/user/hisplan). If you want to build the docker containers on your own and push them to your own docker registry, please follow the instructions [here](./docs/build.md). Otherwise, skip to the Install section.

## Install

```bash
conda create -n scing python=3.8 pip
conda activate scing
conda install -c cyclus java-jre
git clone https://github.com/hisplan/scing.git
pip install .
```

Run the following command to install everything:

```bash
scing install --config=build.yaml --home $HOME/scing/bin
```

Go to `$HOME/scing/bin` and extract everything:

```bash
cd $HOME/scing/bin
ls -1 | xargs -I {} tar xvzf {}
```

## How to Use Pipelines

Prerequisites:

- Cromwell
- AWS Genomics Workflow or GCP

TBD
