# 2_character_profile.rpy
init python:
    from typing import Dict

    def get_character_profiles() -> Dict[str, Dict[str, str]]:
        """
        Central function to maintain character profiles used throughout the game.
        Returns a dictionary of character profiles with their attributes.
        """
        return {
            'emma': {
                'description': 'Emma is a perceptive and insightful character, often understanding the unspoken feelings of others.',
                'speech_style': 'Thoughtful and caring, she often tries to reassure others.',
                'personality': 'Empathetic and observant, but can be hesitant to confront directly.',
                'traits': {
                    'empathy': 0.9,
                    'observant': 0.8,
                    'reassuring': 0.8,
                    'confrontational': 0.2
                }
            },
            'max': {
                'description': 'Max is straightforward and direct, often probing deeper into conversations.',
                'speech_style': 'Confident and assertive, he challenges others.',
                'personality': 'Bold and protective, but can be impulsive.',
                'traits': {
                    'straightforward': 0.9,
                    'assertive': 0.8,
                    'protective': 0.7,
                    'impulsive': 0.4
                }
            },
            'liam': {
                'description': 'Liam is a curious and adventurous young man, always eager to explore new horizons.',
                'speech_style': 'Energetic and inquisitive, he asks many questions.',
                'personality': 'Brave and curious, but can be reckless at times.',
                'traits': {
                    'curious': 0.9,
                    'energetic': 0.8,
                    'brave': 0.7,
                    'reckless': 0.5
                }
            },
            'olivia': {
                'description': 'Olivia is a kind and compassionate soul, often offering a listening ear to those in need.',
                'speech_style': 'Gentle and nurturing, she speaks with a soothing tone.',
                'personality': 'Empathetic and patient, but can be timid in confrontational situations.',
                'traits': {
                    'kind': 0.9,
                    'compassionate': 0.8,
                    'patient': 0.8,
                    'timid': 0.4
                }
            },
            'noah': {
                'description': 'Noah is a logical and analytical thinker, always seeking to understand the world around him.',
                'speech_style': 'Measured and precise, he articulates his thoughts carefully.',
                'personality': 'Intelligent and rational, but can be aloof and detached at times.',
                'traits': {
                    'logical': 0.9,
                    'analytical': 0.8,
                    'rational': 0.7,
                    'aloof': 0.4
                }
            },
            'isabella': {
                'description': 'Isabella is a creative and imaginative individual, often seen with a sketchpad in hand.',
                'speech_style': 'Expressive and eloquent, she has a flair for storytelling.',
                'personality': 'Artistic and whimsical, but can be easily distracted.',
                'traits': {
                    'creative': 0.9,
                    'imaginative': 0.8,
                    'expressive': 0.8,
                    'distractable': 0.5
                }
            },
            'ethan': {
                'description': 'Ethan is a skilled outdoorsman, comfortable in the wilderness and adept at survival.',
                'speech_style': 'Concise and practical, he speaks with a no-nonsense tone.',
                'personality': 'Rugged and self-reliant, but can be gruff and unsociable.',
                'traits': {
                    'skilled': 0.9,
                    'practical': 0.8,
                    'self_reliant': 0.7,
                    'gruff': 0.4
                }
            },
            'sophia': {
                'description': 'Sophia is a diplomatic and level-headed individual, often acting as a peacekeeper.',
                'speech_style': 'Thoughtful and measured, she chooses her words carefully.',
                'personality': 'Rational and composed, but can be overly cautious at times.',
                'traits': {
                    'diplomatic': 0.9,
                    'level_headed': 0.8,
                    'composed': 0.7,
                    'cautious': 0.5
                }
            },
            'lucas': {
                'description': 'Lucas is a charming and charismatic person, able to easily win over those around him.',
                'speech_style': 'Smooth and persuasive, he has a way with words.',
                'personality': 'Confident and sociable, but can be manipulative and self-serving.',
                'traits': {
                    'charming': 0.9,
                    'charismatic': 0.8,
                    'persuasive': 0.8,
                    'manipulative': 0.5
                }
            },
            'ava': {
                'description': 'Ava is a passionate and determined individual, driven to achieve her goals.',
                'speech_style': 'Passionate and resolute, her words carry weight and conviction.',
                'personality': 'Ambitious and resilient, but can be stubborn and headstrong.',
                'traits': {
                    'passionate': 0.9,
                    'determined': 0.8,
                    'ambitious': 0.7,
                    'stubborn': 0.5
                }
            }
        }
