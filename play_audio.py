from vlc import MediaPlayer
from time import sleep

class PlayAudio():

    def __init__(self):
        self.happy = ("sound_files/thumb_up_yippee.mp3", 3)
        self.sad = ("sound_files/thumb_down_downer_noise.mp3", 5)
        self.peace = ("sound_files/victory_sign_mario_kart_win.mp3", 6)
    
    def play_sound(self, emotion):
        match emotion:
            case "rock":
                sound = self.happy
            case "paper":
                sound = self.sad
            case "scissors":
                sound = self.peace
        
        player = MediaPlayer(sound[0])
        player.play()
        sleep(sound[1])