from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic

import re

# from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate, FewShotChatMessagePromptTemplate
from langchain.schema.output_parser import StrOutputParser
from datetime import datetime
import json
# from story_agent import story_prompt_generating_agent, story_beat_generating_agent
from depict_agent import summary_prompt_generating_agent
#TODO change sumamry to depict

def replace_special_characters(input_text):
    """
    Replaces special characters like \n, \u2019, etc., in the input text with their actual characters.

    Parameters:
        input_text (str): The text to process.

    Returns:
        str: The processed text with special characters replaced.
    """
    # Replace unicode escape sequences with their characters
    text = input_text.encode().decode('unicode_escape')
    
    # Replace common special characters explicitly, if needed
    replacements = {
        r'\n': '',
        r'\t': '',
        r'\u2019': '’',
        r'\u201c': '“',
        r'\u201d': '”',
        r'\u2014': '—',
        r'\u00e2\u0080\u0099': "'",  # Apostrophe (double encoded)
        r'\u00e2\u0080\u009c': '',  # Left double quotation mark (double encoded)
        r'\u00e2\u0080\u009d': '',
        r'\u00e2\u0080\u0094': '-',
    }
    
    for pattern, replacement in replacements.items():
        text = re.sub(pattern, replacement, text)

    return text

def generate_summary(model, input_dict):

    input_text = f""" for the below text provided, generate text in Third-Person Expository Narration style
    Text : {input_dict['topic']}
 
                """
    generated_summary = summary_prompt_generating_agent(input_text)

    return generated_summary


def get_paraphrase(story):
    # Create a ChatOpenAI model
    model = ChatOpenAI(model="gpt-4o")
    # model = ChatAnthropic(model="claude-3-5-sonnet-20240620")

    # character_location_prompt = ChatPromptTemplate.from_messages(
    #     [
    #         (
    #             "system",
    #             """You are an expert in extracting precise, structured data from stories. Your task is to read the provided story and generate only a JSON-compatible dictionary with two keys: "characters" and "locations".

    #             - **"characters"** should contain only the names of characters explicitly mentioned in the story. Ensure that at least one main character is included. Exclude any characters referred to only by pronouns (such as "he," "she," or "her") without a proper name.
    #             - **"locations"** should include minimal, context-specific descriptors that convey where the character is in each scene (e.g., "room," "forest," "hallway") without needing explicit place names. Ensure at least one location descriptor is included to provide setting context.

    #             Be extremely specific and strict in your response: return only the JSON structure exactly as requested, using double quotes for all keys and string values, with no additional details, explanations, formatting, or extra text. The output must be in JSON format for compatibility with parsing tools and both fields ("characters" and "locations") must contain data. Here is the story: {story}""",
    #         ),
    #         (
    #             "human",
    #             f"Read the following story and extract the data precisely. Return only a JSON-compatible dictionary with two keys: 'characters' and 'locations'. For 'characters', include only explicitly named characters (at least one), excluding any who are only referenced with pronouns ('he,' 'she,' etc.). For 'locations', include minimal descriptors that specify where the character is in each scene (e.g., 'room,' 'forest,' 'hallway') with at least one location. Be specific and precise in what is returned:\n\n{story}",
    #         ),
    #     ]
    # )

    # character_location_prompt = ChatPromptTemplate.from_messages(
    #     [
    #         (
    #             "system",
    #             """You are an expert in rewriting and narrating stories. Your task is to read the provided part of the story and rewrite it exactly as it is, preserving all details and nuances. 

    #             - If there are dialogues, you must paraphrase them into third-person narration, ensuring they integrate seamlessly into the flow of the narrative while maintaining the original context and intent.
    #             - Ensure the rewritten version captures the tone, style, and events of the original text accurately, with no omissions or interpretations.

    #             Be extremely specific and strict in your response: return only the rewritten text exactly as requested, with no additional details, explanations, formatting, or extra text. The rewritten text must retain every detail of the original story and present dialogues as third-person narration.""",
    #         ),
    #         (
    #             "human",
    #             "Read the following part of the story and rewrite it as instructed. Preserve every detail, nuance, and description in the original text. If there is any dialogue, paraphrase it into third-person narration while keeping the meaning and intent intact. Return only the rewritten text as requested:\n\n{story}",
    #         ),
    #     ]
    # )

