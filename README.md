# Installing tools

Conda and packages that can be installed via Conda.

```bash
# Install tools from ct.yaml
conda env create -n ct --file environments/ct.yaml

# Activate environment
source activate ct
```

Other programs installed in `external` directory, i.e. MiXCR version 2.1.12 and VDJTools version 1.1.10:

```bash
cd external
bash install_external_programs.sh
cd ..
```

# Example

Download the FASTQ files of one of the sample of [the study](https://trace.ddbj.nig.ac.jp/DRASearch/study?acc=SRP040329)). Then, randomly sample 10000 reads. It may take a while.

```bash
cd example
bash get_example.sh
cd ..
```

Run:

```bash
python ct-cl.py --file1 examples/data/sub1.fq --file2 examples/data/sub2.fq --out examples/output --molecule IGH
```
