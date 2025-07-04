# AI-Powered Interactive Story Engine in Ren'Py

![Ren'Py](https://img.shields.io/badge/Ren'Py-8.1.3-ffde5d.svg)
![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)
![MongoDB](https://img.shields.io/badge/MongoDB-Required-green.svg)
![Groq API](https://img.shields.io/badge/API-Groq-lightgrey.svg)

This project is an advanced interactive storytelling engine built with the Ren'Py visual novel engine. Unlike traditional visual novels with pre-written scripts, this game generates its narrative, character responses, and environmental details dynamically using Large Language Models (LLMs) via the Groq API. The entire story state, including events and character memories, is persistently stored in a MongoDB database, allowing for complex, evolving narratives and the ability to continue stories later.

## Core Features

-   **Dynamic Narrative Generation**: The story is not pre-scripted. The narrator's descriptions are generated in real-time based on the player's actions and the current context.
-   **LLM-Powered Characters**: Every non-player character (NPC) is an independent AI agent. Their dialogue is generated based on their unique personality profile, memories, recent conversation, and a dynamically determined emotional state.
-   **Context-Aware Emotion System**: The engine analyzes the context and player input to determine a character's emotion and its intensity (e.g., `angry: 0.8`). This directly influences their dialogue and the on-screen character sprite.
-   **Intelligent Speaker Determination**: A sophisticated two-stage LLM process determines if the player is interacting with a character or the environment. If it's a character, it infers *which* character should respond, even without a direct mention.
-   **Dynamic Background System**: The game's background visuals change automatically. The engine analyzes the narrator's text to select the most appropriate background image from a vast library.
-   **Persistent Story State**: Leverages MongoDB to save every event, conversation, and character memory. This allows players to pause their unique story and resume it at any time using a Story ID.

## How It Works: The Game Loop

The engine's main loop is a cycle of AI-driven decision-making:

1.  **Player Input**: The player enters an action or dialogue.
   ![game1](https://github.com/user-attachments/assets/da137431-f7c2-4fca-8fd9-3fa80f221d44)

3.  **Speaker Determination**: An LLM decides if the input is for the **Narrator** (an action, observation) or a **Character** (dialogue).
    -   If for a **Character**, a second LLM call identifies the specific character being addressed.
      ![emma](https://github.com/user-attachments/assets/b1e296fb-fede-4ab7-a638-cf7dec1ddf17)

4.  **Response Generation**:
    -   **Narrator Bot**: If the input was an action, the Narrator Bot generates a description of the outcome, potentially mentioning characters present in the scene. A `BackgroundDetector` then analyzes this text to set the scene's visual background.
      ![cafe](https://github.com/user-attachments/assets/deb7a439-5a9e-4b5d-81ae-6e500fc550be)

    -   **Character Bot**: If the input was for a character, an `EmotionDeterminationBot` first calculates the character's emotional response. Then, the `CharacterBot` uses this emotion, along with the character's personality and memories, to generate a unique line of dialogue.
5.  **Display Output**: The game displays the generated text, character sprites (with the correct emotion), and background on the screen.
   ![emma sad](https://github.com/user-attachments/assets/5e87e49c-05b0-4977-aeb7-b613a413f72d)

7.  **Database Logging**: The entire interaction (player input and AI response) is saved as an "event" in the MongoDB database for future context.
8.  The loop repeats.

## Setup and Installation

To run this project, you need to set up the dependencies and configure API keys.

### 1. Prerequisites
-   [Ren'Py SDK](https://www.renpy.org/latest.html) (Version 8.1 or newer recommended)
-   [Python](https://www.python.org/downloads/) (usually bundled with Ren'Py)
-   A running [MongoDB](https://www.mongodb.com/try/download/community) instance (can be local or on a cloud service).
-   A [Groq API Key](https://console.groq.com/keys).

### 2. Installation Steps

1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/YourUsername/your-repo-name.git
    cd your-repo-name
    ```

2.  **Install Python Libraries**:
    This project requires `requests` for API calls and `pymongo` for the database connection. Open a terminal and run:
    ```bash
    pip install requests pymongo
    ```

3.  **Configure API Keys and Database (Crucial!)**

    For security, **do not hardcode your API keys in the files**. We will modify `1_api_config.rpy` to use environment variables.

    a. Create a file named `.env` in the root directory of the project.
    
    b. Add your keys and database URI to the `.env` file like this:
    ```
    GROQ_API_KEY="your-actual-groq-api-key-here"
    MONGODB_URI="mongodb://localhost:27017/"
    DATABASE_NAME="interactive_story_db"
    ```

4.  **Launch the Game**:
    -   Open the Ren'Py Launcher.
    -   Select "Add Existing Project" and choose this project's folder.
    -   Click "Launch Project".

## Project Structure

The project logic is modularized into several files within the `game/` directory:

-   `9_script.rpy`: The main game script. It contains the primary game loop, handles player input, and orchestrates calls to the various AI bots.
-   `1_api_config.rpy`: Initializes and configures API keys and the MongoDB database connection.
-   `2_character_profile.rpy`: A centralized function that defines the personality, speech style, and traits for all characters in the game.
-   `3_story_prompt.rpy`: Generates the initial story scenario when a new game is started.
-   `4_story.rpy`: The database abstraction layer. A `Story` class that manages all interactions with MongoDB collections (stories, events, memories).
-   `4_emotion_detection.rpy`: Contains the `EmotionDeterminationBot` class, responsible for analyzing context and determining a character's emotional state.
-   `4_background_detection.rpy`: Contains the `BackgroundDetector` class, which selects a scene background based on the narrator's output.
-   `5_backgrounds.rpy`: Ren'Py script to define and register all background images.
-   `5_character_sprites.rpy`: Ren'Py script to define and register all character sprites for every possible emotion.
-   `6_character_bot.rpy`: Contains the `CharacterBot` class, which generates dialogue for NPCs.
-   `7_narrator.txt`: Contains the `NarratorBot` class, which generates descriptive text for the story world.
-   `8_speaker_determination.rpy`: Contains the `SpeakerDeterminationBot` class for the advanced two-stage speaker inference.