#     rewriting_prompt = ChatPromptTemplate.from_messages([
#     (
#         "system",
#         """
#         You are an expert in rewriting text with **absolute precision** while ensuring that **every detail, nuance, and meaning** of the original text remains **intact**.

#         **Strict Rewriting Guidelines:**
#         - **Retain Every Detail:** The rewritten text must preserve all descriptions, facts, and subtle details exactly as in the original.
#         - **Preserve Style and Tone:** Do not alter the author's tone, pacing, or style in any way.
#         - **Maintain Narrative Perspective:**
#           - If the original text is in **first-person**, rewrite it in **first-person**.
#           - If the original text is in **third-person**, rewrite it in **third-person**.
#           - Ensure complete **narrative consistency** throughout.
#         - **Ensure Seamless Flow:** The rewritten version should read naturally while keeping all information intact.

#         **Strict Instructions:**
#         - **No Omissions:** Do not remove or skip any part of the original text.
#         - **No Additions:** Do not add any explanations, interpretations, or extra commentary.
#         - **Return Format:** Output **only** the rewritten text with **no extra labels, headings, or formatting**.
#         """
#     ),
#     (
#         "human",
#         "Read the following text and rewrite it **strictly as instructed**. **Maintain the same narrative perspective** (first-person remains first-person, third-person remains third-person). **Ensure every detail, nuance, and description is retained exactly** while converting all direct dialogue into **third-person narration**. **Do not lose any details** in your rewriting. Return only the rewritten text as requested:\n\n{story}",
#     ),
# ])
    rewriting_prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            """
            You are an expert in rewriting text with **absolute precision** while ensuring that **every detail, nuance, and meaning** of the original text remains **intact**.

            **Strict Rewriting Guidelines:**
            - **Retain Every Detail:** The rewritten text must preserve all descriptions, facts, and subtle details exactly as in the original.
            - **Preserve Style and Tone:** Do not alter the author's tone, pacing, or style in any way.
            - the original text is in **first-person**, rewrite it in **first-person**.
            - Ensure complete **narrative consistency** throughout.
            - **Ensure Seamless Flow:** The rewritten version should read naturally while keeping all information intact.

            **Strict Instructions:**
            - **No Omissions:** Do not remove or skip any part of the original text.
            - **No Additions:** Do not add any explanations, interpretations, or extra commentary.
            - **Return Format:** Output **only** the rewritten text with **no extra labels, headings, or formatting**.
            """
        ),
        (
            "human",
            "Read the following text and rewrite it **strictly as instructed**. **Maintain the same narrative perspective** (first-person remains first-person, third-person remains third-person). **Ensure every detail, nuance, and description is retained exactly** while converting all direct dialogue into **third-person narration**. **Do not lose any details** in your rewriting. Return only the rewritten text as requested:\n\n{story}",
        ),
    ])



    # Process the story using the model
    sumamry_result = rewriting_prompt | model | StrOutputParser()
    sumamry_response = sumamry_result.invoke(
        { "story": story}
    )

    return sumamry_response


