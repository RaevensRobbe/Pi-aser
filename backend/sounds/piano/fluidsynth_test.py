# import time
# from Modules import mypyfluid  as pyfluidsynth

# fs = pyfluidsynth.Synth()
# fs.start()

# sfid = fs.sfload("example.sf2")
# fs.program_select(0, sfid, 0, 0)

# fs.noteon(0, 60, 30)
# fs.noteon(0, 67, 30)
# fs.noteon(0, 76, 30)
# print("speelt akkoord")
# time.sleep(1.0)

# fs.noteoff(0, 60)
# fs.noteoff(0, 67)
# fs.noteoff(0, 76)

# time.sleep(1.0)

# fs.delete()

# import pygame
# pygame.mixer.init()
# pygame.mixer.music.load("/home/robbe/1920-1mct-project1-RaevensRobbe/Code/backend/sounds/piano/A.wav")
# pygame.mixer.music.play()
import pygame
import time
pygame.init()
pygame.mixer.init()
sound = pygame.mixer.Sound("/home/robbe/1920-1mct-project1-RaevensRobbe/Code/backend/sounds/piano/C.wav")
sound.play()
sound = pygame.mixer.Sound("/home/robbe/1920-1mct-project1-RaevensRobbe/Code/backend/sounds/piano/A.wav")
sound.play()
while pygame.mixer.get_busy():
    print(pygame.mixer.get_busy())



# import playsound

# playsound.playsound('C.wav',True)


# import os
# activatedNote = "A"
# os.system(f'aplay /home/robbe/1920-1mct-project1-RaevensRobbe/Code/backend/sounds/piano/{activatedNote}.wav')