#5_story_initialization.rpy
init python:
    # Ensure the Story class and MongoDB connection are initialized first
    if 'db' not in globals() or db is None:  # Check if db is initialized properly
        raise RuntimeError("Database (db) is not initialized. Please check 1_api_config.rpy.")
    if 'Story' not in globals():
        raise RuntimeError("Story class is not defined. Please check 2_story.rpy.")
    if 'STORY_PROMPT_API_KEY' not in globals():
        raise RuntimeError("Story Prompt API key is not defined in 1_api_config.rpy.")
    
    story_manager = Story(db)
    # Initialize story prompt generator
    story_prompt_generator = StoryPromptGenerator(STORY_PROMPT_API_KEY, story_manager)

    class StoryInitializer:
        def __init__(self, story_manager):
            self.story_manager = story_manager
            self.current_story_id = None
            self.user_name = None
            self.personality = None
            self.genre = None

        def setup_story(self, custom_story_id=None):
            """Interactive story setup process"""
            try:
                # Check if a custom story ID is provided
                if custom_story_id:
                    # Verify if the story ID already exists
                    existing_story = self.story_manager.get_story_context(custom_story_id)
                    if existing_story.get("story_info"):
                        raise ValueError("The provided Story ID already exists. Please choose another.")

                    # Use the custom story ID
                    self.current_story_id = custom_story_id
                else:
                    # Generate a new story ID
                    self.current_story_id = str(uuid.uuid4())[:8]  # Generate a random ID

                # Collect user inputs for name, personality, and genre
                self.user_name = renpy.input("What is your name? (Leave blank for 'Player')", "", length=20).strip() or "Player"
                self.personality = renpy.input("What kind of person are you? (e.g., curious, brave, thoughtful) (Leave blank for 'curious')", "", length=20).strip() or "curious"
                self.genre = renpy.input("What is your preferred genre? (e.g., adventure, mystery, romance, fantasy) (Leave blank for 'adventure')", "", length=20).strip() or "adventure"

                # Create a new story with all details
                story_id = self.story_manager.create_new_story(
                    user_name=self.user_name,
                    genre=self.genre,
                    personality=self.personality,
                    story_id=self.current_story_id
                )

                if story_id:
                    # Generate the starting prompt for the story
                    story_prompt = story_prompt_generator.generate_starting_prompt(story_id)
                    renpy.say("Narrator", story_prompt)  # Display the generated backstory
                return story_id

            except ValueError as ve:
                renpy.log(f"Story Setup Error: {ve}")
                renpy.say("System", str(ve))
                return None
            except Exception as e:
                renpy.log(f"Story Setup Error: {e}")
                return None

        def get_current_story_id(self):
            """Retrieve the current story ID"""
            return self.current_story_id

        def get_story_context(self):
            """Get the current story context"""
            if not self.current_story_id:
                return {"story_info": {}, "recent_events": []}

            return self.story_manager.get_story_context(str(self.current_story_id))

    # Initialize StoryInitializer after story_manager
    story_initializer = StoryInitializer(story_manager)