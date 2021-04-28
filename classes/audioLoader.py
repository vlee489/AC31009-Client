from pygame import mixer
import json


class AudioLoader:
    def __init__(self, folder_location: str):
        """
        Loads in audio
        :param folder_location: Folder to load in
        """
        self.audio_by_id = {}
        self.audio = []
        with open(f"{folder_location}/data.json", "r") as f:
            data = json.load(f)
            for sound in data["moves"]:
                working_sound = mixer.Sound(f"{folder_location}/{sound['file']}")
                self.audio_by_id[f"{sound['id']}"] = working_sound
                self.audio.append(working_sound)
