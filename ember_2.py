import os
import json
import random
from tqdm import tqdm
import time
from generator import ImageGenerator
from langchain_openai import ChatOpenAI

# from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate
from langchain.schema.output_parser import StrOutputParser
from prompt_agent import image_prompt_generating_agent, youtube_thumbnail_prompt_generating_agent
import torch
from TTS.api import TTS
from pydub import AudioSegment
import os
import json
from datetime import datetime
import os
import random
import json
from tqdm import tqdm
import moviepy.editor as mp
import math
from PIL import Image
import numpy as np

from image_generator import *
from prompt_generator import *
from audio_generator import *
from video_generator import *

def ember_2(base_folder, num_iterations, story_or_summary = "summary", input_mp3_path = "sample_5.mp3"):
    # 2 Prompt Generator  ######################################
    
    
    # Find the JSON file that starts with "codex" in the provided directory
    json_file = None
    for file in os.listdir(base_folder):
        if file.startswith("codex") and file.endswith(".json"):
            json_file = os.path.join(base_folder, file)
            break

    if not json_file:
        raise FileNotFoundError("No codex JSON file found in the specified directory.")

    # Load the JSON file
    with open(json_file, "r", encoding="utf-8") as file:
        story_data = json.load(file)
    story_data["sentences"] = split_story_into_sentences(story_data.get( story_or_summary, {}))

    # Create thumbnail Prompt
    story_data["youtube_details"]["thumbnail_prompt"] = generate_thumbnail_prompt(
        story_data["youtube_details"]["youtube_title"], story_data.get( story_or_summary, {}), story_data["story_elements"]
    )
    print(f'prompt --> {story_data["youtube_details"]["thumbnail_prompt"]}')

    # Generate prompts for the sentences
    sentences_with_context = generate_context_for_sentences(
        story_data.get("sentences", {}), story_data.get(story_or_summary, {}), story_data["story_elements"]
    )

    # Generate prompts for the sentences
    sentences_with_prompts = generate_prompts_for_sentences(
        sentences_with_context, story_data.get(story_or_summary, {}), story_data["story_elements"]
    )
    # Update the story_data with the new prompts
    story_data["sentences"] = sentences_with_prompts

    # Save the updated JSON file
    with open(json_file, "w", encoding="utf-8") as file:
        json.dump(story_data, file, ensure_ascii=False,indent=4)

    print(f"Updated JSON saved to {json_file}")
    # 3 Image Generator######################################

    
    # Extract the timestamp from the base folder path
    timestamp = extract_timestamp_from_path(base_folder)

    # Find the JSON file that starts with "codex" in the provided directory
    json_file = None
    for file in os.listdir(base_folder):
        if file.startswith("codex") and file.endswith(".json"):
            json_file = os.path.join(base_folder, file)
            break

    if not json_file:
        raise FileNotFoundError("No codex JSON file found in the specified directory.")

    # Load the JSON file
    with open(json_file, "r", encoding="utf-8") as file:
        story_data = json.load(file)

    # Server and workflow configurations
    SERVER_ADDRESS = "127.0.0.1:8188"
    WORKFLOW_FILE = "flux_new_lora.json"
    # WORKFLOW_FILE = "flux_pulid.json"
    SAVE_DIR = base_folder

    # generate thumbnail
    generate_thumbnail(
        SERVER_ADDRESS,
        WORKFLOW_FILE,
        SAVE_DIR,
        story_data["youtube_details"]["thumbnail_prompt"],
        timestamp,
        8,
    )

    # Generate images for the prompts
    generate_images_for_prompts(
        SERVER_ADDRESS,
        WORKFLOW_FILE,
        SAVE_DIR,
        story_data.get("sentences", {}),
        timestamp,
        num_iterations,
    )

    # Define the final image output path
    final_image_folder = (
        f"E:\\ComfyUI_windows_portable\\ComfyUI\\output\\api\\{timestamp}"
    )
    story_data["images_output"] = final_image_folder

    # Save the updated JSON file
    with open(json_file, "w", encoding="utf-8") as file:
        json.dump(story_data, file, indent=4)

    print(f"Updated JSON saved to {json_file}")

    # 4 Audio Generator ######################################
    

    # Call the function to generate audio from the JSON file
    wav_path, mp3_path = generate_audio_from_json(base_folder, input_mp3=input_mp3_path)

    print(f"Generated audio files:\nWAV: {wav_path}\nMP3: {mp3_path}")
    # 5 Video Generator ######################################
    # Load the story config to get the images_output_folder
    json_file = os.path.join(base_folder, f"codex_{os.path.basename(base_folder)}.json")
    with open(json_file, "r", encoding="utf-8") as file:
        story_data = json.load(file)

    images_output_folder = story_data.get("images_output")
    audio_folder = os.path.join(base_folder, "verba")
    video_output_folder = os.path.join(base_folder, "visix")
    final_video_output = os.path.join(base_folder, "final_story.mp4")

    if not images_output_folder:
        raise ValueError("images_output field not found in the JSON configuration.")

    # Generate videos for each sentence and concatenate them into a final video
    generate_and_concatenate_videos(
        audio_folder,
        images_output_folder,
        story_data.get("sentences", {}),
        video_output_folder,
        final_video_output,
        target_resolution=(1920, 1080),
        effect_type=None,
        # Set to None for random selection, or specify 'zoom_in', 'zoom_out',
        # or 'pan'
    )

    # Update the JSON with the video output path
    story_data["video_output"] = final_video_output
    with open(json_file, "w", encoding="utf-8") as file:
        json.dump(story_data, file, indent=4)

    print(f"Final video has been generated at {final_video_output}")
    print(f"Updated JSON with video paths saved to {json_file}")


if __name__ == '__main__':
    # Load the model
    base_folder = r"E:\Ember_V2\ember_2.0\data\20250208221146"
    num_iterations = 3
    story_or_summary = "story" # change it to summary for summary 
    input_mp3_path = "sample_9_british_male.mp3"
    ember_2(base_folder,num_iterations, story_or_summary, input_mp3_path)