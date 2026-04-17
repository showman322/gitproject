import pygame
import os

def mus_player():
    pygame.init()
    pygame.mixer.init()

    WIDTH, HEIGHT = 800, 800
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Music Player")

    font = pygame.font.Font(None, 36)
    clock = pygame.time.Clock()

    playlist = [
        "music_player/music/titanium.mp3",
        "music_player/music/cheapthrills.mp3",
        "music_player/music/saymyname.mp3"
    ]
    current_track = 0
    is_paused = False

    def load_track():
        pygame.mixer.music.load(playlist[current_track])

    def play_music():
        pygame.mixer.music.play()

    def stop_music():
        nonlocal is_paused
        pygame.mixer.music.stop()
        is_paused = False

    def pause_music():
        nonlocal is_paused
        if not is_paused:
            pygame.mixer.music.pause()
            is_paused = True
        else:
            pygame.mixer.music.unpause()
            is_paused = False

    def next_track():
        nonlocal current_track, is_paused

        current_track += 1
        
        if current_track >= len(playlist):
            current_track = 0
        load_track()
        play_music()
        is_paused = False

    def previous_track():
        nonlocal current_track, is_paused

        current_track -= 1

        if current_track < 0:
            current_track = len(playlist) - 1
        load_track()
        play_music()
        is_paused = False


    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    load_track()
                    play_music()
                elif event.key == pygame.K_SPACE:
                    pause_music()
                elif event.key == pygame.K_q:
                    running = False
                elif event.key == pygame.K_s:
                    stop_music()
                elif event.key == pygame.K_n:
                    next_track()
                elif event.key == pygame.K_b:
                    previous_track()

        screen.fill((30, 30, 30))
        
        track_name = os.path.basename(playlist[current_track])
        track_position = f"{current_track + 1} / {len(playlist)}"

        title_text = font.render("Music Player", True, (255, 255, 255))
        track_text = font.render(f"Track: {track_name}", True, (255, 255, 255))
        position_text = font.render(f"Playlist position: {track_position}", True, (255, 255, 255))
        controls_text = font.render("P-Play S-Stop Q-Quit SPACE-Pause N-Next B-Back", True, (200, 200, 200)) 

        screen.blit(title_text, (280, 80))
        screen.blit(track_text, (180, 180))
        screen.blit(position_text, (180, 240))
        screen.blit(controls_text, (70, 700))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()