import pygame
import sys
import random
import time



# Initialisation de Pygame
pygame.init()

# Musique
pygame.mixer.init()

# Création d'un objet pour écrire
font = pygame.font.Font(None, 36)

# Définition des couleurs
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Paramètres du jeu
WIDTH, HEIGHT = 900, 600
FPS = 60

# Paramètre tire du joueur
MIN_SHOOT_DELAY = 200  # en millisecondes (0.5 secondes)


# Fonction pour dessiner du texte centré
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# Fonction pour le bouton avec effet "hover"
def button(text, x, y, width, height, inactive_color, active_color, action=None):
    cur = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x < cur[0] < x + width and y < cur[1] < y + height:
        pygame.draw.rect(screen, active_color, (x, y, width, height))

        if click[0] == 1 and action is not None:
            action()
    else:
        pygame.draw.rect(screen, inactive_color, (x, y, width, height))

    smallText = pygame.font.Font("freesansbold.ttf", 20)
    textSurf, textRect = text_objects(text, smallText)
    textRect.center = ((x + (width / 2)), (y + (height / 2)))
    screen.blit(textSurf, textRect)

# Fonction pour rendre le texte du bouton
def text_objects(text, font):
    textSurface = font.render(text, True, WHITE)
    return textSurface, textSurface.get_rect()

# Fonction pour l'action du bouton (démarrer le jeu)
def start_game():
    global in_menu
    in_menu = False
    
    
# Fonction pour l'action du bouton "Rejouer"
# Fonction pour l'action du bouton "Rejouer"
def restart_game():
    global game_over, in_menu, countdown, player

    # Réinitialiser les variables du jeu
    player.rect.centerx = WIDTH // 2
    player.rect.bottom = HEIGHT - 20
    player.speedx = 0
    player.score = 0

    for enemy in enemies:
        enemy.kill()

    for bullet in player.bullets:
        bullet.kill()

    countdown = 3
    game_over = False
    in_menu = False
    
    # Ajoutez à nouveau le joueur au groupe all_sprites
    all_sprites.add(player)



# Fonction pour l'action du bouton "Quitter"
def quit_game():
    pygame.quit()
    sys.exit()


# Classe du vaisseau spatial
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load("Ressources/Img/vaisseau.png").convert()
        self.image.set_colorkey(BLACK)  # Si votre image a un fond noir, il sera rendu transparent
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 20
        self.speedx = 0
        self.score = 0
        self.last_shot_time = 0  # Ajout de la variable pour le suivi du dernier tir

        # Chargement des fonds
        self.background = background
        self.second_background = second_background
        self.third_background = third_background

        # Groupe pour les balles du joueur
        self.bullets = pygame.sprite.Group()

    def update(self):
        self.speedx = 0
        self.speedy = 0

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.speedx = -8
        if keys[pygame.K_RIGHT]:
            self.speedx = 8
        if keys[pygame.K_UP]:
            self.speedy = -8
        if keys[pygame.K_DOWN]:
            self.speedy = 8

        self.rect.x += self.speedx
        self.rect.y += self.speedy

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

        # Tir du joueur avec limitation de la fréquence
        if keys[pygame.K_SPACE]:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_shot_time > MIN_SHOOT_DELAY:
                self.shoot()
                self.last_shot_time = current_time

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top, -1)  # direction vers le haut
        all_sprites.add(bullet)
        self.bullets.add(bullet)
        
        # sonBalles.play()  # Jouer le son des tirs

    def change_background(self):
        # Changer le fond en fonction du score
        if self.score >= 5 and self.score < 15:
            return self.second_background
        elif self.score >= 25:
            return self.background
        else:
            return self.third_background

        

