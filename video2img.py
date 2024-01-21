import argparse
import os
import os.path as osp
import pprint

import imageio
import tqdm


def toimg(in_file,prefix='', start=0, duration=None, per=1):
    end = None

    if duration:
        end = start + duration

    stem, ext = osp.splitext(in_file)
    if not osp.exists(stem):
        os.makedirs(stem)

    reader = imageio.get_reader(in_file)
    meta_data = reader.get_meta_data()

    i_offset = None
    for i in tqdm.trange(reader.count_frames()):
        elapsed_time = i * 1.0 / meta_data["fps"]
        if elapsed_time < start:
            continue
        if i_offset is None:
            i_offset = i

        if (i - i_offset) % per == 0:
            img = reader.get_data(i)
            img_file = osp.join(stem, "{}{:08d}.jpg".format(prefix,i))
            if not osp.exists(img_file):
                imageio.imsave(img_file, img)

        if end and elapsed_time >= end:
            break

    reader.close()
