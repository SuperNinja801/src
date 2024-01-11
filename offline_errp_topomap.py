import os
import mne
import numpy as np
import matplotlib.pyplot as plt

evoked_correct = []
evoked_error = []
n_block = 3
file_path = "E:\eeg_data\\2023_12"
for idx_block in range(1, n_block + 1):
    # Load data
    data_path = os.path.join(file_path, "1226-{}.cnt".format(idx_block))
    raw = mne.io.read_raw_cnt(data_path, eog=['HEO', 'VEO'], emg=['EMG'], ecg=['EKG'],
                              preload=True, verbose=False)
    raw.drop_channels(['M1', 'M2'])
    chan_names = raw.info["ch_names"]
    print(chan_names)
    # Rereference

    raw.set_eeg_reference(ref_channels='average')
    # raw.set_eeg_reference(ref_channels=['TP7', 'TP8'])
    # Bandpass Filter
    raw = raw.filter(l_freq=1, h_freq=10, method='iir')

    # Epochs
    events, event_id = mne.events_from_annotations(raw, event_id={'1': 1, '2': 2})
    epochs = mne.Epochs(raw, events, event_id=[1, 2], tmin=-0.2, tmax=1.0,
                        baseline=(-0.2, 0),
                        preload=True,
                        )
    epochs = epochs.get_data()

    idx_error = np.where(events[:, -1] == 1)[0]
    # 错误是1
    idx_correct = np.where(events[:, -1] == 2)[0]
    # idx_correct = np.setdiff1d(idx_correct, idx_error+1)
    # idx_correct = np.setdiff1d(idx_correct, idx_error-1)
    # idx_correct = np.setdiff1d(idx_correct, [30*i for i in range(12)])
    epochs_error = epochs[idx_error]
    epochs_correct = epochs[idx_correct]

    evoked_error.append(np.mean(epochs_error, axis=0))
    evoked_correct.append(np.mean(epochs_correct, axis=0))

evoked_correct = np.stack(evoked_correct, axis=0)
evoked_error = np.stack(evoked_error, axis=0)

evoked_correct_mean = np.mean(evoked_correct, axis=0) * 1e6
evoked_error_mean = np.mean(evoked_error, axis=0) * 1e6
evoked_differ = evoked_error_mean - evoked_correct_mean
print(evoked_error_mean.shape)
# In[]: Time domain
fig = plt.figure(figsize=(6, 3), tight_layout=True)
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
ax = plt.gca()
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)

ylim = 5
idx_chan_list = [18]
for idx, idx_chan in enumerate(idx_chan_list):
    plt.subplot(len(idx_chan_list), 1, idx + 1)
    x_time = np.linspace(-0.2, 1.0, evoked_correct_mean.shape[1])
    plt.plot(x_time, evoked_correct_mean[idx_chan],
             linewidth=2, color=[127 / 255, 203 / 255, 164 / 255], label='Correct')
    plt.plot(x_time, evoked_error_mean[idx_chan],
             linewidth=2, color=[164 / 255, 5 / 255, 69 / 255], label='Error')
    plt.plot(x_time, evoked_differ[idx_chan], linewidth=1, color='b', label='Difference')

    plt.plot([0, 0], [-ylim, ylim], linewidth=0.5, color='grey', linestyle='--')
    plt.xticks(np.arange(-0.2, 1.6, 0.2), fontsize=14)
    plt.xlim([-0.2, 1])
    plt.ylim([-ylim, ylim])
    plt.yticks(fontsize=14)
    plt.xlabel('Time (s)', fontsize=16)
    plt.ylabel('Amplitude (μV)', fontsize=16)
    plt.text(-0.35, ylim - 1.5, '{}'.format(chan_names[idx_chan]), fontsize=18)
    plt.legend(loc='upper right', fontsize=8, frameon=False)

# plt.savefig('2.png', dpi=300)
plt.show()

# In[]:
# locs文件地址
locs_info_path = "64-channels.loc"

chan_drop = ['CB1', 'CB2']

idx_chan_drop = [chan_names.index(c) for c in chan_drop]
evoked_correct_mean2 = np.delete(evoked_correct_mean.copy(), idx_chan_drop, axis=0)
evoked_error_mean2 = np.delete(evoked_error_mean.copy(), idx_chan_drop, axis=0)
evoked_differ_2 = evoked_error_mean2 - evoked_correct_mean2
new_chan_names = chan_names.copy()
for idx_chan in range(len(chan_drop)):
    new_chan_names.remove(chan_drop[idx_chan])
montage = mne.channels.read_custom_montage(locs_info_path)
info = mne.create_info(ch_names=new_chan_names, sfreq=1000., ch_types='eeg')
evoked_correct_mean2 = mne.EvokedArray(evoked_correct_mean2, info)
evoked_correct_mean2.set_montage(montage)
evoked_error_mean2 = mne.EvokedArray(evoked_error_mean2, info)
evoked_error_mean2.set_montage(montage)
evoked_differ_2 = mne.EvokedArray(evoked_differ_2, info)
evoked_differ_2.set_montage(montage)
fig, ax = plt.subplots(nrows=5, ncols=10, figsize=(15, 10))
# 正确的脑地形图
# for i in range(50):
#     row_idx = i // 10  # 行索引
#     col_idx = i % 10  # 列索引
#
#     # 使用 ax[row_idx, col_idx] 来指定子图
#     mne.viz.plot_topomap(evoked_error_mean2.data[:, int(200 + 20 * i)],
#                          evoked_error_mean2.info, show=False, axes=ax[row_idx, col_idx])
#
#     ax[row_idx, col_idx].set_title("{} ms".format(20 * i))
# fig.suptitle("Error Topomaps", fontsize=16)
# plt.show()
# 错误的脑地形图
# for i in range(50):
#     row_idx = i // 10  # 行索引
#     col_idx = i % 10  # 列索引
#
#     # 使用 ax[row_idx, col_idx] 来指定子图
#     mne.viz.plot_topomap(evoked_correct_mean2.data[:, int(200 + 20 * i)],
#                          evoked_correct_mean2.info, show=False, axes=ax[row_idx, col_idx])
#
#     ax[row_idx, col_idx].set_title("{} ms".format(20 * i))
# fig.suptitle("Correct Topomaps", fontsize=16)
# plt.show()
# 差异波的脑地形图
for i in range(50):
    row_idx = i // 10  # 行索引
    col_idx = i % 10  # 列索引

    # 使用 ax[row_idx, col_idx] 来指定子图
    mne.viz.plot_topomap(evoked_differ_2.data[:, int(200 + 20 * i)],
                         evoked_differ_2.info, show=False, axes=ax[row_idx, col_idx])

    ax[row_idx, col_idx].set_title("{} ms".format(20 * i))
fig.suptitle("Differ Topomaps", fontsize=16)
plt.show()