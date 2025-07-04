# 9_script.rpy
init python:
    import uuid
    import re
    show_emotion = ""
    story_choice = ""
    story_id = ""
    user_name = ""  # Will be set dynamically
    user_personality = ""  # Will be set dynamically
    selected_genre = ""  # Will be set dynamically
    input_value = ""
    previous_speaker = ""
    sprite_name = ""
    current_background = "default"
    previous_background = ""
    previous_characters = []

# The start label
label start:
    scene black
    with fade

    menu:
        "Would you like to start a new story or continue an existing one?"
        
        "Start New Story":
            $ story_choice = "new"
            jump new_story_setup
        
        "Continue Existing Story":
            $ story_choice = "continue"
            jump continue_story_setup

label continue_story_setup:
    python:
        story_id = renpy.input("Please enter your Story ID:", "", length=20)
        try:
            story = Story(db)
            context = story.get_story_context(story_id)
            if not context["story_info"]:
                renpy.say("System", "Story ID not found. Starting a new story instead.")
                story_choice = "new"
                renpy.jump("new_story_setup")
        except Exception as e:
            renpy.say("System", f"Error loading story: {e}")
            renpy.jump("new_story_setup")
    
    jump story_loop

label new_story_setup:
    # Ask if the user wants to provide a custom Story ID
    menu:
        "Would you like to provide your own Story ID?"        
        "Yes":
            $ custom_story_id = renpy.input("Enter your custom Story ID:", "", length=20)
        "No":
            $ custom_story_id = None

    python:
        try:
            # Initialize the StoryInitializer and set up the story
            story_initializer = StoryInitializer(story_manager)
            story_id = story_initializer.setup_story(custom_story_id)
            if not story_id:
                raise Exception("Failed to create a new story.")
        except Exception as e:
            renpy.say("System", f"Error creating a story: {e}")

    "Your Story ID is [story_id]. Please save this ID to continue your story later."

    jump story_loop

label story_loop:
    python:
        user_input = renpy.input("What would you like to do? (Type 'exit' to quit)", "", length=200)
        
        if user_input.lower() == "exit":
            renpy.say("", f"Story paused. Your story ID is {story_id}. You can continue this story later using this ID.")
            renpy.full_restart()
        
        try:
            # Initialize story and get context
            story = Story(db)
            story_context = story.get_story_context(story_id)
            background_detector = BackgroundDetector(BACKGROUND_API_KEY, story_manager)
            
            # Ensure story_id is in the context
            if 'story_id' not in story_context.get('story_info', {}):
                story_context['story_info']['story_id'] = story_id

            # Store the user input in the events collection
            story.add_event(
                story_id,
                SpeakerType.CHARACTER,  # Treat user input as coming from a "character"
                "User",  # Explicitly set the speaker name to "User"
                user_input
            )
            
            # Determine speaker
            speaker_bot = SpeakerDeterminationBot(SPEAKER_API_KEY, story)
            speaker_type, speaking_character = speaker_bot.determine_speaker(story_id, user_input)
            emotion_determination_bot = EmotionDeterminationBot(EMOTION_API_KEY, story)
            
            if speaker_type == SpeakerType.NARRATOR:
                narrator_bot = NarratorBot(NARRATOR_API_KEY, story)
                response = narrator_bot.generate_response(user_input, story_context)
                available_characters = list(story.get_all_character_profiles().keys())
                mentioned_characters = narrator_bot.get_mentioned_characters(response, available_characters)
                
                # Hide previous background and characters
                if previous_background:
                    renpy.hide(previous_background)
                for character in previous_characters:
                    renpy.hide(character)
                
                # Detect and show the new background
                current_background = background_detector.detect_background(story_id, response)
                renpy.scene()  # Clear the current scene
                renpy.show(current_background)  # Show the detected background

                # Show mentioned characters in the background
                max_characters = 4  # Maximum number of characters to show
                shown_characters = []
                for i, character in enumerate(mentioned_characters[:max_characters]):
                    # Calculate the position based on the index
                    xposition = 0.25 + i * 0.25
                    renpy.show(character.lower(), at_list=[Transform(align=(xposition, 1.0), alpha=0.9, zoom=0.7)])  # Adjust positioning, alpha, and zoom as needed
                    shown_characters.append(character.lower())

                previous_background = current_background
                previous_characters = shown_characters

                # Add event to the database
                story.add_event(
                    story_id, 
                    SpeakerType.NARRATOR, 
                    "Narrator", 
                    response
                )
                
                renpy.say("Narrator", response)
            else:
                # Hide previous characters mentioned by the narrator
                for character in previous_characters:
                    renpy.hide(character)

                # Determine the emotion and intensity
                dominant_emotion, intensity_score = emotion_determination_bot.determine_emotion_with_intensity(story_id, speaking_character, user_input)
                renpy.notify(f"Emotion: {dominant_emotion}, Intensity: {intensity_score}") # Add this line
                character_bot = CharacterBot(CHARACTER_API_KEY, story)
                response = character_bot.get_response(story_id, user_input, speaking_character, {dominant_emotion: intensity_score}) # Pass emotion and intensity

                # Add event to the database
                story.add_event(
                    story_id,
                    SpeakerType.CHARACTER,
                    speaking_character,
                    response
                )

                # Show the character sprite based on the determined emotion and intensity
                if previous_speaker:
                    renpy.hide(previous_speaker)

                if intensity_score >= 0.3:  # Example threshold, adjust as needed
                    sprite_name = speaking_character.lower() + "/" + dominant_emotion
                    renpy.show(sprite_name)
                else:
                    sprite_name = speaking_character.lower() + "/normal" # Show normal sprite if intensity is low
                    renpy.notify(f"Emotion: {dominant_emotion}, Intensity: {intensity_score}") # Display with notify
                    renpy.show(sprite_name)

                # Display the character's response
                renpy.say(speaking_character, response)

                # Store the current sprite name as the previous speaker
                previous_speaker = sprite_name

        except Exception as e:
            renpy.say("System", f"An error occurred: {e}")

    jump story_loop
