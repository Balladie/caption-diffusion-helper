import argparse
import glob
import os
import shutil
from tqdm import tqdm
from PIL import Image
from pathlib import Path

import streamlit as st


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--image_dir', type=str, required=True)
    parser.add_argument('--caption_dir', type=str, required=True)
    return parser.parse_args()


def get_list_path(image_dir, caption_dir):
    image_glob_path = os.path.join(image_dir, '*.jpg')
    caption_glob_path = os.path.join(caption_dir, '*.txt')
    return sorted(glob.glob(image_glob_path)), sorted(glob.glob(caption_glob_path))


def check_validity_image_text_pair(list_image_path, list_caption_path):
    if not len(list_image_path) == len(list_caption_path):
        print('Numbers of image and caption are not matched!')
        print('Number of image:', len(list_image_path))
        print('Number of caption:', len(list_caption_path))
        raise AssertionError

    list_image_stem = list(map(lambda x: Path(x).stem, list_image_path))
    list_caption_stem = list(map(lambda x: Path(x).stem, list_caption_path))
    if list_image_stem != list_caption_stem:
        print('Validity check failed. Check if any of pairs is missing?')
        raise AssertionError


def iter_next_image(loc_image, loc_caption, list_image_path):
    st.session_state.idx += 1

    curr_image_path = list_image_path[st.session_state.idx]
    curr_caption_path = list_caption_path[st.session_state.idx]

    image = Image.open(curr_image_path)
    loc_image.image(image)

    with open(curr_caption_path, 'r') as f:
        caption_prev = f.read()
    loc_caption.write(caption_prev)


# initialize webpage configuration
st.set_page_config(page_title='Caption Helper', layout='centered', initial_sidebar_state='auto')

# parse arguments
args = parse_args()

# get list of image paths
list_image_path, list_caption_path = get_list_path(args.image_dir, args.caption_dir)

# check validity for image and caption pairs
check_validity_image_text_pair(list_image_path, list_caption_path)

# initialize index for image
if 'idx' not in st.session_state:
    st.session_state['idx'] = 0

# start with the first pair
curr_image_path = list_image_path[st.session_state.idx]
curr_caption_path = list_caption_path[st.session_state.idx]

# initialize image
image = Image.open(curr_image_path)
loc_image = st.empty()
loc_image.image(image)

# initialize caption text
with open(curr_caption_path, 'r') as f:
    caption_prev = f.read()
loc_caption = st.empty()
caption_input = loc_caption.write(caption_prev)

# initialize buttons
if st.button('Next'):
    iter_next_image(loc_image, loc_caption, list_image_path)