# Receipt: Channel units from the paper (LFP/MUA µV, MUAT Hz)

**Claim**: Self et al. 2016 S1 Fig states the units: LFP and MUA in µV, MUAT (MUAt spike density) in Hz. MUA in CURVET.mat is baseline-subtracted, unlike the OSF document and the other 6 tasks.

**PR**: nemarDatasets/nm000460#3, receipt on top of head `e5e11b70`.

## Source
- Paper: Self MW et al. 2016, PLoS Biol, doi:10.1371/journal.pbio.1002420 (PMC4807817), S1 Fig (`pbio.1002420.s001.tif`, sha256 `09b5ff91…996e6247`, read 2026-10-22) and its caption:
  - (A) "The unprocessed signal (filtered between 0.1 Hz–9 kHz) on a single trial": 100 µV scale bar. LFP is this re-referenced signal, down-sampled and filtered.
  - (D) MUA: "This signal has units of microvolts, but we present normalized data throughout the manuscript." The panel has a 1 µV scale bar with the envelope at about 2-3 µV. The OSF data are not normalised (OSF docx).
  - (G) the trial-averaged MUA has a 1 µV scale bar, and (H) the spike density a 10 Hz scale bar.
  - (H) "The MUAt spike-density function, created by first binning the spike-times into bins of 1.1 ms duration and then convolving the spike-train with a 22.6 ms long Gaussian density function with a standard deviation of 3.2 ms and integral of one. The convolved spike-trains were averaged to produce the spike-density plot below with units of Hertz."
- Release: OSF registration brczy (doi:10.17605/OSF.IO/BRCZY), the 7 task files (`CONTEXT.mat`, `CONTRASTtuning.mat`, `CURVET.mat`, `ORItuning.mat`, `RFmapping.mat`, `SIZEtuning.mat`, `SFtuning.mat`). Each file's md5 equals `original_files.<name>.md5` in this repo's `sourcedata/osf-brczy/osf_manifest.json`.
- NEMAR nm000460 `origin/main` `d74475db176106824ed89f9caf388eb01a164664`: the 7 `sub-01/ieeg/sub-01_task-*_ieeg.{vhdr,eeg}`. Each `.eeg` sha256 equals its git-annex key at that commit.

## Method
- Release files read with scipy 1.18.1 `loadmat`: `LFP`, `MUA`, `MUAT` (epochs x samples, E6 and E7 rows per `DETS[:, 0]`), `TD` (time, s) and `FsD` (930.17 Hz).
- BIDS files read with MNE 1.13.2 `read_raw_brainvision`, `get_data(units="uV")`. The header has no unit, so this returns the stored float32 values. Each of the 42 channel series (7 tasks x E6/E7 x LFP/MUA/MUAT) was compared with float32 of the source, sample by sample.
- MUA baseline: the share of negative samples, and per epoch |mean| over [-0.2, 0) s.
- MUAT: per epoch, the integral `sum(MUAT) / FsD`. It counts as whole when it is within 1e-6 of an integer. Because the kernel has integral one, a spike whose 22.6 ms kernel lies fully inside the epoch adds exactly 1. Non-whole epochs are tested for MUAT > 0 within 12 samples of either edge (half the 22.6 ms kernel at 930 Hz, rounded up).

