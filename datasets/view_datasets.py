#!/usr/bin/env python3
"""
As a sanity check, load the data from the source/target domains and display it

Note: sets CUDA_VISIBLE_DEVICES= so that it doesn't use the GPU.
"""
import os
import tensorflow as tf
import matplotlib.pyplot as plt

from absl import app
from absl import flags

import datasets

FLAGS = flags.FLAGS

flags.DEFINE_enum("source", None, datasets.names(), "What dataset to use as the source")
flags.DEFINE_enum("target", "", [""]+datasets.names(), "What dataset to use as the target")
flags.DEFINE_boolean("test", False, "Show test images instead of training images")

flags.mark_flag_as_required("source")


def display(name, data, feature_names, example=0):
    # Shape: examples, time steps, features
    num_examples, num_samples, num_features = data.shape

    fig, axes = plt.subplots(nrows=num_features, ncols=1,
        sharex=True, sharey=False)
    fig.suptitle(name)

    for i in range(num_features):
        ax = axes[i]

        x_list = list(range(0, num_samples))  # the x axis... basically ignore
        values = data[example, :, i]  # data we care about

        if feature_names is not None:
            label = feature_names[i]
        else:
            label = "#"+str(i)

        ax.plot(x_list, values)
        ax.set_ylabel(label)
        ax.set_ylim(auto=True)


def main(argv):
    # Don't bother using the GPU for this
    os.environ["CUDA_VISIBLE_DEVICES"] = ""

    # Input data
    if FLAGS.target != "":
        source_dataset, target_dataset = datasets.load_da(FLAGS.source, FLAGS.target)
    else:
        source_dataset = datasets.load(FLAGS.source)
        target_dataset = None

    if not FLAGS.test:
        source_data = source_dataset.train_data
        target_data = target_dataset.train_data \
            if target_dataset is not None else None
    else:
        source_data = source_dataset.test_data
        target_data = target_dataset.test_data \
            if target_dataset is not None else None

    source_feature_names = source_dataset.feature_names
    target_feature_names = target_dataset.feature_names \
        if target_dataset is not None else None

    display("Source", source_data, source_feature_names)

    if target_dataset is not None:
        display("Target", target_data, target_feature_names)

    plt.show()


if __name__ == "__main__":
    app.run(main)
