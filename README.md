[![DOI](https://img.shields.io/badge/DOI-10.82901%2Fnemar.nm000460-blue)](https://doi.org/10.82901/nemar.nm000460)

# Spiking activity and LFP in human early visual cortex (V2/V3), one patient, stimulus-locked epochs: DERIVATIVE dataset

**This is a DERIVATIVE dataset: the signals are epoched around stimulus onset. No continuous recording was released.**
It repackages the public Open Science Framework registration "The effects of context and attention on human early visual
cortex." (Matthew Self, registered February 2016, doi:10.17605/OSF.IO/BRCZY, https://osf.io/brczy/, licence CC-By Attribution 4.0
International). The deposit holds the data of Self et al. 2016, PLoS Biology, doi:10.1371/journal.pbio.1002420. The same files
are also listed on EBRAINS; this copy was made from the OSF release.

## Participant and recording (from the paper)
One patient, a 35-year-old woman with late-onset epilepsy, normal IQ and no reported visual deficits. She had 15 depth electrodes
(AdTech) implanted under general anaesthesia by frameless stereotaxy. One electrode in visual cortex carried a microwire bundle
(40 um platinum-iridium side-wires between the clinical macro-contacts). Recordings from the microwires started 2 days after
surgery and continued for 7 more days. Two microwires, **E6 and E7**, recorded visually driven spiking activity. Their location is
**left occipital, V2/V3 per fMRI retinotopy**: the paper estimated it on post-explantation fMRI retinotopic maps of the left
hemisphere. **No electrode coordinates were released** (MRI/CT only on request from the Data Access Committee of the Netherlands
Institute for Neuroscience), so `electrodes.tsv` has x/y/z = n/a plus the stated region, hemisphere, material and the
post-explantation impedances (E6 158 kOhm, E7 115 kOhm).

Acquisition (paper): NeuraLynx HS-9 unity-gain head-stage, skull-screw ground, 32.5 kHz. E6/E7 re-referenced to the average of
microwires E0-E4 (E5 excluded because of noise). From this the authors made three signals, all released at FsD = 930.1714 Hz:
- **LFP**: down-sampled to 930 Hz, band-pass 1-200 Hz (2nd-order zero-phase Butterworth), 50 Hz removed by fitting and
  subtracting a sine per trial. Channel type SEEG (microwire LFP).
- **MUA**: multi-unit envelope. 500 Hz-5 kHz band-pass, rectified, down-sampled to 930 Hz, low-pass < 200 Hz. Channel type MISC.
- **MUAT**: thresholded MUA (MUAt). Channel type MISC.
The OSF document says MUA and MUAT are not normalised or baseline-corrected; in CURVET.mat (`curvetracing`), however, MUA is
baseline-subtracted (pre-stimulus mean ~0 per trial, 44% of samples negative). Units, from the paper's S1 Fig: LFP and MUA in
µV (scale bars of panels A and D; caption D: MUA "has units of microvolts"); MUAT is the spike-density function in Hz (caption H:
spike trains convolved with a Gaussian of integral one; 5641 of 6764 epochs integrate to a whole spike count, the other 1123 have
spike density within 12 samples of an epoch edge, where the kernel is cut). The BrainVision header carries no unit, so MNE reads
all channels as µV; MUAT values are spikes/s.

## Experiments (one task per OSF file)
Visual stimuli on a laptop LCD (60 Hz, 66 cm). Fixation within 2 deg near the top-left of the screen, else the trial was
aborted. Eye position was recorded with an EyeLink (1000 Hz).

| task | OSF file | epochs | epoch length (time re stimulus onset) | layout |
|---|---|---|---|---|
| `rfmapping` | RFmapping.mat | 1210 | 0.601 s (-0.200 to +0.400 s) | both electrodes in one run (trial-wise LFP residual correlation E6-E7 median 0.88 vs -0.10 shuffled within condition) |
| `orientation` | ORItuning.mat | 398 | 1.500 s (-0.399 to +1.100 s) | both electrodes in one run (trial-wise LFP residual correlation E6-E7 median 0.89 vs -0.14 shuffled within condition) |
| `spatialfreq` | SFtuning.mat | 100 | 1.100 s (-0.399 to +0.700 s) | both electrodes in one run (trial-wise LFP residual correlation E6-E7 median 0.90 vs -0.04 shuffled within condition) |
| `contrast` | CONTRASTtuning.mat | 320 | 1.100 s (-0.399 to +0.700 s) | both electrodes in one run (trial-wise LFP residual correlation E6-E7 median 0.88 vs -0.05 shuffled within condition) |
| `size` | SIZEtuning.mat | 200 | 1.300 s (-0.499 to +0.800 s) | both electrodes in one run (trial-wise LFP residual correlation E6-E7 median 0.90 vs -0.04 shuffled within condition) |
| `context` | CONTEXT.mat | 840 | 1.000 s (-0.399 to +0.600 s) | both electrodes in one run (identical eye traces; trial-wise LFP residual correlation E6-E7 median 0.88 vs -0.03 shuffled within condition) |
| `curvetracing` | CURVET.mat | 314 | 2.500 s (-0.499 to +2.000 s) | both electrodes in one run (identical eye traces; trial-wise LFP residual correlation E6-E7 median 0.89 vs -0.01 shuffled within condition) |

Channels per run: `E6_LFP`, `E7_LFP`, `E6_MUA`, `E7_MUA`, `E6_MUAT`, `E7_MUAT` (a per-electrode run has only its own three).
In the OSF files every trial appears once per electrode (rows = electrode x trial, `DETS` column 1 = electrode). We merged the
two electrodes' rows into one run only after checking that they come from the same trials: identical DETS sequence, plus
identical eye traces (CONTEXT, CURVET) or a trial-wise LFP correlation far above a within-condition shuffle.

## Files and how to read them
- `sub-01/ieeg/sub-01_task-<task>_ieeg.vhdr`: BrainVision, IEEE float32, the epochs of one experiment **concatenated in the
  OSF row order** (`RecordingType` epoched, `EpochLength` in the sidecar). **Epoch boundaries are discontinuities: do not filter
  across them.** Reshape to (epochs, channels, samples) or cut at `epoch_start` in events.tsv.
- `events.tsv`: one row per epoch at **stimulus onset** (t = 0 of the authors' time base `TD`), with every `DETS` column under
  a readable name (`events.json`) and a `trial_type` text. The context condition names are those of the OSF document
  (ORI 1 = 45 deg, ORI 2 = 135 deg, Sz 1 = 4 deg, Sz 2 = 6 deg). The paper's Methods give 60 and 150 deg for the central
  grating; we kept the deposit's wording.
- Totals: 1 participant, 7 experiments, 3382 epochs, 1.020 h of epoch time.
- float64 -> float32: max absolute deviation 1.52e-05. The files read back bit-exactly and through
  `mne.io.read_raw_brainvision`.
- Not converted: the eye traces (EYEX, EYEY, deg from fixation, 1000 Hz, own time base `eyetb`) of CONTEXT and CURVET. Their
  epochs are 1.000 s / 2.500 s at 1000 Hz against 0.9998 s / 2.4995 s of neural data, so concatenating them would not line up.
  They are in `sourcedata/osf-brczy/CONTEXT.mat` and `CURVET.mat`.

## Analysis notes from the paper
Trials with eye position more than 1 deg from fixation (10-15%) were discarded in the context and attention analyses. **That
selection is not applied here**: all deposited epochs are included. The curve-tracing events keep the deposit's `correct` column as is (values 0, 1, 2; the OSF document gives no code list).

## Ethics
Quoted verbatim from Self et al. 2016 (Materials and Methods, "Surgical Procedures and Patient Details"):

> The study was approved by the medical ethics board of the Free University Medical Center (protocol 2009/194). The patient gave written informed consent to participate in the study.

## sourcedata/osf-brczy/
The 8 OSF files ("Archive of OSF Storage"): the 7 .mat files and "Details of the dataset.docx" (the authors' description of the
variables and DETS columns). `osf_manifest.json` lists the original OSF sizes and md5 hashes, which matched on download. Two
privacy-only changes:
1. The MAT text header ("Created on: <weekday> <month> <day> <time> <year>") keeps only month and year; the day is set to 01.
   The data bytes are unchanged, and every variable reloads identically.
2. The docx creation/modification dates in docProps/core.xml are set to day 01. The document text is unchanged.
So md5 of these copies differs from OSF; get the byte-identical originals from https://osf.io/brczy/.

## Licence and citation
CC BY 4.0 (OSF licence "CC-By Attribution 4.0 International", 2016), kept. Cite the paper (Self, M. W., Peters, J. C., Possel, J. K., Reithler, J., Goebel, R., Ris, P., Jeurissen, D., Reddy, L., Claus, S., Baayen, J. C. & Roelfsema, P. R. The Effects of Context and Attention on Spiking Activity in Human Early Visual Cortex. PLoS Biology 14(3): e1002420 (2016). doi:10.1371/journal.pbio.1002420) and the data (Self, M. W. The effects of context and attention on human early visual cortex. Open Science Framework registration, 2016. doi:10.17605/OSF.IO/BRCZY).
The OSF document also asks users to contact the corresponding author (Matthew Self, Netherlands Institute for Neuroscience)
so that analyses do not overlap.
Changes made here (CC BY "indicate if changes were made"): format conversion to BIDS/BrainVision float32, events and sidecars
from the DETS tables and the paper, header dates in sourcedata reduced to month/year. No signal processing.

Funding (paper): NWO (OnderzoeksTalent 406-12-072; Brain and Cognition 433-09-208; ALW 823-02-010), EU FP7 (Marie-Curie
PITN-GA-2011-290011; ERC advanced grants 339490 and 269853; HBP 604102), Neuroscience Campus Amsterdam proof-of-concept grant.
