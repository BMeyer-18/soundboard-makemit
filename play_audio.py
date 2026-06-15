from vlc import MediaPlayer
from time import sleep


class PlayAudio:

    def __init__(self):
        # INSTRUCTIONS (part 1):
        # Add an instance variable for each gesture you want to include.
        # Each variable should be a tuple in which the first element is
        # the path to the sound effect that gesture corresponds to, and
        # the second element is the approximate length of the sound
        # effect in seconds (often rounded up).
        self.happy = ("sound_files/thumb_up_yippee.mp3", 3)
        self.sad = ("sound_files/thumb_down_downer_noise.mp3", 5)
        self.peace = ("sound_files/victory_sign_mario_kart_win.mp3", 6)
        self.okay = ("sound_files/duck_mac-quack.mp3", 2)
        self.mad = ("sound_files/duck_quack_reverb.mp3", 4)

    def play_sound(self, emotion):
        # INSTRUCTIONS (part 2):
        # Add a case to this match statement for each hand gesture you
        # want the model to recognize. Each case should be the name of
        # the hand gesture, which is the name of the folder in which the
        # images of that hand gesture are stored.
        # For each case, set the sound variable equal to the instance
        # variable you defined above for the corresponding sound effect.
        match emotion:
            case "thumbs_up":
                sound = self.happy
            case "thumbs_down":
                sound = self.sad
            case "peace":
                sound = self.peace
            case "okay":
                sound = self.okay
            case "fist":
                sound = self.mad

        # You shouldn't need to modify this code. Enjoy!
        player = MediaPlayer(sound[0])
        player.play()
        sleep(sound[1])
