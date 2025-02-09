import os
import json
import random
from tqdm import tqdm
import time
from generator import ImageGenerator


def extract_timestamp_from_path(path):
    # Extracts the timestamp from the base folder path
    return os.path.basename(path)


def generate_images_for_prompts(
    server_address, workflow_file, save_dir, sentences, timestamp, num_iterations=3
):
    generator = ImageGenerator(server_address, workflow_file)

    # images_folder = os.path.join(save_dir, "images")
    # os.makedirs(images_folder, exist_ok=True)

    for key, value in tqdm(sentences.items(), desc="Generating Images for Sentences"):
        # prompt = value.get("prompt", "").strip()
        prompt = value.get("prompt_agent", "").strip()
        if not prompt:
            continue  # Skip if the prompt is empty

        for i in range(num_iterations):
            # time.sleep(5)  # Add a sleep delay between iterations
            seed = random.randint(100000000000000, 9999999999999999)

            api_prefix = f"api/{timestamp}/{key}/{i+1:02}"

            updates = {
                "6": {
                    "text": prompt,
                },
                "25": {
                    "noise_seed": seed,
                },
                "41": {
                    "filename_prefix": f"{api_prefix}_hires/",
                },
                "9": {
                    "filename_prefix": f"{api_prefix}_facefix/",
                },
                "38": {
                    "lora_name": "flux\\flux_realisim_hf.safetensors",
                },
            }


            generator.generate_images(save_dir, updates=updates)

    return sentences


def generate_thumbnail(
    server_address,
    workflow_file,
    save_dir,
    thumbnail_prompt,
    timestamp,
    num_iterations=3,
):
    generator = ImageGenerator(server_address, workflow_file)

    # images_folder = os.path.join(save_dir, "images")
    # os.makedirs(images_folder, exist_ok=True)

    print(f"thumbnail_prompt -> {thumbnail_prompt}")
    for i in range(num_iterations):
        # time.sleep(5)  # Add a sleep delay between iterations
        seed = random.randint(100000000000000, 9999999999999999)

        api_prefix = f"api/{timestamp}/thumbnail/{i+1:02}"

        updates = {
            "6": {
                "text": thumbnail_prompt,
            },
            "25": {
                "noise_seed": seed,
            },
            "41": {
                "filename_prefix": f"{api_prefix}_hires/",
            },
            "9": {
                "filename_prefix": f"{api_prefix}_facefix/",
            },
            "38": {
                "lora_name": "flux\\flux_realisim_hf.safetensors",
            },
        }


        generator.generate_images(save_dir, updates=updates)

    return True


if __name__ == "__main__":
    # High-level path provided
    base_folder = r"E:\Ember_V2\ember_2.0\data\20250208221146"
    num_iterations = 2
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
        num_iterations,
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