## Result
| file | sha256 | = git-annex key | md5 | = osf_manifest.json md5 |
|---|---|---|---|---|
| sub-01/ieeg/sub-01_task-context_ieeg.eeg | 1739725f7d2299e00a9d2fbf804d1b53fff51f2cd8fad8db8adf271ac1a1fcd7 | True | | |
| OSF CONTEXT.mat | 2d081d5005f7992bf808c5c1ba7d799fba1a07455d396f4541b2babb3ab3a3e5 | | 2ad196e11dd5d3389708af3f229e3756 | True |
| sub-01/ieeg/sub-01_task-contrast_ieeg.eeg | 62deb317405a4a2ad0e2ced6f42400afefeb01fcea8bcee8e85259b36b62f1cf | True | | |
| OSF CONTRASTtuning.mat | dbb39c5beb62d8ccdc35d37b62d5597290adfde35777d612bf6fa66e8291f3d6 | | e8620ffd7af574a2ce18cd1cc07f52c3 | True |
| sub-01/ieeg/sub-01_task-curvetracing_ieeg.eeg | 3fcf83aa8439867a296128bde7e81d2794b935ab54a3e2a9f4b0675e13a77a05 | True | | |
| OSF CURVET.mat | 7023b41a92532ef805515977b68572a3811d0a29966e7d82152163c169d9d591 | | 0fcd0b9fa8171b97d14c565f13c01844 | True |
| sub-01/ieeg/sub-01_task-orientation_ieeg.eeg | 88901df7fb9d181cf02a52bb08b75a0b71514d563da8be9499ab267693bbea18 | True | | |
| OSF ORItuning.mat | 17406410dcb7bae83864637b006e93fb878e4aad72f6f1a83f15026c5f83d3f6 | | 3a9a1041b96a2ce35298406ecf99e52e | True |
| sub-01/ieeg/sub-01_task-rfmapping_ieeg.eeg | c8216cad4c373246dd790567d2bfabe5f4015027ca5cae0684045bf60820e591 | True | | |
| OSF RFmapping.mat | 4eb7995000ed3ebf73b7bd0329690dea69963aaf8dc69fb2fdeb1023c86ffdcf | | 59af6a1a1c40da9ba65d2facbf7d5283 | True |
| sub-01/ieeg/sub-01_task-size_ieeg.eeg | cf158e3ddf4dadb0e7dccf459d452e886938478602d87772c521e2239d87fe7e | True | | |
| OSF SIZEtuning.mat | e86d8b9c0df1ae4675935fa2d74af93cc27e59fea92ce270402b74970df5ecb0 | | 964afaa44691892c4891a71659a3b656 | True |
| sub-01/ieeg/sub-01_task-spatialfreq_ieeg.eeg | 5835d7785e096a4812636dfedb55155750a404fecabcd1147b8fc940d3423f6e | True | | |
| OSF SFtuning.mat | 4d4c9dd1c8b110e6116241d164736d4429e18ffead6efb419d72809637410bf1 | | 77b8adf2a44aa5aff1762b569dc34232 | True |

| task | source | epochs per electrode | BIDS = float32(source) | LFP median abs | MUA median | MUA % < 0 | MUA mean over [-0.2, 0.0) s per epoch: median abs, max abs | MUAT epochs with integer integral | non-integer epochs with MUAT > 0 within 12 samples of an edge | MUAT spikes per epoch (integer epochs) |
|---|---|---:|---|---:|---:|---:|---|---:|---:|---|
| context | CONTEXT.mat | 840 | True | 34.4 | 2.328 | 0.0 | 2.2, 2.8 | 1449 of 1680 | 231 of 231 | 1-26 |
| contrast | CONTRASTtuning.mat | 320 | True | 30.2 | 2.260 | 0.0 | 2.2, 2.8 | 547 of 640 | 93 of 93 | 1-24 |
| curvetracing | CURVET.mat | 314 | True | 31.9 | 0.052 | 44.2 | 6.4e-16, 3.8e-15 | 530 of 628 | 98 of 98 | 3-41 |
| orientation | ORItuning.mat | 398 | True | 29.7 | 2.263 | 0.0 | 2.2, 2.9 | 681 of 796 | 115 of 115 | 3-31 |
| rfmapping | RFmapping.mat | 1210 | True | 22.1 | 2.425 | 0.1 | 2.5, 2.8 | 1905 of 2420 | 515 of 515 | 0-16 |
| size | SIZEtuning.mat | 200 | True | 28.4 | 2.497 | 0.0 | 2.5, 2.7 | 356 of 400 | 44 of 44 | 5-27 |
| spatialfreq | SFtuning.mat | 100 | True | 31.6 | 2.310 | 0.0 | 2.3, 2.7 | 173 of 200 | 27 of 27 | 4-20 |

- MUA (µV): the median envelope is 2.3-2.5 in the 6 uncorrected tasks, matching the ~2-3 µV envelope in S1 Fig D.
- MUAT: 5641 of 6764 epoch rows integrate to a whole spike count. All 1123 others have spike density within 12 samples of an epoch edge, where part of a kernel falls outside the epoch.
  - This corrects the README wording at the PR head, "each epoch integrates to a whole spike count". The README now gives these counts.
- CURVET.mat MUA is baseline-subtracted: 44.2% of samples are negative and the pre-stimulus mean is at most 3.8e-15 per epoch. The 6 other tasks are not (0.0-0.1% negative, pre-stimulus mean 2.2-2.9).
- Rows changed by the PR: units of the 42 rows of the 7 channels.tsv (LFP and MUA µV, MUAT Hz), and the curvetracing MUA description.

## Coverage
7 of 7 recordings and 7 of 7 release files, all 42 channel series and all epochs.

## Reproduce
```
uv run --no-project --with mne==1.13.2 --with scipy python code/receipts/2026-10-22_units-from-paper.py <nm000460 root> <nm000460 git clone> <dir with the 7 OSF brczy .mat>
```
Run on 2026-10-22 (Slurm job 13447977) on a NEMAR copy of `origin/main` `d74475d` and the OSF files (since deleted). The clone is used for the annex keys and `osf_manifest.json`.
