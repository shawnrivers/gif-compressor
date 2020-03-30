from moviepy.editor import *
import sys
import os
import numpy as np

min_fps = 10
min_colors = 40
min_dimension = 160

limit_size = 1000000

# FUNCTIONS DEFINATION
# Get the width of the clip.


def getClipWidth(clip):
    # Get the first frame of the clip.
    frame = clip.get_frame(0)
    return np.size(frame, 1)

# Get the height of the clip.


def getClipHeight(clip):
    # Get the first frame of the clip.
    frame = clip.get_frame(0)
    return np.size(frame, 0)

# Tell the side with the least pixels ("width"/"height").


def getClipSide(clip):
    # Return the dimension with the smallest value.
    if (getClipWidth(clip) < getClipHeight(clip)):
        return 'width'
    else:
        return 'height'

# Get the dimension of the smallest side.


def getClipDimension(clip):
    return min(getClipWidth(clip), getClipHeight(clip))

# Get the total frames count of the clip.


def getClipFramesCount(clip):
    return int(clip.fps * clip.duration)

# Get the size of a file.


def getFileSize(path):
    return os.path.getsize(path)

# Show the info of the original clip.


def showOrigInfo(width, height, framesCount, fps, duration, colors, size):
    print('  Dimension: %d * %d' % (width, height))
    print('  Frames Count: %(fr)d (%(fps)d fps *  %(du).2f s)' %
          {'fr': framesCount, 'fps': fps, 'du': duration})
    print('  File Size: %d KB\n' % (size / 1000))

# Show the changes after compression.


def showChangedInfo(width, height, framesCount, fps, duration, colors, size,
                    orig_width, orig_height, orig_framesCount,
                    orig_fps, orig_duration, orig_size):
    print('  Dimension: %(orig_wid)d * %(orig_hei)d -> %(curr_wid)d * %(curr_hei)d' %
          {'curr_wid': width, 'curr_hei': height, 'orig_wid': orig_width, 'orig_hei': orig_height})
    print('  Frames Count: %(orig_fr)d (%(orig_fps)d fps *  %(orig_du).2f s) -> %(curr_fr)d (%(curr_fps)d fps *  %(curr_du).2f s)' %
          {'orig_fr': orig_framesCount, 'orig_fps': orig_fps, 'orig_du': orig_duration,
           'curr_fr': framesCount, 'curr_fps': fps, 'curr_du': duration})
    print('  Colors Count: %d' % colors)
    print('  Size: %(orig)d KB -> %(curr)d KB\n' %
          {'orig': (orig_size / 1000), 'curr': (size / 1000)})


# Compress the clip.


