# dsv2pulseq

Create Pulseq sequence files from Siemens dsv simulation files.

## Dependencies & Installation

A Python environment with the dependencies can be installed with the provided yml file: `conda env create -f dsv2pulseq.yml`.
Afterwards run: `pip install .`.  

This package only depends on numpy and a slightly modified version of PyPulseq [1], which is added as a submodule.

## Sequence simulation

The sequence should be simulated in transversal orientation with phase-encode direction A->P and no FOV shift (which is the default).
It has to be simulated with RF phase output (sim /RFP+). Mandatory dsv files are "_INF", "_RFD", "_RFP", "_GRX", "_GRY" and "_GRZ".

## Create Pulseq output

The conversion can be started by running the script: `dsv_to_pulseq.py -o #OUT_FILE -r #REF_VOLT #IN_FILE_PREFIX`.  

The IN_FILE_PREFIX is the prefix of the dsv files, e.g. "gre" for "gre_XXX.dsv".
The OUT_FILE is the Pulseq output sequence file (default: "external.seq"). The reference voltage is the voltage the sequence was simulated with (default: 223.529007 V)
The Pulseq sequence has the same orientation as the original sequence, when running in "XYZ in TRA" mode. This can fail, if a sequence block in the original Siemens sequence uses a different rotation matrix.

The conversion can also be done in Python by running:
```
    from dsv2pulseq import read_dsv
    seq = read_dsv('/path/to/dsv/dsv_prefix')
    seq.write_pulseq('external.seq')
```

There is an experimental function to check the shapes of RF waveforms and gradients that plots the difference between the original and converted waveforms:
```
    from dsv2pulseq import check_dsv
    check_dsv('/path/to/dsv_original/dsv_prefix', '/path/to/dsv_pulseq/dsv_prefix')
```
Note that the RF and gradient waveforms might be slightly different due to fixed rotation matrices in the original sequence for some event blocks.

## References

[1] Ravi, Keerthi, Sairam Geethanath, and John Vaughan. "PyPulseq: A Python Package for MRI Pulse Sequence Design." Journal of Open Source Software 4.42 (2019): 1725., https://github.com/imr-framework/pypulseq
