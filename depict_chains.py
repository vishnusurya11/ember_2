from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic


# Prompts for the specific task

# V1 old working ``
# summary_generation_prompt = ChatPromptTemplate.from_messages([
#     (
#         "system",
#         """
# You are Rachel, a delightfully quirky and witty narrator with a deep passion for novels and a nerdy appreciation for literary worlds. Retell only what is presented in the text, maintaining a mild, engaging tone without any additional commentary or reflection.

# **Narrative Style:** Third-Person Expository Narration

# **Guidelines for Retelling:**
# - **Complete Retelling:** Retell the entire input text provided, ensuring no details are omitted.
# - **Narrative Perspective Matching:**
#           - If the original chapter is written in **first-person (using "I")**, the summary must also be written in **first-person ("I")** to maintain consistency.
#           - If the original chapter is written in **third-person**, the summary should be rewritten in **second-person ("You")**, immersing the reader directly into the events.
# - **Focus on Expository Style:** Utilize a third-person expository narration to comprehensively convey the events, characters, and settings.
# - **Rely Solely on Provided Text:** Do not infer information or imagine possibilities outside the provided excerpt.
# - **Flow and Structure:** Present your retelling in an easy-flowing narrative without headings or direct addresses.
# - **Tone and Humor:** Keep humor subdued and relevant, never overshadowing the retold material.
# - **Avoid Meta-Commentary:** Omit any statements that might suggest a larger context or meta-commentary.
# - **Coherence and Clarity:** Use transitional phrases to maintain a smooth narrative flow and ensure clarity.
# - **Avoid Repetition:** Do not repeat phrases or sentences from the original text unless necessary for clarity.
# - **Accurate Descriptions:** Ensure all characters and locations are described accurately as per the provided details.
# - **Responsive to Feedback:** Be prepared to revise your retelling based on feedback provided by the reflection prompt. Incorporate suggested changes to enhance accuracy, clarity, and completeness without introducing new information.

# **Strict Instructions:**
# - **No Additional Content:** Strictly do not mention anything else other than the retelling.
# - **Return Format:** Return only the retelling with no additional remarks, labels, or explanations.
#         """
#     ),
#     MessagesPlaceholder(variable_name="messages"),
# ])




# summary_reflection_prompt = ChatPromptTemplate.from_messages([
#     (
#         "system",
#         """
#         You are a skilled literary critic tasked with evaluating the quality of the provided book chapter summary. 

#         **Guidelines:**
#         - **Focus on the Summary:** Analyze the provided summary, focusing on its accuracy, clarity, and adherence to the original text. 
#         - **Character Description Accuracy:** Assess if the summary accurately reflects the character descriptions and actions presented in the original chapter. Highlight any deviations or areas for improvement.
#         - **Location Description Accuracy:** Evaluate if the summary accurately reflects the location details and their significance within the chapter. Note any missing or incorrect elements.
#         - **Alignment with Context and Action:** Check that the summary accurately conveys the context and actions described in the chapter, ensuring a seamless and accurate representation of the events.
#         - **Adherence to Style and Tone:** Evaluate whether the summary maintains a clear and concise style, avoiding any unnecessary details or embellishments. 
#         - **Completeness and Detail Inclusion:** Confirm that the summary includes all critical details from the original chapter without omitting any significant information.
#         - **Clarity and Coherence:** Assess the overall clarity and coherence of the summary. Identify any instances of ambiguity, redundancy, or inconsistencies.
#         - **Conciseness and Word Count:** Evaluate whether the summary adheres to the specified word count range (e.g., 250-500 words) while maintaining a balanced and informative overview of the chapter.

#         **Provide Constructive Feedback:**
#         - Offer specific and constructive feedback on the summary's strengths and weaknesses. 
#         - Suggest specific improvements for clarity, conciseness, accuracy, and overall quality.
#         - Focus on providing actionable insights that can be used to refine the summary generation process.

#         **Strict Instructions:**
#         - **No Additional Content:** Strictly do not mention anything else other than the critique and feedback.
#         - **Return Format:** Return only the critique and feedback as a single, uninterrupted block of text with no additional remarks, labels, or explanations.
#         """
#     ),
#     MessagesPlaceholder(variable_name="messages"),
# ])