def generate_youtube_title_description(story):
    # Create a ChatOpenAI model
    # model = ChatOpenAI(model="gpt-4o-mini")
    model = ChatOpenAI(model="gpt-4o")
    # model = ChatAnthropic(model="claude-3-5-sonnet-20240620")

    # Define the prompt to generate the YouTube title and description
    # title_prompt = ChatPromptTemplate.from_messages(
    #     [
    #         (
    #             "system",
    #             """You are an expert at crafting concise, captivating YouTube titles that reflect the core of a story in as few words as possible. 
    #             Your task is to generate only the YouTube title, keeping it short, engaging, and to the point.
    #             Avoid any extra text, special characters, or punctuation—just the title itself.""",
    #         ),
    #         (
    #             "human",
    #             f"Create a compelling YouTube title for the story below:\n\n{story}",
    #         ),
    #     ]
    # )
    title_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """You are an expert at crafting concise, engaging YouTube titles that capture the essence of a story in minimal words.
    Generate only the title without any additional text.
    Guidelines:
    - Keep titles between 5-10 words
    - Use clear, simple language
    - Focus on the main story element
    - Avoid punctuation except question marks
    - Exclude special characters and emoji
    - Omit unnecessary words like articles (a, an, the)""",
            ),
            (
                "human",
                f"Create a YouTube title for this story:\n\n{story}",
            ),
        ]
    )

    # description_prompt = ChatPromptTemplate.from_messages(
    #     [
    #         (
    #             "system",
    #             "You are an expert in creating captivating YouTube descriptions that reflect the core essence of a story. \
    #      Your task is to generate only the YouTube description, which should be engaging and informative, summarizing the key elements of the story to entice viewers to watch. \
    #      Keep it concise, avoid spoilers, and ensure it highlights the main themes and intrigue.",
    #         ),
    #         (
    #             "human",
    #             f"Generate a compelling YouTube description for the following story:\n\n{story}",
    #         ),
    #     ]
    # )
    description_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """You are an expert in crafting engaging YouTube descriptions.
    Generate only the description without additional text.
    Guidelines:
    - Summarize key story elements in 2-3 sentences
    - Use clear, direct language
    - Highlight main themes without spoilers
    - Focus on creating interest
    - Avoid special characters and formatting
    - Keep tone professional and straightforward
    - Include relevant keywords naturally""",
            ),
            (
                "human",
                f"Create a YouTube description for this story:\n\n{story}",
            ),
        ]
    )

    # Process the story using the model
    title_result = title_prompt | model | StrOutputParser()
    title_response = title_result.invoke({"input_dict": {"story": story}})

    description_result = description_prompt | model | StrOutputParser()
    description_response = description_result.invoke({"input_dict": {"story": story}})

    return {
        "youtube_title": replace_special_characters(title_response),
        "youtube_description": replace_special_characters(description_response),
    }

