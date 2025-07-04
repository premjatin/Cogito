#8_speaker_determination.rpy
init python:
    import requests
    from enum import Enum
    from typing import Tuple

    class SpeakerType(Enum):
        NARRATOR = "narrator"
        CHARACTER = "character"

    class SpeakerDeterminationBot:
        def __init__(self, api_key: str, story):
            self.api_key = api_key
            self.story = story

        def determine_speaker(self, story_id: str, user_input: str) -> Tuple[SpeakerType, str]:
            recent_context = self._get_recent_context(story_id)

            # Stage 1: Determine Recipient (Narrator or Character)
            system_prompt_stage1 = f"""Determine the primary intent of the following user input within the context of an interactive story.

                Available characters: {', '.join(get_character_profiles().keys())}

                Recent conversation context:
                {recent_context}

                User's input: {user_input}

                Consider whether the user is primarily intending to:

                - **Engage with a specific character (CHARACTER):** This includes directly speaking to a character, asking them questions, responding to their statements, or expressing thoughts/feelings directed at a character.

                - **Perform an action or describe something in the environment (NARRATOR):** This includes describing the user's actions, observing the surroundings, or expressing general thoughts or states that set the scene.

                Respond with a single word: "CHARACTER" or "NARRATOR".
                """
            response_stage1 = self._call_llm(system_prompt_stage1, user_input, recent_context)

            if "NARRATOR" in response_stage1.upper():
                return SpeakerType.NARRATOR, ""
            elif "CHARACTER" in response_stage1.upper():
                # Stage 2: Determine Specific Character
                system_prompt_stage2 = f"""The user's input is intended for a specific character. Determine which character should respond based on the context.

                Available characters: {', '.join(get_character_profiles().keys())}

                Recent conversation context:
                {recent_context}

                User's input: {user_input}

                Consider the following rules:
                1. **Direct Address:** If the user explicitly named a character at the beginning of their input and is clearly speaking *to* them, that character should respond.
                2. **Recent Interaction:** If the user's input is a direct follow-up (question, statement, reaction) to something a specific character just said or did, that character should respond.
                3. **Contextual Relevance:** Consider which character is most central to the situation, the topic of conversation, or the user's stated intent in the input.
                4. **Pronoun Resolution:** Identify pronouns like "you," "he," or "she" in the user's input and determine which character they refer to based on the context.
                5. **Speaker of Thoughts (Indirect):** If the user is expressing a thought or feeling seemingly directed at someone (even without a direct name), infer the intended recipient based on the content.

                Respond with the name of the single character who should respond.
                """
                response_stage2 = self._call_llm(system_prompt_stage2, user_input, recent_context)
                character_name = response_stage2.strip()
                if self.validate_character(character_name):
                    return SpeakerType.CHARACTER, character_name
                else:
                    print(f"Invalid character determined in Stage 2: {character_name}. Defaulting to narrator.")
                    return SpeakerType.NARRATOR, ""
            else:
                print(f"Unexpected response from Stage 1: {response_stage1}. Defaulting to narrator.")
                return SpeakerType.NARRATOR, ""

        def _get_recent_context(self, story_id):
            context = self.story.get_story_context(story_id)
            return "\n".join([
                f"{event.get('speaker_name', 'Unknown')}: {event.get('content', '')}"
                for event in context.get('recent_events', [])[-5:]
            ])

        def _call_llm(self, system_prompt, user_input, recent_context):
            try:
                response = requests.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "llama-3.1-8b-instant",
                        "messages": [
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_input}
                        ],
                        "temperature": 0.1
                    }
                )
                response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)

                try:
                    return response.json()['choices'][0]['message']['content'].strip()
                except json.JSONDecodeError as e:
                    print(f"JSONDecodeError: {e}")
                    print(f"Raw API response content: {response.content}") # Log the raw content
                    return ""  # Or handle the error as appropriate

            except requests.exceptions.RequestException as e:
                print(f"Error calling LLM API: {e}")
                return ""
        def validate_character(self, character_name: str) -> bool:
            available_characters = list(get_character_profiles().keys())
            return character_name in available_characters