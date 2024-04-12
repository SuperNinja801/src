import os
import mne
import numpy as np
from dsp import DCPM
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import accuracy_score

# 读取数据并预处理
merged_epochs_list = []
labels_list = []
n_block =8
file_path = "F:\\eeg_data\\2024_4"

for idx_block in range(1, n_block):
    # Load data
    data_path = os.path.join(file_path, "2024-4-11-{}.cnt".format(idx_block))
    raw = mne.io.read_raw_cnt(data_path, eog=['HEO', 'VEO'], emg=['EMG'], ecg=['EKG'],
                              preload=True, verbose=False)
    raw.drop_channels(['M1', 'M2'])
    chan_names = raw.info["ch_names"]
    # Rereference
    # channels_of_interest = chan_names[:15]
    # raw.pick_channels(channels_of_interest)
    raw.set_eeg_reference(ref_channels='average')
    # raw.set_eeg_reference(ref_channels=['TP7', 'TP8'])
    # Bandpass Filter
    raw = raw.filter(l_freq=1, h_freq=10, method='iir')
    raw.set_eeg_reference(ref_channels=['TP7', 'TP8'])
    labels = [1,2]
    Xs = []
    # Epochs
    tmin=0
    tmax=0.8
    baseline=(0,0)
    events, event_id = mne.events_from_annotations(raw, event_id={'1': 1, '2': 2})
    epochs = mne.Epochs(raw, events, event_id=[1, 2], tmin=tmin, tmax=tmax,
                        baseline=baseline,
                        preload=True,
                        )
    epochs = epochs.get_data()

    idx_error = np.where(events[:, -1] == 1)[0]
    idx_correct = np.where(events[:, -1] == 2)[0]
    #4.7实验2是错误
    epochs_error = epochs[idx_error]  # trails*channels*samples
    epochs_correct = epochs[idx_correct]
    merged_epochs_list.append(epochs_error)
    merged_epochs_list.append(epochs_correct)
    labels_list.extend([0] * epochs_error.shape[0])
    labels_list.extend([1] * epochs_correct.shape[0])

X = np.concatenate(merged_epochs_list, axis=0)
y = np.array(labels_list)
print(y)
skf = StratifiedKFold(n_splits=7, shuffle=True, random_state=42)
accuracies = []
true_positives = 0
false_negatives = 0
for train_index, test_index in skf.split(X, y):
    X_train, X_test = X[test_index], X[train_index]
    y_train, y_test = y[test_index], y[train_index]

    estimator = DCPM(n_components=8)
    model = estimator.fit(X_train, y_train)
    p_labels = estimator.pre(X_test)
    for true_label, predicted_label in zip(y_test, p_labels):
        if true_label == 0 and predicted_label == 0:
            true_positives += 1
        elif true_label == 0 and predicted_label == 1:
            false_negatives += 1
    accuracy = accuracy_score(y_test, p_labels)
    accuracies.append(accuracy)

print("Cross-Validation Accuracies:", accuracies)
print("Mean Accuracy:", np.mean(accuracies))
true_positive_rate = true_positives / (true_positives + false_negatives)
print("True Positive Rate (for predicted label 0):", true_positive_rate)