#5_character_sprites.rpy
init python:
    # Define character sprite images
    for character in ["emma", "max", "liam", "olivia", "noah", "isabella", "ethan", "sophia", "lucas", "ava"]:
        for emotion in ["normal", "angry", "smile", "sad", "annoyed", "shocked", "sleepy", "delighted", "pride", "laugh"]:
            renpy.image(character + "/" + emotion, f"images/characters/{character}/{emotion}.png")
