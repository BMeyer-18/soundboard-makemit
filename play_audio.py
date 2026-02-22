from vlc import MediaPlayer
from time import sleep

class PlayAudio():

    def __init__(self):
        self.happy = ("sound_files/thumb_up_yippee.mp3", 3)
        self.sad = ("sound_files/thumb_down_downer_noise.mp3", 5)
        self.peace = ("sound_files/victory_sign_mario_kart_win.mp3", 6)
        self.okay = ("sound_files/duck_mac-quack.mp3", 2)
        self.mad = ("sound_files/duck_quack_reverb.mp3", 4)
    
    def play_sound(self, emotion):
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
        
        player = MediaPlayer(sound[0])
        player.play()
        sleep(sound[1])