def compressClip(clip_path):
    # Output file name and path setting.

    file_name, file_extension = os.path.splitext(clip_path)
    output_filename = file_name + '.gif'

    temp_path = os.path.join(os.getcwd(), 'output/', output_filename)

    clip = VideoFileClip(clip_path)

    # Store original clip information
    shortest_side = getClipSide(clip)
    original_dimension = getClipDimension(clip)
    original_width = getClipWidth(clip)
    original_height = getClipHeight(clip)
    original_fps = clip.fps
    original_duration = clip.duration
    original_framesCount = getClipFramesCount(clip)
    original_size = getFileSize(clip_path)

    print('\nOriginal Info:')
    showOrigInfo(original_width, original_height, original_framesCount,
                 original_fps, original_duration, 0, original_size)

    # PRE-COMPRESSION
    # Change color count.
    current_colorsCount = 64

    # Set a variable for changing dimension.
    if original_dimension > 300:
        current_dimension = 300
    else:
        current_dimension = original_dimension

    # Change dimension based on the shortest side.
    if shortest_side == 'width':
        temp_clip = clip.resize(width=current_dimension)
    else:
        temp_clip = clip.resize(height=current_dimension)

    # Change fps.
    if original_fps > 15:
        current_fps = 15
    else:
        current_fps = original_fps

    # Compress to a gif file.
    temp_clip.write_gif(temp_path, fps=current_fps, program='ffmpeg',
                        colors=current_colorsCount, tempfiles=True)

    temp_clip = VideoFileClip(temp_path)
    current_size = getFileSize(temp_path)
    current_framesCount = getClipFramesCount(temp_clip)
    current_duration = temp_clip.duration
    print('\n\n1-time compression finished.')
    showChangedInfo(getClipWidth(temp_clip), getClipHeight(temp_clip),
                    current_framesCount, temp_clip.fps, current_duration,
                    current_colorsCount, current_size, original_width,
                    original_height, original_framesCount, original_fps,
                    original_duration, original_size)

    # COMPRESSION
    compression_counter = 1
    real_counter = 1

    while True:
        if (current_size < limit_size) or (current_fps <= min_fps and current_dimension <= min_dimension and current_colorsCount <= min_colors):
            # os.rename(temp_path, output_path)
            print('Ouput file saved to %s\n' % temp_path)
            break

        # Compression settings
        if compression_counter == 0:
            if original_dimension > 300:
                current_dimension = 300
                real_counter += 1
                compression_counter += 1
            else:
                compression_counter += 1
                continue
        elif compression_counter == 1:
            if original_dimension > 260:
                current_dimension = 260
                real_counter += 1
                compression_counter += 1
            else:
                compression_counter += 1
                continue
        elif compression_counter == 2:
            if original_fps > 12:
                current_fps = 12
                real_counter += 1
                compression_counter += 1
            else:
                compression_counter += 1
                continue
        elif compression_counter == 3:
            current_colorsCount = 56
            real_counter += 1
            compression_counter += 1
        elif compression_counter == 4:
            if original_dimension > 220:
                current_dimension = 220
                real_counter += 1
                compression_counter += 1
            else:
                compression_counter += 1
                continue
        elif compression_counter == 5:
            current_colorsCount = 48
            real_counter += 1
            compression_counter += 1
        elif compression_counter == 6:
            if original_dimension > 200:
                current_dimension = 200
                real_counter += 1
                compression_counter += 1
            else:
                compression_counter += 1
                continue
        elif compression_counter == 7:
            current_colorsCount = 40
            real_counter += 1
            compression_counter += 1
        elif compression_counter == 8:
            if original_fps > 10:
                current_fps = 10
                real_counter += 1
                compression_counter += 1
            else:
                compression_counter += 1
                continue
        elif compression_counter == 9:
            if original_dimension > 160:
                current_dimension = 160
                real_counter += 1
                compression_counter += 1
            else:
                compression_counter += 1
                continue

        # Execute the compression
        # Change dimension based on the shortest side.
        if shortest_side == 'width':
            temp_clip = clip.resize(width=current_dimension)
        else:
            temp_clip = clip.resize(height=current_dimension)

        # Compress to a gif file.
        temp_clip.write_gif(temp_path, fps=current_fps, program='ffmpeg',
                            colors=current_colorsCount, tempfiles=True)

        temp_clip = VideoFileClip(temp_path)
        current_size = getFileSize(temp_path)
        current_framesCount = getClipFramesCount(temp_clip)
        current_duration = temp_clip.duration
        print('\n\n%d-time compression finished.' % (real_counter))
        showChangedInfo(getClipWidth(temp_clip), getClipHeight(temp_clip),
                        current_framesCount, temp_clip.fps, current_duration,
                        current_colorsCount, current_size, original_width,
                        original_height, original_framesCount, original_fps,
                        original_duration, original_size)


# MAIN EXECUTION
files_count = len(sys.argv) - 1

for i in range(files_count):
    clip_path = str(sys.argv[i + 1])

    print('\n----------------------------------------------\nCurrent job: %s' % clip_path)
    print('\nOverall progress: %(current)d/%(overall)d Started.' %
          {'current': (i + 1), 'overall': files_count})

    compressClip(clip_path)

    print('\nOverall progress: %(current)d/%(overall)d Finished.' %
          {'current': (i + 1), 'overall': files_count})
