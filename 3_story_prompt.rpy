# 3_story_prompt.rpy
init python:
    import requests

    class StoryPromptGenerator:
        def __init__(self, api_key: str, story):
            self.api_key = api_key
            self.story = story  # Reference to the Story database

        def generate_starting_prompt(self, story_id: str) -> str:
            """
            Generate a starting prompt based on the user's name, personality, and genre.
            """
            try:
                # Retrieve story context
                context = self.story.get_story_context(story_id)
                story_info = context.get('story_info', {})
                available_characters = list(self.story.get_all_character_profiles().keys())
                
                # Get character profiles
                character_profiles = get_character_profiles()

                # System prompt to guide the LLM
                system_prompt = f"""You are a storyteller bot that creates engaging personal scenarios. When generating a story prompt based on the user's name, preferred story type, and available characters, create:
                User's name: {story_info.get('user_name')}
                User's personality: {story_info.get('user_personality')}
                Genre: {story_info.get('genre')}
                
                A vivid personal context (2-3 sentences) that places the user as a central character with clear emotional stakes
                
                A brief but rich explanation of the situation and relationships (2-3 sentences)
                Mention the characters and their detailed profiles:
                {', '.join([f"{char}: {profile.get('description', 'No description')}" for char, profile in character_profiles.items()])}
                
                An open scenario that hints at possibilities (1-2 sentences)
                
                Combine these elements into a single, flowing paragraph that reads naturally and emotionally engages the reader.
                
                Characters to include subtly:
                {', '.join(available_characters)}
                
                ."""

                # Call the LLM API
                response = requests.post(
                    "https://api.groq.com/openai/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "llama-3.1-8b-instant",
                        "messages": [
                            {"role": "system", "content": system_prompt}
                        ],
                        "temperature": 0.7
                    }
                )

                # Extract the generated prompt
                prompt = response.json()['choices'][0]['message']['content'].strip()

                # Store the starting prompt in the events collection as a narrator event
                self.story.add_event(
                    story_id=story_id,
                    speaker_type=SpeakerType.NARRATOR,  # Narrator event
                    speaker_name="Narrator",
                    content=prompt
                )

                return prompt

            except Exception as e:
                print(f"Error generating starting prompt: {e}")
                return "An error occurred while generating the story introduction. Please try again later."