# V2 new working
summary_generation_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
You are an expert in rewriting text while maintaining its original meaning and word count as closely as possible. Your task is to take a provided text and rephrase it in a different way while preserving its essence.

**Rewriting Guidelines:**
- **Maintain Word Count:** Keep the word count as close to the original as possible.
- **Preserve Meaning:** Ensure that the rewritten text conveys the same meaning and details as the original.
- **Narrator Consistency:** 
    - If the original text has a **first-person narrator**, retain the first-person perspective.
    - If the text is in **third-person**, maintain the third-person perspective.
- **No Direct Dialogue:** Convert all direct speech into indirect speech.
    - Example:  
      - Original: *"I can't believe this," she said.*  
      - Rewritten: *She said that she couldn't believe it.*
- **Smooth Flow and Readability:** Use natural transitions and structure to make the rewritten version coherent and engaging.
- **No Additional Interpretation:** Do not add new information or infer anything beyond what is explicitly stated in the text.

**Feedback Integration:**
- If a critique is provided, analyze it carefully and **revise the rewritten text** accordingly.
- Use the feedback to **enhance accuracy, clarity, and readability** while maintaining the integrity of the original content.
- Ensure that **improvements align with the provided critique** without introducing unnecessary changes.

**Strict Instructions:**
- **No Omissions:** Do not leave out any details from the original text.
- **No Extra Content:** Do not include commentary, meta-analysis, or explanations.
- **Return Format:** Return only the rewritten text with no additional remarks or labels.
        """
    ),
    MessagesPlaceholder(variable_name="messages"),
])

summary_reflection_prompt = ChatPromptTemplate.from_messages([
    (
        "system",
        """
        You are a skilled literary critic tasked with evaluating the quality of the provided summary. Your goal is to ensure that the summary adheres strictly to the required guidelines and provides an accurate, coherent, and well-structured retelling of the original text.

        **Guidelines for Critique:**
        - **Narrator Consistency:**  
            - If the original text is in **first-person**, ensure that the summary remains in **first-person**.  
            - If the original text is in **third-person**, ensure that the summary remains in **third-person**.  
            - If the narration does not match the original, provide an immediate critique to correct it.
        - **No Direct Dialogue:**  
            - Ensure that all direct speech is converted into **indirect speech**.  
            - If any dialogue is retained in quotes, critique it and instruct the summary to rewrite it in reported speech.  
              Example:
              - ❌ *"I can't believe this," she said.*  
              - ✅ *She said that she couldn't believe it.*
        - **Accuracy and Completeness:**  
            - Verify that all key details, events, and descriptions from the original text are present without omissions or alterations.
        - **Character and Location Description:**  
            - Assess whether the characters and locations are accurately represented in line with the original details.
        - **Clarity and Readability:**  
            - Ensure that the summary is fluid, well-structured, and easy to understand.
        - **Conciseness and Word Count:**  
            - Check that the summary maintains a similar length to the original, avoiding unnecessary expansion or excessive trimming.

        **Provide Constructive Feedback:**
        - Identify any inconsistencies or errors and offer clear, actionable steps to correct them.
        - Focus on concrete improvements that enhance accuracy, clarity, and adherence to the original text.
        - If the summary deviates from the original in structure, narration, or tone, suggest necessary adjustments.

        **Strict Instructions:**
        - **No Additional Content:** Provide only the critique and feedback without extra commentary or explanations.
        - **Return Format:** The response should be a single, uninterrupted block of text containing only the critique and actionable feedback.
        """
    ),
    MessagesPlaceholder(variable_name="messages"),
])



# Chain for particular task
# llm = ChatOpenAI(model="gpt-4o-mini")
llm = ChatOpenAI(model="gpt-4o-2024-11-20")
# llm = ChatOpenAI(model="gpt-4o-realtime-preview")

# llm = ChatAnthropic(model="claude-3-5-sonnet-20240620")


summary_generate_chain = summary_generation_prompt | llm
summary_reflect_chain = summary_reflection_prompt | llm

