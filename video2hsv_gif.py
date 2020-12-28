import argparse
import moviepy.editor as mp
import numpy as np
from skimage import io
from skimage import color

parser = argparse.ArgumentParser()
parser.add_argument("-i", dest='filename', type=str, default = './Christmas_Tree.mp4')
parser.add_argument("--n_frames", dest='n_frames',type=int, default = 30)
parser.add_argument("--fps", dest='fps',type=int, default = 20)
parser.add_argument("--duration", dest='duration', type=float, default =1)
parser.add_argument("--boomerang", dest='boomerang', type=bool, default=True)
parser.add_argument("--annotation", dest='annotation', type=str, default='')

args = parser.parse_args()

n_frames = args.n_frames
fps = args.fps
duration = args.duration
is_boomerang = args.boomerang
text_annotation = args.annotation

filename = args.filename
filename_out = './' + ''.join(filename.split('.')[0:-1]) + '_hsv.gif'

clip = mp.VideoFileClip(filename)

frame_skip_rate = int((clip.fps * clip.duration) / (fps * duration))
if is_boomerang:
    frame_skip_rate *= 2

frames_gif = []
for i, frame in enumerate(clip.iter_frames()):
    if(i % frame_skip_rate == 0):
        frames_gif.append(frame)

if is_boomerang:
    frames_reversed = frames_gif.copy()
    frames_reversed.reverse()
    for i in range(1, len(frames_reversed)-1):
        frames_gif.append(frames_reversed[i])


frames_gif = [frames[i] for i in range(38)]
hsv_shifts = np.linspace(0,1, len(frames_gif), False)

frames_hsv_shift = []
for i in range(len(hsv_shifts)):
    img_hsv = color.rgb2hsv(frames_gif[i])
    hue = img_hsv[:,:,0]
    hue_shift = (hue + hsv_shifts[i]) % 1
    img_hsv[:,:,0] = hue_shift
    img_hsv_shift_rgb = 255*color.hsv2rgb(img_hsv)
    img_hsv_shift_rgb = img_hsv_shift_rgb.astype(np.uint8)
    frames_hsv_shift.append(img_hsv_shift_rgb)

clip_out = mp.ImageSequenceClip(frames_hsv_shift, fps = fps)

text_clip = mp.TextClip(text_annotation, font ="Helvetica-Bold",
fontsize = 156, color ="white",
stroke_color='black', stroke_width = 4, align='center')
text_clip = text_clip.set_duration(clip_out.duration)
#text_clip = text_clip.set_pos('top')
text_clip = text_clip.set_position((0.12,0.02), relative=True)
clip_out_text = mp.CompositeVideoClip([clip_out, text_clip])
clip_small = clip_out_text.resize(width=240)

clip_small.write_gif(filename_out)
os.system("gifsicle -i " + filename_out + " -O3 --colors 256 -o normal_holidays_2020_opt.gif")
