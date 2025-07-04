#7_narrator.rpy
init python:
    import requests
    import re
    
    class NarratorBot:
        def __init__(self, api_key: str, story):
            self.api_key = api_key
            self.story = story

        def generate_response(self, user_input: str, context: dict) -> str:
            try:
                # Gather necessary context
                story_info = context.get('story_info', {})
                recent_events = context.get('recent_events', [])
                available_characters = list(get_character_profiles().keys())

                # Combine recent events into a single contextual string
                full_context = "\n".join([
                    f"{event.get('speaker_name', 'Unknown')}: {event.get('content', '')}"
                    for event in recent_events
                ])

                # Define the system prompt for the narrator
                system_prompt = f"""You are a playful and quirky narrator guiding players through an interactive story.
    Act as a voice in the player's head. Your style is engaging and lively, often reflecting the player's emotions and decisions.
    Use brief descriptions that evoke imagery without overwhelming the player.
    Occasionally, incorporate humor and light-hearted commentary to enhance the experience.

    Available characters that can be mentioned in the story:
    {', '.join(available_characters)}

    Important rules:
    - Only mention characters from the available characters list
    - Never create or mention characters that aren't in the list
    - Keep the story flowing naturally without giving explicit choices
    - Maintain consistency with previous events
    - If multiple characters are present, highlight the most prominent character in each paragraph

    User's name: {story_info.get('user_name')}
    User's personality: {story_info.get('user_personality')}
    Genre: {story_info.get('genre',)}

    Full story context:
    {full_context}

    User's action: {user_input}"""

                # Make API call and get response
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
                        "temperature": 0.7
                    }
                )

                narrator_response = response.json()['choices'][0]['message']['content'].strip()
                
                # Update narrator's memory (using character memory method)
                self.story.update_character_memory(
                    context.get('story_info', {}).get('story_id', ''),
                    "Narrator", 
                    f"User: {user_input}\nResponse: {narrator_response}"
                )

                return narrator_response

            except Exception as e:
                return f"An error occurred: {str(e)}"

        def get_mentioned_characters(self, narrator_response: str, available_characters: List[str]) -> List[str]:
            """
            Extract mentioned characters from the narrator's response.
            """
            mentioned_characters = re.findall(r'\b(?:' + '|'.join(available_characters) + r')\b', narrator_response)
            return mentioned_characters