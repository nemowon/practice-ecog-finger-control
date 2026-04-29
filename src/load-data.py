from pathlib import Path
import gc
from scipy.io import loadmat
import numpy as np
import pandas as pd

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
DEFAULT_SUBJECT_FILES = {
    "sub1": DATA_DIR / "sub1_comp.mat",
    "sub2": DATA_DIR / "sub2_comp.mat",
    "sub3": DATA_DIR / "sub3_comp.mat",
}


def load_subject(path):
    """Load a single .mat subject file."""
    return loadmat(path)


def load_all_subjects(data_dir=DATA_DIR):
    """Load all three subjects from the project data folder."""
    return {name: loadmat(path) for name, path in DEFAULT_SUBJECT_FILES.items()}


def find_good_channels(train_data, train_dg, subject_name,
                       var_low_percentile=1, var_high_percentile=99,
                       corr_threshold=0.01):
    """Identify good channels using variance and correlation filters."""
    n_channels = train_data.shape[1]

    variances = np.var(train_data, axis=0)
    var_low = np.percentile(variances, var_low_percentile)
    var_high = np.percentile(variances, var_high_percentile)

    var_good = set()
    var_bad_low = []
    var_bad_high = []
    for ch in range(n_channels):
        if variances[ch] < var_low:
            var_bad_low.append(ch)
        elif variances[ch] > var_high:
            var_bad_high.append(ch)
        else:
            var_good.add(ch)

    corr_good = set()
    corr_bad = []
    for ch in range(n_channels):
        ch_corrs = []
        for f in range(train_dg.shape[1]):
            r = np.abs(np.corrcoef(train_data[:, ch], train_dg[:, f])[0, 1])
            ch_corrs.append(r)
        max_corr = max(ch_corrs)
        if max_corr >= corr_threshold:
            corr_good.add(ch)
        else:
            corr_bad.append(ch)

    good_channels = sorted(var_good & corr_good)
    return good_channels


def unify_channels(*good_channels_lists):
    """Keep the minimum number of good channels across all subjects."""
    if not good_channels_lists:
        return []
    n_unified = min(len(ch_list) for ch_list in good_channels_lists)
    return [ch_list[:n_unified] for ch_list in good_channels_lists]


def select_channels(subject, final_indices):
    """Select channels from subject train/test data and labels."""
    return (
        subject["train_data"][:, final_indices],
        subject["test_data"][:, final_indices],
        subject["train_dg"],
    )


def downsample_array(array, factor=4):
    """Downsample along the first axis by keeping every factor-th sample."""
    return array[::factor]


def merge_subjects(train_arrays, dg_arrays):
    """Concatenate multiple subject arrays along the sample axis."""
    return np.concatenate(train_arrays, axis=0), np.concatenate(dg_arrays, axis=0)


def random_select_row(data, random_state=None):
    """Return a random row index and row from a DataFrame or NumPy array."""
    rng = np.random.default_rng(random_state)

    if isinstance(data, pd.DataFrame):
        n_rows = len(data)
        idx = int(rng.integers(0, n_rows))
        return idx, data.iloc[idx]

    if isinstance(data, np.ndarray):
        n_rows = data.shape[0]
        idx = int(rng.integers(0, n_rows))
        return idx, data[idx]

    raise TypeError("random_select_row only supports pandas DataFrame or NumPy ndarray.")


def process_all_subjects(data_dir=DATA_DIR, downsample_factor=4):
    """Load subjects, perform smart channel removal, downsample, and merge."""
    subjects = load_all_subjects(data_dir)

    good_ch_1 = find_good_channels(subjects["sub1"]["train_data"], subjects["sub1"]["train_dg"], "Subject 1")
    good_ch_2 = find_good_channels(subjects["sub2"]["train_data"], subjects["sub2"]["train_dg"], "Subject 2")
    good_ch_3 = find_good_channels(subjects["sub3"]["train_data"], subjects["sub3"]["train_dg"], "Subject 3")

    final_ch_1, final_ch_2, final_ch_3 = unify_channels(good_ch_1, good_ch_2, good_ch_3)

    sub1_train, sub1_test, sub1_dg = select_channels(subjects["sub1"], final_ch_1)
    sub2_train, sub2_test, sub2_dg = select_channels(subjects["sub2"], final_ch_2)
    sub3_train, sub3_test, sub3_dg = select_channels(subjects["sub3"], final_ch_3)

    sub1_train_ds = downsample_array(sub1_train, factor=downsample_factor)
    sub1_dg_ds = downsample_array(sub1_dg, factor=downsample_factor)
    sub2_train_ds = downsample_array(sub2_train, factor=downsample_factor)
    sub2_dg_ds = downsample_array(sub2_dg, factor=downsample_factor)
    sub3_train_ds = downsample_array(sub3_train, factor=downsample_factor)
    sub3_dg_ds = downsample_array(sub3_dg, factor=downsample_factor)

    X_train_all, y_train_all = merge_subjects(
        [sub1_train_ds, sub2_train_ds, sub3_train_ds],
        [sub1_dg_ds, sub2_dg_ds, sub3_dg_ds],
    )

    # Free large arrays
    del subjects, sub1_train, sub2_train, sub3_train
    del sub1_dg, sub2_dg, sub3_dg
    del sub1_train_ds, sub2_train_ds, sub3_train_ds
    del sub1_dg_ds, sub2_dg_ds, sub3_dg_ds
    gc.collect()

    return X_train_all, y_train_all, (final_ch_1, final_ch_2, final_ch_3)
<<<<<<< Updated upstream


if __name__ == "__main__":
    X_train_all, y_train_all, final_indices = process_all_subjects()
    print("Merged X shape:", X_train_all.shape)
    print("Merged y shape:", y_train_all.shape)
    idx, row = random_select_row(X_train_all)
    print("Random row index:", idx)
    print("Random row shape:", np.shape(row))
=======
>>>>>>> Stashed changes
