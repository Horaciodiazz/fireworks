import pygame, random, math
import datetime
from datetime import datetime as dt


pygame.init()

width, height = 800, 500
window = pygame.display.set_mode((width, height))
name = pygame.display.set_caption('Fireworks')
clock, FPS = pygame.time.Clock(), 60

pallete = [
    (255, 0, 0),
    (0, 0, 255), 
    (0, 255, 0),
    (75, 0, 155),
    (255, 0, 215),
    (255, 100, 0)
]

#Fonts & Writing
class Writer:

    def __init__(self):
        pass
    
    def write(self, text, color, x, y, size):
        self.size = size
        pygame.font.init()
        self.font = pygame.font.Font('Python\Reddit Projects\PressStart2P-Regular.ttf', self.size)
        self.text = self.font.render(text, True, color)
        self.x = x - self.size * len(text) / 2
        self.y = y - self.size / 2
        window.blit(self.text, (self.x, self.y))

#Fireworks
class Firework():

    def __init__(self):
        r, g, b = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
        self.color = (r, g, b)
        self.width = 2
        self.height = random.randint(5, 10)
        self.x = random.randint(0 + self.width, width - self.width)
        self.y = 500 - self.height
        self.y_vel = random.randint(3, 5)
        self.dead = False
        self.deadline = random.uniform(250, 300)

    def move(self):
        self.y -= self.y_vel
        if self.y <= self.deadline:
            self.dead = True

    def draw(self):
        a = [int(self.x), int(self.y + self.height)]
        b = [int(self.x), int(self.y - self.height)]

        pygame.draw.line(window, self.color, a, b, self.width)

#Particles
class Particle:

    def __init__(self, x, y):
        self.color = random.choice(pallete)
        self.x = x
        self.y = y
        angle = random.randint(-60, 240)
        speed = random.uniform(0.3, 2.5)
        self.vx = speed * math.cos(math.radians(angle))
        self.vy = speed * math.sin(math.radians(angle))
        self.timer = 0
        self.finish = False

    def move(self):

        self.x += self.vx
        self.y -= self.vy
        self.timer += 1
        if self.timer >= FPS:
            self.finish = True

    def draw(self):

        pygame.draw.rect(window, self.color, (self.x, self.y, 2, 2))

def main():

    fireworks = [Firework()]
    particles = []
    writer = Writer()
    n = 0
    r, g, b = 255, 255, 255

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        window.fill((0, 0, 0))
        date = dt.now()
        current_time = date.strftime("%H:%M:%S, %d %b, %Y")
        new_year = date.strftime("%H:%M, %d %b, %Y")
        writer.write(f'Time(in Uruguay): {current_time}', ((r, g, b)), width // 2, 20, 16)

        if new_year == '00:00, 01 Jan, 2023':
            writer.write('2023', (255, 255, 0), width // 2, height // 2 - 110, 64)
            try:
                writer.write('Happy New Year!', (pallete[n]), width // 2, height // 2  - 180, 32)
            except IndexError:
                n = random.randint(0, len(pallete))


            if random.uniform(0, 1) <= 1/45:
                fireworks.append(Firework())
                r, g, b = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
                n = random.randint(0, len(pallete))

            for firework in fireworks:
                firework.draw()
                firework.move()
                if firework.dead:
                    fireworks.remove(firework)
                    particles += [Particle(firework.x, firework.y) for i in range(15)]
                for particle in particles:
                    particle.draw()
                    particle.move()
                    if particle.finish:
                        particles.remove(particle)

        pygame.display.update()
        clock.tick(FPS)

main()

