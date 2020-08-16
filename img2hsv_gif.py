import argparse
import moviepy.editor as mp
import numpy as np
from skimage import io
from skimage import color

parser = argparse.ArgumentParser()
parser.add_argument("-i", dest='filename', type=str, default = './PoolParty_2.png')
parser.add_argument("--n_frames", dest='n_frames',type=int, default = 30)
parser.add_argument("--fps", dest='fps',type=int, default = 20)
args = parser.parse_args()

n_frames = args.n_frames
fps = args.fps

filename = args.filename
filename_out = './' + ''.join(filename.split('.')[0:-1]) + '_hsv.gif'

img = io.imread(filename)
img = img[:,:,0:3]
img_hsv = color.rgb2hsv(img)
hsv_shifts = np.linspace(0,1, n_frames, False)
hsv_sequnece=[]

for shift in hsv_shifts:
    img_hsv_shift = img_hsv.copy()
    hue = img_hsv[:,:,0].copy()
    hue_shift = (hue + shift) % 1
    img_hsv_shift[:,:,0] = hue_shift
    img_hsv_shift_rgb = 255*color.hsv2rgb(img_hsv_shift)
    img_hsv_shift_rgb = img_hsv_shift_rgb.astype(np.uint8)
    hsv_sequnece.append(img_hsv_shift_rgb)

clip = mp.ImageSequenceClip(hsv_sequnece, fps = fps)
clip_small = clip.resize(width=300)
clip_small.write_gif(filename_out)
