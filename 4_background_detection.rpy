init python:
    import requests

    class BackgroundDetector:
        def __init__(self, api_key: str, story_db: Story):
            self.api_key = api_key
            self.story_db = story_db
            self.backgrounds = [
    "abandoned_warehouse_inside_day", "abandoned_warehouse_inside_night", "airship_wreck", 
    "airship_wreck_night", "amusement_park_day", "amusement_park_night", "ancient_temple", 
    "art_room", "art_room_night", "Attic_Room_day", "Attic_Room_night", "auditiorium_night", 
    "auditorium_backstage", "auditorium_day", "backyard_day", "backyard_day_night", 
    "basement_day", "basketball_court", "basketball_court_evening", "bathroom_day", 
    "bathroom_night", "beach_day", "beach_night", "bedroom_lights", "bedroom_morning", 
    "cafe_outdoor", "cafe_outdoor_night", "canyon_day", "canyon_night", "castle_night", 
    "cemetry_day", "cemetry_night", "city_rooftop_day", "city_rooftop_night", 
    "city_street_day", "city_street_night", "classroom_daylight", "classroom_frontview_day", 
    "classroom_front_day", "classroom_night", "classroom_sideview_night", "class_corner_night", 
    "class_front_day", "class_front_night", "class_middleveiw_day", "cliffside_village", 
    "coastal_cliff_day", "coastal_cliff_night", "computer_lab", "cottage_day", "cottage_night", 
    "dark_dense_forest", "dark_forest", "dark_mysterious_class", "dense_forest_night", 
    "deserted_marketplace", "deserted_temple", "desert_night", "desert_oasis_day", 
    "desert_with_camels", "dining_room_day", "dining_room_night", "dusty_attic_day", 
    "flower_field_day", "forest_clearing_night", "forest_glade_day", "forest_glade_night", 
    "frontyard_day", "front_porch_night", "garage_day", "garden_gazebo", "garden_gazebo_night", 
    "gym_area_day", "gym_area_night", "Hallway", "hallway_night", "hidden_fortress_day", 
    "hidden_fortress_night", "hidden_waterfall_day", "hidden_waterfall_night", 
    "high_cliffs_day", "high_cliffs_night", "hospital_corridor_day", "hospital_corridor_night", 
    "hospital_entrance_day", "hospital_entrance_night", "hospital_lobby_day", 
    "hospital_lobby_night", "house_backdoor", "house_balcony_day", "house_balcony_night", 
    "house_front_Day", "house_garden_day", "house_garden_night", "house_hallway_day", 
    "house_hallway_night", "house_staircase_day", "house_staircase_night", "ice_rink", 
    "ice_rink_day", "image (29)", "image (7)", "jungle_ruins", "kitchen_day", "kitchen_night", 
    "lakeside-pier_night", "lakeside_pier_day", "latern_festival", "library_corner", 
    "library_corner_day", "library_day", "library_night", "living_room_day", 
    "living_room_night", "locker_day", "locker_room_night", "Loft_Room", "Loft_Room_day", 
    "magical_forest", "marketplace_day", "marketplace_night", "mountainpeak", 
    "mountain_campfire", "mountain_pass", "mountain_pass_day", "music_room_day", 
    "music_room_night", "mysterious_forest", "patient_room_day", "patient_room_night", 
    "peaceful_forest_clearing", "playarea_night", "playground", "rainy_street", 
    "residential_area_day", "residential_area_night", "restaurant_day", "restaurant_night", 
    "river_crossing_day", "river_crossing_night", "Rooftop_dining", "Rooftop_Room_day", 
    "Rooftop_Room_night", "school_backgate_day", "school_back_night", "school_canteen", 
    "school_courtyard_day", "school_courtyard_night", "school_courtyard_view_day", 
    "school_courtyard_view_night", "school_entrance", "school_entrance_night", 
    "school_festival_night", "school_festival_stalls_day", "school_front_day", 
    "school_front_night", "school_garden_day", "school_garden_night", 
    "school_nurse_office_day", "school_nurse_office_night", "school_parking_day", 
    "school_parking_evening", "school_rooftop_day", "school_rooftop_night", 
    "school_staircase_day", "school_staircase_night", "science_lab", "shipwrecked shore", 
    "ship_wrecked_day", "Small_Balcony_Room", "Small_Balcony_Room_night", "snowy_feild", 
    "snowy_plain", "snow_covered_mountain", "snug_livingroom_day", "sports_field_day", 
    "sports_field_night", "sports_room", "staff_room_day", "staff_room_night", 
    "starry_beach_night", "street_cherryblossom_trees", "Study_Room_day", "Study_Room_night", 
    "sunset_beach", "swamp_day", "swamp_night", "swimming_pool_day", "swimming_pool_night", 
    "Tea_Room_day", "Tea_Room_night", "terrace_day", "terrace_night", "thick_forest", 
    "train_station_day", "train_station_night", "tranquil_flower_field", 
    "tranquil_flower_field_night", "underground_cave", "underground_tomb", "vineyard_day", 
    "vineyard_night"
]


        def detect_background(self, story_id: str, narrator_output: str) -> str:
            context = self.story_db.get_story_context(story_id)
            current_background = context.get('story_info', {}).get('current_background', 'default')
            system_prompt = f"""Background Detection Task:
            Available backgrounds: {', '.join(self.backgrounds)}
            Carefully analyze the narrator's output and determine the most appropriate background.
            Guidelines:
            1. Match the background exactly if possible
            2. If no exact match, find the closest semantic match
            3. Consider the context and setting described
            4. If no clear match, retain the previous background
            Narrator's output: {narrator_output}
            Requirements:
            - Respond with ONLY the background name from the provided list
            - If no suitable background is found, return the current/previous background
            - Be precise and contextually aware"""

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
                detected_background = response.json()['choices'][0]['message']['content'].strip().lower()
                if detected_background in self.backgrounds:
                    self.story_db.update_background(story_id, detected_background)
                    return detected_background
                closest_match = self.find_closest_background(detected_background)
                if closest_match and closest_match != current_background:
                    self.story_db.update_background(story_id, closest_match)
                    return closest_match
                return current_background
            except Exception as e:
                print(f"Error in background detection: {e}")
                return current_background

        def find_closest_background(self, input_background: str) -> str:
            if input_background in self.backgrounds:
                return input_background
            matches = [bg for bg in self.backgrounds if input_background in bg or bg in input_background]
            if matches:
                return matches[0]
            semantic_mappings = {
                "indoor": ["bedroom", "kitchen", "classroom", "house_in_woods"],
                "outdoor": ["beach", "park", "forest", "town_street"],
                "city": ["city_night", "city_morning", "city_afternoon", "town_street"],
                "nature": ["beach", "forest", "flowers_meadows", "park"],
                "building": ["school_entrance", "restaurant", "church", "cinema"]
            }
            for category, backgrounds in semantic_mappings.items():
                if any(category in input_background.lower() for category in semantic_mappings):
                    return backgrounds[0]
            return None