# Classe des ennemis
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        original_image = pygame.image.load("Ressources/Img/vaisseauEnnemi.png").convert()
        original_image.set_colorkey(BLACK)
        self.image = pygame.transform.rotate(original_image, 180)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)

        # Groupe pour les balles des ennemis
        self.bullets = pygame.sprite.Group()

        # Ajoutez une variable pour le compteur de temps entre les tirs
        self.shoot_cooldown = random.randint(50, 200)  # Choisissez une valeur initiale aléatoire

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)

        # Mise à jour du compteur de temps entre les tirs
        self.shoot_cooldown -= 1

        # Tir des ennemis si le compteur de temps atteint zéro
        if self.shoot_cooldown <= 0:
            self.shoot()
            # Réinitialisez le compteur de temps pour le prochain tir
            self.shoot_cooldown = random.randint(50, 200)  # Choisissez une nouvelle valeur aléatoire

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.bottom, 1)  # direction vers le bas
        all_sprites.add(bullet)
        self.bullets.add(bullet)
        enemy_bullets.add(bullet)
        # sonBalles.play()  # Jouer le son des tirs

    def kill(self):
        explosion = Explosion(self.rect.center, 1)  # Taille de l'explosion (1, 2, 3, ...)
        all_sprites.add(explosion)
        explosions.add(explosion)
        super().kill()

            
# Classe des balles
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.image = pygame.image.load("Ressources/Img/spaceBullet.jpg").convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speedy = direction * 10  # direction = 1 pour tir du joueur, -1 pour tir des ennemis
        sonBalles.play()

    def update(self):
        self.rect.y += self.speedy
        # Supprimer la balle lorsqu'elle sort de l'écran
        if self.rect.bottom < 0 or self.rect.top > HEIGHT:
            self.kill()
            sonBalles.stop()
            
            
class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        super().__init__()
        self.size = size
        self.image = pygame.image.load("Ressources/Img/explosion.png").convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0  # Pour l'animation de l'explosion
        sound_explode.play()
        self.expiration_time = pygame.time.get_ticks() + 200  # Expire après 1000 millisecondes (1 seconde)
        
        self.sound_expiration_time = pygame.time.get_ticks() + 3000
        

    def update(self):
        # Ajoutez ici la logique d'animation si nécessaire
        # Vérifiez si l'explosion a expiré
        if pygame.time.get_ticks() > self.expiration_time:
            self.kill()  # Supprime l'explosion lorsque le temps d'expiration est atteint
            
        # Vérifiez si l'expiration du son est atteinte
        if pygame.time.get_ticks() > self.sound_expiration_time:
            sound_explode.stop()  # Arrête le son de l'explosion

        

# Initialisation de la fenêtre
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Chargement du fond
background = pygame.image.load("Ressources/Img/fondSpace.jpg").convert()
second_background = pygame.image.load("Ressources/Img/secondBackground.jpg").convert()
third_background = pygame.image.load("Ressources/Img/thirdBackground.jpg").convert()
fourth_background = pygame.image.load("Ressources/Img/menu_background.jpg").convert()

# Redimensionner le fond pour qu'il ait la taille du cadre du jeu
fourth_background = pygame.transform.scale(fourth_background, (WIDTH, HEIGHT))

# Chargement de la musique d'ambiance
pygame.mixer.music.load("Ressources/Audio/musiquefond.wav")

# Charger son de la balle
sonBalles = pygame.mixer.Sound("Ressources/Audio/laser-gun-shot.wav")

sound_explode = pygame.mixer.Sound("Ressources/Audio/sound_explode.mp3")

pygame.display.set_caption("Space Shooter")
clock = pygame.time.Clock()

# Création des groupes de sprites
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
explosions = pygame.sprite.Group()
enemy_bullets = pygame.sprite.Group()


# Compte à rebours
countdown = 3

# Variable pour indiquer si le jeu est en cours ou si nous sommes dans le menu
in_menu = True

# Variable pour la gestion de la fenêtre de fin de jeu
game_over = False

