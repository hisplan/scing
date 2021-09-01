# Build

## Set Up Build Environment

The best way to build is set up an AWS EC2 instance and build the docker containers from there. Building from your local machine is definitely possible, but you will probably hear heavy CPU fan noise (and possibly some smoke).

Prerequisites:

- Miniconda
- Docker
- bash, curl, wget, tar, git

```bash
conda create -n scing python=3.8 pip
conda activate scing
conda install -c cyclus java-jre
git clone https://github.com/hisplan/scing.git
pip install .
```

## Configure

Set `registry` in `config.yaml` to your container registry.

The following will use, for example, `hisplan` in Docker Hub as your container registry. Replace `hisplan` with yours.

```yaml
versoin: 1.0
containers:
  registry: docker.io/hisplan
```

If you want to use Red Hat Quay.io:

```yaml
versoin: 1.0
containers:
  registry: quay.io/dpeerlab
```

where `dpeerlab` should be replaced with your own Quay.io namespace.

If you want to use Amazon ECR (EC2 Container Registry):

```yaml
versoin: 1.0
containers:
  registry: 583643567512.dkr.ecr.us-east-1.amazonaws.com
```

where `583643567512.dkr.ecr.us-east-1.amazonaws.com` should be replaced with your own AWS ECR.

## Log In to Your Container Registry

### Docker Hub

```bash
docker login
```

### Red Hat Quay.io

```bash
docker login quay.io
```

In addition to the login, you must set an OAuth access token so that the build script can create public repositories in Red Hat Quay.io:

```bash
export QUAY_AUTH_TOKEN="xyz-123-abc"
```

If you don't have one, you can create one by following [this instruction](https://access.redhat.com/documentation/en-us/red_hat_quay/3/html/red_hat_quay_api_guide/using_the_red_hat_quay_api#create_oauth_access_token).

### Amazon ECR

```bash
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 583643567512.dkr.ecr.us-east-1.amazonaws.com
```

where `583643567512.dkr.ecr.us-east-1.amazonaws.com` is your registry address.

## Build

In case some of the GitHub repositories are in private, you must set up GitHub auth token to access those private repositories. If everything is publicly available, you can skip this part.

```bash
export GIT_AUTH_TOKEN="abc-123-xyz"
```

10x software (e.g. Cell Ranger) will be dockerized. To do this, you must first sign the 10x Genomics End User Software License Agreement (EULA). To automate the build process (e.g. CI/CD), make sure you sign the 10x Genomics EULA first:

```bash
scing download \
  --site-url="https://support.10xgenomics.com/single-cell-gene-expression/software/downloads/6.0/" \
  --agree-eula
```

Run the build script:

```bash
scing build --config=config.yaml
```

## Job File

When you create a job file (e.g. a job file for scATAC-seq), make sure you set the `dockerRegistry` parameter to your own docker registry:

```
{
    "CellRangerATAC.sampleName": "test_sample1",
    "CellRangerATAC.fastqNames": "test_sample1",
    "CellRangerATAC.fastqFiles": [
        "s3://.../test_sample1_L001_I1_001.fastq.gz",
        "s3://.../test_sample1_L001_R1_001.fastq.gz",
        "s3://.../test_sample1_L001_R2_001.fastq.gz",
        "s3://.../test_sample1_L001_R3_001.fastq.gz",
    ],
    "CellRangerATAC.referenceGenome": {
        "name": "GRCh38-2020-A-2.0.0",
        "location": "https://cf.10xgenomics.com/supp/cell-atac/refdata-cellranger-arc-GRCh38-2020-A-2.0.0.tar.gz"
    },
    "CellRangerATAC.dockerRegistry": "${YOUR_DOCKER_REGISTRY}"
}
```
