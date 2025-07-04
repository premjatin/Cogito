# In 6_character_bot.rpy
init python:
    import requests
    class CharacterBot:
        def __init__(self, api_key: str, story):
            self.api_key = api_key
            self.story = story

        def get_response(self, story_id: str, user_input: str, speaking_character: str, emotion_scores: Dict[str, float]) -> str:
            try:
                # Gather necessary context
                context = self.story.get_story_context(story_id)
                character_memories = self.story.get_character_memory(story_id, speaking_character)
                story_info = context.get('story_info', {})
                recent_events = context.get('recent_events', [])

                # Get character profile from the centralized profiles
                character_profiles = get_character_profiles()
                character_profile = character_profiles.get(speaking_character, {})

                recent_context = "\n".join([
                    f"{event.get('speaker_name', 'Unknown')}: {event.get('content', '')}"
                    for event in recent_events[-5:]
                ])

                # Extract the dominant emotion and its intensity
                dominant_emotion = next(iter(emotion_scores))
                intensity = emotion_scores.get(dominant_emotion, 0.0)

                # Define the system prompt for the character
                system_prompt = f"""You are {speaking_character}. Your characteristics:
        Description: {character_profile.get('description')}
        Speech Style: {character_profile.get('speech_style')}
        Personality: {character_profile.get('personality')}
        Traits: {character_profile.get('traits')}
        Recent conversation context:
        {recent_context}

        Your memories:
        {' '.join(character_memories)}

        You are currently feeling **{dominant_emotion}** with an intensity of **{intensity:.2f}**.

        As {speaking_character}, respond naturally to the user's last statement or action, reflecting your current emotional state and its intensity.
            - Speak in first person, using your character's unique voice and personality
            - Respond directly to what was just said or done
            - Stay focused on the situation
            - Keep responses natural and conversational
            - Reflect the given emotion and its intensity appropriately. For example, if you are slightly annoyed, your response should reflect mild annoyance, not extreme anger.

        Respond only with dialogue, staying true to your character's personality and speech style."""

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
                            {"role": "system", "content": system_prompt}
                        ],
                        "temperature": 0.7
                    }
                )

                character_response = response.json()['choices'][0]['message']['content'].strip()

                # Update character's memories
                self.story.update_character_memory(
                    story_id,
                    speaking_character,
                    f"User: {user_input}\nResponse (Emotion: {dominant_emotion}, Intensity: {intensity:.2f}): {character_response}"
                )

                return character_response

            except Exception as e:
                return f"An error occurred: {str(e)}"
