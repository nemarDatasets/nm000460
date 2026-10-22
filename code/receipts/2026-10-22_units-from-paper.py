"""MUA/MUAT statistics of the 7 OSF brczy files and their nm000460 BrainVision copies.

Usage: python 2026-10-22_units-from-paper.py <nm000460 root> <nm000460 git clone> <osf dir>
"""

import hashlib
import json
import subprocess
import sys
from pathlib import Path

import mne
import numpy as np
import scipy.io

REV = "origin/main"
TASKS = {
    "context": "CONTEXT.mat",
    "contrast": "CONTRASTtuning.mat",
    "curvetracing": "CURVET.mat",
    "orientation": "ORItuning.mat",
    "rfmapping": "RFmapping.mat",
    "size": "SIZEtuning.mat",
    "spatialfreq": "SFtuning.mat",
}
BASELINE_S = (-0.2, 0.0)
INTEGER_TOL = 1e-6
EDGE = 12  # samples: half of the 22.6 ms kernel at 930 Hz, rounded up


def digest(path: Path, algo: str) -> str:
    h = hashlib.new(algo)
    with path.open("rb") as f:
        while chunk := f.read(1 << 24):
            h.update(chunk)
    return h.hexdigest()


def git(clone: Path, *args: str) -> str:
    out = subprocess.run(["git", "-C", clone, *args], capture_output=True, text=True)
    return out.stdout.strip() if out.returncode == 0 else "n/a"


def main(root: Path, clone: Path, osf: Path) -> None:
    print(f"mne {mne.__version__}, numpy {np.__version__}, scipy {scipy.__version__}")
    print(f"{REV} of the clone: {git(clone, 'rev-parse', REV)}")
    manifest = json.loads(
        git(clone, "show", f"{REV}:sourcedata/osf-brczy/osf_manifest.json")
    )
    print("\n| file | sha256 | = git-annex key | md5 | = osf_manifest.json md5 |")
    print("|---|---|---|---|---|")
    for task, mat in TASKS.items():
        rel = f"sub-01/ieeg/sub-01_task-{task}_ieeg.eeg"
        key = git(clone, "cat-file", "-p", f"{REV}:{rel}").rsplit("--", 1)[-1]
        sha = digest(root / rel, "sha256")
        print(f"| {rel} | {sha} | {key.startswith(sha)} | | |")
        md5 = digest(osf / mat, "md5")
        listed = manifest["original_files"][mat]["md5"]
        print(
            f"| OSF {mat} | {digest(osf / mat, 'sha256')} | | {md5} | {md5 == listed} |"
        )

    print(
        "\n| task | source | epochs per electrode | BIDS = float32(source) "
        "| LFP median abs | MUA median | MUA % < 0 "
        f"| MUA mean over [{BASELINE_S[0]}, {BASELINE_S[1]}) s per epoch: median abs, max abs "
        "| MUAT epochs with integer integral | non-integer epochs with MUAT > 0 "
        f"within {EDGE} samples of an edge | MUAT spikes per epoch (integer epochs) |"
    )
    print("|---|---|---:|---|---:|---:|---:|---|---:|---:|---|")
    for task, mat in TASKS.items():
        m = scipy.io.loadmat(osf / mat, squeeze_me=True)
        td, fs, electrode = m["TD"], float(m["FsD"]), m["DETS"][:, 0]
        vhdr = root / f"sub-01/ieeg/sub-01_task-{task}_ieeg.vhdr"
        raw = mne.io.read_raw_brainvision(vhdr, preload=True, verbose="error")
        # header unit empty: MNE reads µV, so units="uV" returns the stored float32 values
        same = all(
            np.array_equal(
                np.float32(m[sig][electrode == e]).ravel(),
                np.float32(raw.get_data(picks=[f"E{e}_{sig}"], units="uV")[0]),
            )
            for sig in ("LFP", "MUA", "MUAT")
            for e in (6, 7)
        )
        mua, muat = m["MUA"], m["MUAT"]
        window = (td >= BASELINE_S[0]) & (td < BASELINE_S[1])
        base = np.abs(mua[:, window].mean(1))
        integral = muat.sum(1) / fs
        integer = np.abs(integral - np.round(integral)) < INTEGER_TOL
        at_edge = (muat[:, :EDGE] > 0).any(1) | (muat[:, -EDGE:] > 0).any(1)
        counts = np.round(integral[integer]).astype(int)
        print(
            f"| {task} | {mat} | {mua.shape[0] // 2} | {same} "
            f"| {np.median(np.abs(m['LFP'])):.1f} | {np.median(mua):.3f} "
            f"| {100 * (mua < 0).mean():.1f} | {np.median(base):.2g}, {base.max():.2g} "
            f"| {integer.sum()} of {integer.size} "
            f"| {(~integer & at_edge).sum()} of {(~integer).sum()} "
            f"| {counts.min()}-{counts.max()} |"
        )


if __name__ == "__main__":
    main(Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3]))
