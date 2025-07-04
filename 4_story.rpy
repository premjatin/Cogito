# 4_story.rpy
init python:
    from typing import Dict, List, Optional
    from datetime import datetime
    from enum import Enum
    import uuid

    class SpeakerType(Enum):
        NARRATOR = "narrator"
        CHARACTER = "character"
    
    class Story:
        def __init__(self, db):
            # Initialize collections
            self.stories = db['stories']
            self.events = db['events']
            self.character_memories = db['character_memories']
            self.character_profiles = db['character_profiles']
            
            # Create indexes
            self.stories.create_index('story_id')
            self.events.create_index([('story_id', 1), ('timestamp', 1)])
            self.character_memories.create_index([('story_id', 1), ('character_name', 1)])
            
            # Initialize character profiles if they don't exist
            self._initialize_character_profiles()

        def _initialize_character_profiles(self):
            # Your existing character profiles initialization logic
            default_profiles = {
                'Emma': {
                    'description': 'Emma is a perceptive and insightful character, often understanding the unspoken feelings of others.',
                    'speech_style': 'Thoughtful and caring, she often tries to reassure others.',
                    'personality': 'Empathetic and observant, but can be hesitant to confront directly.'
                },
                'Max': {
                    'description': 'Max is straightforward and direct, often probing deeper into conversations.',
                    'speech_style': 'Confident and assertive, he challenges others.',
                    'personality': 'Bold and protective, but can be impulsive.'
                },
                'Liam': {
                    'description': 'Liam is a curious and adventurous young man, always eager to explore new horizons.',
                    'speech_style': 'Energetic and inquisitive, he asks many questions.',
                    'personality': 'Brave and curious, but can be reckless at times.'
                },
                'Olivia': {
                    'description': 'Olivia is a kind and compassionate soul, often offering a listening ear to those in need.',
                    'speech_style': 'Gentle and nurturing, she speaks with a soothing tone.',
                    'personality': 'Empathetic and patient, but can be timid in confrontational situations.'
                },
                'Noah': {
                    'description': 'Noah is a logical and analytical thinker, always seeking to understand the world around him.',
                    'speech_style': 'Measured and precise, he articulates his thoughts carefully.',
                    'personality': 'Intelligent and rational, but can be aloof and detached at times.'
                },
                'Isabella': {
                    'description': 'Isabella is a creative and imaginative individual, often seen with a sketchpad in hand.',
                    'speech_style': 'Expressive and eloquent, she has a flair for storytelling.',
                    'personality': 'Artistic and whimsical, but can be easily distracted.'
                },
                'Ethan': {
                    'description': 'Ethan is a skilled outdoorsman, comfortable in the wilderness and adept at survival.',
                    'speech_style': 'Concise and practical, he speaks with a no-nonsense tone.',
                    'personality': 'Rugged and self-reliant, but can be gruff and unsociable.'
                },
                'Sophia': {
                    'description': 'Sophia is a diplomatic and level-headed individual, often acting as a peacekeeper.',
                    'speech_style': 'Thoughtful and measured, she chooses her words carefully.',
                    'personality': 'Rational and composed, but can be overly cautious at times.'
                },
                'Lucas': {
                    'description': 'Lucas is a charming and charismatic person, able to easily win over those around him.',
                    'speech_style': 'Smooth and persuasive, he has a way with words.',
                    'personality': 'Confident and sociable, but can be manipulative and self-serving.'
                },
                'Ava': {
                    'description': 'Ava is a passionate and determined individual, driven to achieve her goals.',
                    'speech_style': 'Passionate and resolute, her words carry weight and conviction.',
                    'personality': 'Ambitious and resilient, but can be stubborn and headstrong.'
                }
            }
        
            # Insert profiles if they don't exist
            existing = self.character_profiles.find_one({'_id': '672dd013ca34be5931e84195'})
            if not existing:
                self.character_profiles.insert_one({
                    '_id': '672dd013ca34be5931e84195',
                    'characters': default_profiles
                })

        def create_new_story(self, user_name: str, genre: str, personality: str, story_id: Optional[str] = None) -> str:
            """
            Create a new story with detailed metadata. Requires personality to be explicitly provided.
            """
            try:
                # Use the provided story ID or generate a random one
                if not story_id:
                    story_id = str(uuid.uuid4())[:8]

                # Create story document
                story_doc = {
                    'story_id': story_id,
                    'user_name': user_name,
                    'genre': genre,
                    'current_background': 'default',
                    'user_personality': personality,  # Explicitly save personality
                    'created_at': datetime.now(),
                    'status': 'active'
                }

                # Check for duplicate story ID
                if self.stories.find_one({'story_id': story_id}):
                    raise ValueError(f"A story with ID '{story_id}' already exists.")

                # Insert the story
                self.stories.insert_one(story_doc)
                return story_id
            except Exception as e:
                print(f"Error creating new story: {e}")
                return None

        def add_event(self, story_id: str, speaker_type: SpeakerType, speaker_name: str, content: str) -> bool:
            try:
                event = {
                    'story_id': story_id,
                    'timestamp': datetime.now(),
                    'speaker_type': speaker_type.value,
                    'speaker_name': speaker_name,
                    'content': content
                }
                self.events.insert_one(event)
                return True
            except Exception as e:
                print(f"Error adding event: {e}")
                return False

        def get_story_context(self, story_id: str, limit: int = 10) -> Dict:
            try:
                story = self.stories.find_one({'story_id': story_id})
                recent_events = list(self.events.find(
                    {'story_id': story_id},
                    {'_id': 0}
                ).sort('timestamp', -1).limit(limit))
                
                return {
                    'story_info': story,
                    'recent_events': recent_events[::-1]  # Reverse to get chronological order
                }
            except Exception as e:
                print(f"Error getting story context: {e}")
                return {}

        def update_character_memory(self, story_id: str, character_name: str, memory: str):
            try:
                self.character_memories.update_one(
                    {'story_id': story_id, 'character_name': character_name},
                    {'$push': {'memories': {
                        'content': memory,
                        'timestamp': datetime.now()
                    }}},
                    upsert=True
                )
            except Exception as e:
                print(f"Error updating character memory: {e}")

        def get_character_memory(self, story_id: str, character_name: str, limit: int = 5) -> List[str]:
            try:
                memory_doc = self.character_memories.find_one(
                    {'story_id': story_id, 'character_name': character_name}
                )
                if memory_doc and 'memories' in memory_doc:
                    return [m['content'] for m in memory_doc['memories'][-limit:]]
                return []
            except Exception as e:
                print(f"Error getting character memory: {e}")
                return []

        def get_all_character_profiles(self) -> Dict:
            try:
                doc = self.character_profiles.find_one({'_id': '672dd013ca34be5931e84195'})
                if doc and 'characters' in doc:
                    return doc['characters']
                return {}
            except Exception as e:
                print(f"Error getting character profiles: {e}")
                return {}

        def remove_last_event(self, story_id: str) -> bool:
            """
            Remove the most recent event for a given story
            """
            try:
                # Find the most recent event
                most_recent_event = self.events.find_one(
                    {'story_id': story_id},
                    sort=[('timestamp', -1)]
                )
                
                if most_recent_event:
                    # Delete the specific event
                    result = self.events.delete_one({'_id': most_recent_event['_id']})
                    return result.deleted_count > 0
                
                return False
            except Exception as e:
                print(f"Error removing last event: {e}")
                return False

        def update_background(self, story_id: str, background: str):
            try:
                self.stories.update_one(
                    {'story_id': story_id},
                    {'$set': {'current_background': background}}
                )
            except Exception as e:
                print(f"Error updating background: {e}")
        
        def get_current_background(self, story_id: str) -> str:
            # Retrieve the current background for the story
            story_collection = self.db["stories"]
            story = story_collection.find_one({"story_id": story_id})
            if story:
                return story.get("current_background", "default")
            return "default"