# Boucle principale
while in_menu:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Afficher le titre du jeu
    screen.blit(background, (0, 0))
    draw_text("Space Shooter", font, WHITE, screen, WIDTH // 2 - 80, HEIGHT // 4)

    # Afficher le bouton "Jouer"
    button("Jouer", WIDTH // 2 - 100, HEIGHT // 2, 200, 50, (BLACK), (RED), start_game)

    # Rafraîchissement de l'écran
    pygame.display.flip()

    # Limite de FPS
    clock.tick(FPS)

# Création du vaisseau spatial
player = Player()
all_sprites.add(player)

# Création des ennemis
for _ in range(5):
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)

# Boucle principale
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Jouer la musique d'ambiance
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.play(loops=-1)

    # Mise à jour des sprites
    all_sprites.update()
    explosions.update()

    # Afficher le compte à rebours
    if countdown > 0:
        screen.fill(BLACK)
        draw_text(str(countdown), font, WHITE, screen, WIDTH // 2 - 20, HEIGHT // 2 - 20)
        pygame.display.flip()
        pygame.time.delay(1000)
        countdown -= 1
    else:
        # Gestion des collisions entre le joueur et les ennemis
        hits = pygame.sprite.spritecollide(player, enemies, False)
        for hit in hits:
            player.kill()  # Supprime le joueur
            explosion = Explosion(player.rect.center, 1)  # Crée une explosion au centre du joueur
            all_sprites.add(explosion)
            explosions.add(explosion)
            # sound_explode.play()
            game_over = True  # Le jeu s'arrête si le joueur touche un ennemi

        # Gestion des collisions entre les balles du joueur et les ennemis
        hits = pygame.sprite.groupcollide(enemies, player.bullets, True, True)
        for enemy_hit in hits:
            # Vous pouvez ajouter des actions supplémentaires ici
            # Par exemple, augmenter le score
            player.score += 1
            
            explosion = Explosion(enemy_hit.rect.center, 1)  # Crée une explosion au centre de l'ennemi touché
            all_sprites.add(explosion)
            explosions.add(explosion)
            
            # sonBalles.play()  # Jouer le son des balles
            # sound_explode.play()

        # Gestion des collisions entre les balles des ennemis et le joueur / enemy.bullets
        hits = pygame.sprite.spritecollide(player, enemy_bullets, True)
        if hits:
            # Vous pouvez ajouter des actions supplémentaires ici
            player.kill()  # Supprime le joueur
            explosion = Explosion(player.rect.center, 1)  # Crée une explosion au centre du joueur
            all_sprites.add(explosion)
            explosions.add(explosion)
            # sound_explode.play()
            game_over = True  # Le jeu s'arrête si le joueur est touché par une balle ennemie

        # Générer de nouveaux ennemis si le nombre d'ennemis actuels est inférieur à un certain seuil
        while len(enemies) < 5:
            enemy = Enemy()
            all_sprites.add(enemy)
            enemies.add(enemy)

        # Changer le fond en fonction du score
        background = player.change_background()

        # Background
        screen.blit(background, (0, 0))

        # Score
        score_text = font.render(f"Score : {player.score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        # Dessin
        all_sprites.draw(screen)
        explosions.draw(screen)  # Dessine les explosions

        # Rafraîchissement de l'écran
        pygame.display.flip()

        # Limite de FPS
        clock.tick(FPS)

        # Gestion de la fenêtre de fin de jeu
        while game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = False
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        restart_game()
                    elif event.key == pygame.K_q:
                        quit_game()

            # Afficher la fenêtre de fin de jeu
            screen.blit(fourth_background, (0, 0))
             # Afficher le texte "Game Over"
            draw_text("Game Over !", font, (RED), screen, WIDTH // 2 - 70, HEIGHT // 3)

            # Afficher le score final du joueur
            draw_text(f"Score final : {player.score}", font, (124,252,0), screen, WIDTH // 2 - 80, HEIGHT // 2 - 40)

            # Afficher le bouton "Rejouer"
            button("Rejouer", WIDTH // 2 - 100, HEIGHT // 2 + 20, 200, 50, (BLACK), (BLACK), restart_game)

            # Afficher le bouton "Quitter"
            button("Quitter", WIDTH // 2 - 100, HEIGHT // 2 + 90, 200, 50, (RED), (RED), quit_game)

            pygame.display.flip()
            clock.tick(FPS)

# Arrêter la musique lorsque le jeu se termine
pygame.mixer.music.stop()

# Quitter le jeu
pygame.quit()
sys.exit()
