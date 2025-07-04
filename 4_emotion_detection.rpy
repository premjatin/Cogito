init python:
    from typing import Tuple
    import requests

    class EmotionDeterminationBot:
        def __init__(self, api_key: str, story_db: Story):
            self.api_key = api_key
            self.story_db = story_db
            self.emotions = [
                "normal", "angry", "smile", "sad", "annoyed",
                "shocked", "sleepy", "delighted", "pride", "laugh"
            ]

        def determine_emotion_with_intensity(self, story_id: str, character_name: str, user_input: str) -> Tuple[str, float]:
            context = self.story_db.get_story_context(story_id)
            recent_events = context.get('recent_events', [])
            relevant_context = "\n".join([
                f"{event['speaker_name']}: {event['content']}"
                for event in recent_events[-3:]  # Get last 3 events for context
            ])

            # Get character profile from the centralized profiles
            character_profiles = get_character_profiles()
            character_profile = character_profiles.get(character_name, {})

            system_prompt = f"""You need to determine the emotion and its intensity for {character_name}.

Based on the context:
- The most likely emotion from this list: {', '.join(self.emotions)}
- An intensity score for that emotion (between 0.0 and 1.0).

Respond in this EXACT format: `<emotion>:<intensity_score>`
For example: `angry:0.8` or `sad:0.2`

Character's Profile:
Description: {character_profile.get('description', 'No description provided')}
Speech Style: {character_profile.get('speech_style', 'No speech style provided')}
Personality: {character_profile.get('personality', 'No personality provided')}
Traits: {character_profile.get('traits', 'No traits provided')}

Recent Context:
{relevant_context}

User Input: {user_input}
"""

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
                            {"role": "system", "content": system_prompt}
                        ],
                        "temperature": 0.2
                    }
                )
                llm_response = response.json()['choices'][0]['message']['content'].strip()
                print(f"LLM Response: {llm_response}")  # Debugging line: Print the raw response
                parts = llm_response.split(':')
                if len(parts) == 2:
                    determined_emotion = parts[0].lower()
                    try:
                        intensity_score = float(parts[1])
                        if 0.0 <= intensity_score <= 1.0 and determined_emotion in self.emotions:
                            return determined_emotion, intensity_score
                    except ValueError:
                        print(f"Invalid intensity score received: {parts[1]}. Defaulting to normal with 0.0 intensity.")
                        return "normal", 0.0
                else:
                    print(f"Unexpected format received from LLM: {llm_response}. Defaulting to normal with 0.0 intensity.")
                    return "normal", 0.0
            except Exception as e:
                print(f"Error in emotion determination: {e}")
                return "normal", 0.0

