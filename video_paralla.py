import os
import random
import json
import math
import numpy as np
from tqdm import tqdm
from multiprocessing import Pool, cpu_count
from PIL import Image
import moviepy.editor as mp

# Set batch size to process 5 videos at a time
BATCH_SIZE = 5

def zoom_effect(clip, zoom_ratio=0.04):
    def effect(get_frame, t):
        img = Image.fromarray(get_frame(t))
        base_size = img.size
        new_size = [
            math.ceil(img.size[0] * (1 + (zoom_ratio * t))),
            math.ceil(img.size[1] * (1 + (zoom_ratio * t))),
        ]
        new_size[0] += new_size[0] % 2
        new_size[1] += new_size[1] % 2
        img = img.resize(new_size, Image.LANCZOS)
        x = math.ceil((new_size[0] - base_size[0]) / 2)
        y = math.ceil((new_size[1] - base_size[1]) / 2)
        img = img.crop([x, y, new_size[0] - x, new_size[1] - y]).resize(base_size, Image.LANCZOS)
        return np.array(img)
    return clip.fl(effect)


def pan_effect(clip, pan_ratio, direction):
    def effect(get_frame, t):
        img = Image.fromarray(get_frame(t))
        base_size = img.size

        if direction in ["left", "right"]:
            new_width = math.ceil(base_size[0] / (1 - pan_ratio))
            new_size = (new_width, base_size[1])
        else:
            new_height = math.ceil(base_size[1] / (1 - pan_ratio))
            new_size = (base_size[0], new_height)

        img = img.resize(new_size, Image.LANCZOS)

        if direction == "right":
            x = int((new_size[0] - base_size[0]) * (t / clip.duration))
            y = 0
        elif direction == "left":
            x = int((new_size[0] - base_size[0]) * (1 - t / clip.duration))
            y = 0
        elif direction == "down":
            x = 0
            y = int((new_size[1] - base_size[1]) * (t / clip.duration))
        else:
            x = 0
            y = int((new_size[1] - base_size[1]) * (1 - t / clip.duration))

        img = img.crop([x, y, x + base_size[0], y + base_size[1]])
        return np.array(img)
    return clip.fl(effect)


def create_video_for_sentence(params):
    key, audio_path, image_folder, output_path, target_resolution, effect_type = params

    images = [f for f in os.listdir(image_folder) if "facefix" in f and f.endswith(".png")]

    if not images:
        print(f"❌ No 'facefix' images found in {image_folder}, skipping.")
        return None

    selected_image = random.choice(images)
    image_path = os.path.join(image_folder, selected_image)

    try:
        audio_clip = mp.AudioFileClip(audio_path)
        image_clip = (
            mp.ImageClip(image_path)
            .set_duration(audio_clip.duration)
            .resize(target_resolution)
        )

        if effect_type is None:
            effect_type = random.choice(["zoom_in", "zoom_out", "pan"])

        if effect_type == "zoom_in":
            effected_clip = zoom_effect(image_clip, 0.06)
        elif effect_type == "zoom_out":
            effected_clip = zoom_effect(image_clip, 0.06).fx(mp.vfx.time_mirror)
        elif effect_type == "pan":
            direction = random.choice(["left", "right", "up", "down"])
            effected_clip = pan_effect(image_clip, 0.06, direction)
        else:
            raise ValueError("effect_type must be 'zoom_in', 'zoom_out', 'pan', or None")

        final_clip = effected_clip.set_audio(audio_clip)
        
        # Enable multi-threaded GPU rendering
        final_clip.write_videofile(output_path, fps=30, threads=4, logger=None)  

        return output_path

    except Exception as e:
        print(f"❌ Failed to create video for {key}: {e}")
        return None


def generate_and_concatenate_videos(
    audio_base_path,
    images_base_path,
    sentences,
    output_folder,
    final_output_path,
    target_resolution=(1920, 1080),
    effect_type=None,
):
    os.makedirs(output_folder, exist_ok=True)

    video_params = []
    for key, value in sentences.items():
        audio_file = os.path.join(audio_base_path, f"{key}.wav")
        image_folder = os.path.join(images_base_path, key)
        output_video = os.path.join(output_folder, f"{key}.mp4")

        if not os.path.exists(audio_file):
            print(f"⚠️ Audio file {audio_file} does not exist, skipping.")
            continue

        if not os.path.exists(image_folder):
            print(f"⚠️ Image folder {image_folder} does not exist, skipping.")
            continue

        video_params.append((key, audio_file, image_folder, output_video, target_resolution, effect_type))

    # Process videos in batches of 5
    batch_count = math.ceil(len(video_params) / BATCH_SIZE)
    processed_videos = []

    for i in range(batch_count):
        batch = video_params[i * BATCH_SIZE : (i + 1) * BATCH_SIZE]
        
        with Pool(min(BATCH_SIZE, cpu_count())) as pool:
            results = list(tqdm(pool.imap(create_video_for_sentence, batch), total=len(batch), desc=f"Processing Batch {i+1}/{batch_count}"))

        processed_videos.extend([r for r in results if r])

    # Load video clips after batch processing
    video_clips = [mp.VideoFileClip(v) for v in processed_videos]

    if video_clips:
        final_clip = mp.concatenate_videoclips(video_clips)
        
        # Enable multi-threaded GPU rendering
        final_clip.write_videofile(final_output_path, fps=30, threads=4, logger=None) 


if __name__ == "__main__":
    base_folder = r"E:\Ember_V2\ember_2.0\data\20250208221146"

    json_file = os.path.join(base_folder, f"codex_{os.path.basename(base_folder)}.json")
    with open(json_file, "r", encoding="utf-8") as file:
        story_data = json.load(file)

    images_output_folder = story_data.get("images_output")
    audio_folder = os.path.join(base_folder, "verba")
    video_output_folder = os.path.join(base_folder, "visix")
    final_video_output = os.path.join(base_folder, "final_story.mp4")

    if not images_output_folder:
        raise ValueError("images_output field not found in the JSON configuration.")

    # Generate videos in parallel (batch processing)
    generate_and_concatenate_videos(
        audio_folder,
        images_output_folder,
        story_data.get("sentences", {}),
        video_output_folder,
        final_video_output,
        target_resolution=(1920, 1080),
        effect_type=None,
    )

    # Update JSON
    story_data["video_output"] = final_video_output
    with open(json_file, "w", encoding="utf-8") as file:
        json.dump(story_data, file, indent=4)

    print(f"✅ Final video has been generated at {final_video_output}")
    print(f"✅ Updated JSON with video paths saved to {json_file}")
