# 1_api_config.rpy
init python:
    import pymongo
    NARRATOR_API_KEY = "GROQ_API_KEY"
    CHARACTER_API_KEY = "GROQ_API_KEY"
    SPEAKER_API_KEY = "GROQ_API_KEY"
    STORY_PROMPT_API_KEY = "GROQ_API_KEY"
    EMOTION_API_KEY = "GROQ_API_KEY"
    BACKGROUND_API_KEY = "GROQ_API_KEY"
    # MongoDB Configuration
    MONGODB_URI = "mongodb://localhost:27017/"
    DATABASE_NAME = "interactive_story_db"

    def init_mongodb():
        """
        Initialize MongoDB connection.
        """
        try:
            client = pymongo.MongoClient(MONGODB_URI)
            db = client[DATABASE_NAME]
            print("MongoDB connection successful.")  # Debugging line
            return client, db
        except Exception as e:
            print(f"MongoDB Connection Error: {e}")  # Print the error
            return None, None

    # Initialize MongoDB connection
    client, db = init_mongodb()
    