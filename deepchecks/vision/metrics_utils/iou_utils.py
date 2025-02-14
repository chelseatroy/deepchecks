# ----------------------------------------------------------------------------
# Copyright (C) 2021-2022 Deepchecks (https://www.deepchecks.com)
#
# This file is part of Deepchecks.
# Deepchecks is distributed under the terms of the GNU Affero General
# Public License (version 3 or later).
# You should have received a copy of the GNU Affero General Public License
# along with Deepchecks.  If not, see <http://www.gnu.org/licenses/>.
# ----------------------------------------------------------------------------
#
"""Module for computing Intersection over Unions."""
import numpy as np


def jaccard_iou(dt, gt):
    """Calculate the jaccard IoU.

    See https://en.wikipedia.org/wiki/Jaccard_index
    """
    x_dt, y_dt, w_dt, h_dt = dt[:4]
    x_gt, y_gt, w_gt, h_gt = gt[1:]

    x2_dt, y2_dt = x_dt + w_dt, y_dt + h_dt
    x2_gt, y2_gt = x_gt + w_gt, y_gt + h_gt

    # innermost left x
    xi = max(x_dt, x_gt)
    # innermost right x
    x2i = min(x2_dt, x2_gt)
    # same for y
    yi = max(y_dt, y_gt)
    y2i = min(y2_dt, y2_gt)

    # calculate areas
    dt_area = float(w_dt * h_dt)
    gt_area = float(w_gt * h_gt)
    intersection = float(max(x2i - xi, 0)) * float(max(y2i - yi, 0))
    return float(intersection / (dt_area + gt_area - intersection))


def compute_pairwise_ious(detected, ground_truth):
    """Compute pairwise ious between detections and ground truth."""
    ious = np.zeros((len(detected), len(ground_truth)))
    for g_idx, g in enumerate(ground_truth):
        for d_idx, d in enumerate(detected):
            ious[d_idx, g_idx] = jaccard_iou(d, g)
    return ious