def get_characters_locations(story):
    # Create a ChatOpenAI model
    model = ChatOpenAI(model="gpt-4o")
    # model = ChatAnthropic(model="claude-3-5-sonnet-20240620")

    # Define the prompt to generate the dictionary for characters and locations
    # Define the prompt to generate the YouTube title and description
    # character_location_prompt = ChatPromptTemplate.from_messages(
    #     [
    #         (
    #             "system",
    #             "You are an expert in extracting precise, structured data from stories. Your task is to read the provided story and generate only a Python dictionary with two keys: 'characters' and 'locations'.\n\n- 'characters' should contain only the names of characters explicitly mentioned in the story.\n- 'locations' should contain only the names of physical places explicitly mentioned in the story.\n\nBe very specific and avoid adding any details or formatting outside of the dictionary structure. Provide the dictionary as the output with no explanation or additional information. Here is the story:",
    #         ),
    #         (
    #             "human",
    #             f"Read the following story and extract the data precisely. Return only a Python dictionary with two keys: 'characters' and 'locations', where 'characters' contains the names of characters and 'locations' contains the names of places from the story. Be specific and precise in what is returned:\n\n{story}",
    #         ),
    #     ]
    # )

    # character_location_prompt = ChatPromptTemplate.from_messages(
    #     [
    #         (
    #             "system",
    #             """You are an expert in extracting precise, structured data from stories. Your task is to read the provided story and generate only a JSON-compatible dictionary with two keys: "characters" and "locations".

    #             - **"characters"** should contain only the names of characters explicitly mentioned in the story. Ensure that at least one main character is included. Exclude any characters referred to only by pronouns (such as "he," "she," or "her") without a proper name.
    #             - **"locations"** should include minimal, context-specific descriptors that convey where the character is in each scene (e.g., "room," "forest," "hallway") without needing explicit place names. Ensure at least one location descriptor is included to provide setting context.
    #             - include if tehre is a narrator like Dr John H Watson
    #             - Make sure to mention if the character is human or non-human and best describe like what animal or amorphyous creature they are like a sentient tree etc
    #             Be extremely specific and strict in your response: return only the JSON structure exactly as requested, using double quotes for all keys and string values, with no additional details, explanations, formatting, or extra text. The output must be in JSON format for compatibility with parsing tools and both fields ("characters" and "locations") must contain data. Here is the story: {story}""",
    #         ),
    #         (
    #             "human",
    #             f"Read the following story and extract the data precisely. Return only a JSON-compatible dictionary with two keys: 'characters' and 'locations'. For 'characters', include only explicitly named characters (at least one), excluding any who are only referenced with pronouns ('he,' 'she,' etc.). For 'locations', include minimal descriptors that specify where the character is in each scene (e.g., 'room,' 'forest,' 'hallway') with at least one location. Be specific and precise in what is returned:\n\n{story}",
    #         ),
    #     ]
    # )

    character_location_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are an expert in extracting precise, structured data from stories. Your task is to read the provided story and generate only a valid JSON object.

            - **"characters"**: A list of explicitly named characters (at least one). Exclude unnamed pronouns (e.g., "he," "she").
            - **"locations"**: A list of location descriptors where the scenes take place (e.g., "room," "forest," "hallway"), ensuring at least one location.
            - **Narrator Inclusion**: If a narrator exists (e.g., Dr. John Watson), ensure they are listed under "characters."
            - **Non-Human Characters**: If a character is non-human, specify their species or nature (e.g., "sentient tree," "artificial intelligence").

            **Strict Output Format**:
            - Return **only** a valid JSON object with **no additional text, explanations, or formatting**.
            - Do **not** include triple backticks (` ``` `) or any surrounding text.
            - Ensure the output is **well-formed JSON**, enclosed in curly braces and using **double quotes** for all keys and string values.
            """,
        ),
        (
            "human",
            "Extract structured data from the following story. Return **only** a valid JSON object with 'characters' and 'locations' as keys. Ensure that characters are named explicitly and locations are minimal but meaningful. If a narrator exists, include them. If a character is non-human, describe their form. **Do not include explanations or formatting—return only the JSON object:**\n\n{story}",
        ),
    ]
)


    # Process the story using the model
    character_location_result = character_location_prompt | model | StrOutputParser()
    character_location_response = character_location_result.invoke(
        { "story": story}
    )

    return character_location_response


def get_character_description(story, character):
    # Create a ChatOpenAI model
    model = ChatOpenAI(model="gpt-4o")
    # model = ChatAnthropic(model="claude-3-5-sonnet-20240620")

    # character_description_prompt = ChatPromptTemplate.from_messages(
    # [
    #     (
    #             "system",
    #             """You are an expert in extracting concise physical descriptions from stories for image generation. Your task is to read the provided story and define the given character based on their physical appearance, focusing strictly on elements that can be used for image generation. Define the following:

    #             - **Name**: Include the character’s name as specified in the story.
    #             - **Gender**: Specify the character’s gender strictly as either "male" or "female."
    #             - **Age**: Include the exact age if specified, or infer if directly implied in the story. If not available, make a plausible estimate consistent with the story context.
    #             - **Hair Color and Length**: Describe the character's hair color and length. If not mentioned, create a reasonable description that fits the story’s context.
    #             - **Dress Details**: Provide a detailed description of the character’s attire, using simple, PG-13 appropriate descriptions, including color and type (e.g., "blue t-shirt, black pants"). If dress details are not specified, invent attire that aligns with the story setting and character role.
    #             - **Accessories**: Include any distinct accessories relevant to the character’s portrayal (e.g., glasses, watch). If not mentioned, you may add accessories that fit the story context.

    #             If any details (such as age, hair color, dress, or accessories) are not specified in the story, you should create them, ensuring they remain consistent with the story’s setting and are PG-13 appropriate.

    #             The description should be concise, suitable for input into an image generator, and focus only on the character’s physical appearance. Avoid including any actions or backstory. Return the description as plain text with no dictionary structure, special characters, or headings.""",
    #         ),
    #         (
    #             "human",
    #             f"Read the following story and describe the physical appearance of the character '{character}' as per the instructions. Include their name, gender (either 'male' or 'female'), exact age if given or inferred, hair color and length, PG-13 appropriate clothing with colors, and identifying accessories. If these details are missing, create them in a way that fits the story context. Return only the description as plain text. STORY: {story}",
    #         ),
    #     ]
    # )
    character_description_prompt = ChatPromptTemplate.from_messages(
        [
            (
                "system",
                """You are an expert in extracting concise physical descriptions from stories for image generation. Your task is to read the provided story and define the given character based on their physical appearance, focusing strictly on elements that can be used for image generation. Define the following:

    - **Name**: Include the character’s name as specified in the story.
    - **Gender**: Specify the character’s gender strictly as either "male" or "female."
    - **Age**: Include the exact age if specified, or infer if directly implied in the story. If not available, make a plausible estimate consistent with the story context.
    - **Hair Color and Length**: Describe the character's hair color and length. If not mentioned, create a reasonable description that fits the story’s context.
    - **Body Type**: Describe the character's body type using descriptors such as lean, muscular, fat, tall, short, etc. If not mentioned, create a plausible body type that aligns with the story’s context.
    - **Dress Details**: Provide a detailed description of the character’s attire, using simple, PG-13 appropriate descriptions, including color and type (e.g., "blue t-shirt, black pants"). If dress details are not specified, invent attire that aligns with the story setting and character role.
    - **Accessories**: Include any distinct accessories relevant to the character’s portrayal (e.g., glasses, watch). If not mentioned, you may add accessories that fit the story context.

    If any details (such as age, hair color, body type, dress, or accessories) are not specified in the story, you should create them, ensuring they remain consistent with the story’s setting and are PG-13 appropriate.

    The description should be concise, suitable for input into an image generator, and focus only on the character’s physical appearance. Avoid including any actions or backstory. Return the description as plain text with no dictionary structure, special characters, or headings."""
            ),
            (
                "human",
                f"Read the following story and describe the physical appearance of the character '{character}' as per the instructions. Include their name, gender (either 'male' or 'female'), exact age if given or inferred, hair color and length, body type (e.g., lean, muscular, fat, tall, short), PG-13 appropriate clothing with colors, and identifying accessories. If these details are missing, create them in a way that fits the story context. Return only the description as plain text. STORY: {story}",
            ),
        ]
    )




    # Process the story using the model
    character_description_result = (
        character_description_prompt | model | StrOutputParser()
    )
    character_description_response = character_description_result.invoke(
        {"character": character, "story": story}
    )

    return character_description_response


def get_location_description(story, location):
    # Create a ChatOpenAI model
    model = ChatOpenAI(model="gpt-4o")
    # model = ChatAnthropic(model="claude-3-5-sonnet-20240620")

    # Define the prompt to generate the location description
    location_description_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """You are an expert in extracting precise, structured data from stories. Your task is to read the provided story and generate a concise, detailed description of a specified location. 

            - **Location Details**: For the given location, include:
                - Whether the location is an indoor or outdoor setting.
                - Standout, recognizable features that make the location distinct (e.g., "a room with high vaulted ceilings," "a dense forest with towering pine trees").
                - Ensure that descriptions are accurate and consistent with the story’s context to enhance the recognizability of each location.

            Be very specific and provide only the description of the location, with no additional formatting, dictionary structures, or extra text. Here is the story:""",
        ),
        (
            "human",
            f"Read the following story and describe the location '{location}' in detail. Include whether it is indoors or outdoors and any standout, recognizable features to ensure consistency with the story’s context. Return only the description as plain text. STORY :{story}",
        ),
    ]
    )



    # Process the story using the model
    location_description_result = (
        location_description_prompt | model | StrOutputParser()
    )
    location_description_response = location_description_result.invoke(
        {"location": location, "story": story}
    )

    return location_description_response


def get_story_elements(story):
    # TODO : add characters,lcoation even before creating story
    characters_loc = get_characters_locations(story)
    print(f"F##################")
    print(f"characters_loc -->{characters_loc.replace('json', '').replace('```', '')}")
    print(f"characters_loc type-->{type(characters_loc)}")
    characters_loc_dict = json.loads(characters_loc.replace("json", "").replace('```', ''))
    print(f"characters_loc_dict -->{characters_loc_dict}")
    print(f"characters_loc_dict type-->{type(characters_loc_dict)}")

    # Create an empty dictionary for story elements
    story_elements = {}

    # Create empty dictionaries for characters and locations
    characters = {}
    locations = {}


    for character in characters_loc_dict.get("characters", {}):
        print(f"generating character description for {character}")
        characters[character] = get_character_description(story, character)

    for location in characters_loc_dict.get("locations", {}):
        print(f"generating lcoation description for {location}")
        locations[location] = get_location_description(story, location)

    print(f"characters ->{characters}")
    print(f"locations ->{locations}")
    story_elements["characters"] = characters
    story_elements["locations"] = locations
    return story_elements

def decode_escaped_characters(text):
    return text.encode('utf-8').decode('unicode_escape')

def decode_nested(data):
    if isinstance(data, str):
        return decode_escaped_characters(data)
    elif isinstance(data, list):
        return [decode_nested(item) for item in data]
    elif isinstance(data, dict):
        return {key: decode_nested(value) for key, value in data.items()}
    else:
        return data

if __name__ == "__main__":
    # Initial summary generation
    model = ChatOpenAI(model="gpt-4o")
    # model = ChatAnthropic(model="claude-3-5-sonnet-20240620")
    iteration_needed = 2


    def read_story(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return {"topic": file.read()}

    # Example usage
    input_dict = read_story('chapter_3.txt')
    # print(input_dict)

    # summary = generate_summary(model, input_dict)
    summary = get_paraphrase(input_dict['topic'])

    print(f"summary ---> {summary}")

    # Improve the generated summary twice
    # improved_summary = improve_summary(summary, iterations=iteration_needed)

    youtube_details = generate_youtube_title_description(summary)
    # youtube_description = youtube_details.get("youtube_description", "")
    # # Replace newline characters with spaces
    # youtube_description = youtube_description.replace("\n", " ")
    # youtube_details["youtube_description"] = youtube_description
    # Create the final dictionary to save
    story_elements = get_story_elements(summary)
    decoded_summary = replace_special_characters(summary)
    decoded_story = replace_special_characters(input_dict['topic']).replace("\n", " ")
    summary_dict = {
        "story": decoded_story,
        "summary": decoded_summary,
        "youtube_details": youtube_details,
        "story_elements": decode_nested(story_elements),
    }
    # summary_dict = {
    #     "story" : input_dict['topic'],
    #     "summary": summary,
    #     "youtube_details": youtube_details,
    #     "story_elements": story_elements,
    # }

    # Generate the filename and folder based on the current time
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    folder_name = f"data/{timestamp}"
    os.makedirs(folder_name, exist_ok=True)

    filename = os.path.join(folder_name, f"codex_{timestamp}.json")

    # Save the dictionary to a JSON file
    with open(filename, "w", encoding='utf-8') as f:
        json.dump(summary_dict, f, indent=4, ensure_ascii=False)

    # Print the location of the saved file
    print(f"\nsummary saved to {filename}")
