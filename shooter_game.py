import pygame
import random
from pygame import *


pygame.init()
mixer.init()


genislik = 700
yukseklik = 500
pencere = display.set_mode((genislik, yukseklik))
display.set_caption("Uzay Oyunu")
arka_plan = transform.scale(image.load("galaxy.jpg"), (genislik, yukseklik))


mixer.music.load("space.ogg")
mixer.music.play(-1)
ates_sesi = mixer.Sound("fire.ogg")


skor = 0
kacan = 0
yazi = pygame.font.Font(None, 36)


class OyunNesnesi(sprite.Sprite):
    def __init__(self, resim, x, y, hiz, boyut=(65, 65)):
        super().__init__()
        self.image = transform.scale(image.load(resim), boyut)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.hiz = hiz

    def ciz(self):
        pencere.blit(self.image, self.rect)

class Oyuncu(OyunNesnesi):
    def __init__(self, resim, x, y, hiz):
        super().__init__(resim, x, y, hiz, (100, 60))

    def hareket(self):
        tuslar = key.get_pressed()
        if tuslar[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.hiz
        if tuslar[K_RIGHT] and self.rect.x < genislik - self.rect.width:
            self.rect.x += self.hiz

class Dusman(OyunNesnesi):
    def __init__(self, x, y, hiz):
        super().__init__("ufo.png", x, y, hiz, (60, 50))

    def hareket(self):
        self.rect.y += self.hiz

class Mermi(OyunNesnesi):
    def __init__(self, x, y):
        super().__init__("bullet.png", x, y, 7, (10, 20))

    def hareket(self):
        self.rect.y -= self.hiz
        if self.rect.bottom < 0:
            self.kill()


oyuncu = Oyuncu("rocket.png", 300, 420, 5)
dusmanlar = sprite.Group()
mermiler = sprite.Group()

for _ in range(5):
    x = random.randint(0, genislik - 60)
    y = random.randint(-100, -40)
    hiz = random.randint(2, 5)
    dusmanlar.add(Dusman(x, y, hiz))


saat = time.Clock()
calisiyor = True
bitis = False

while calisiyor:
    pencere.blit(arka_plan, (0, 0))

    for e in event.get():
        if e.type == QUIT:
            calisiyor = False
        if e.type == KEYDOWN and e.key == K_SPACE and not bitis:
            mermi = Mermi(oyuncu.rect.centerx - 5, oyuncu.rect.top)
            mermiler.add(mermi)
            ates_sesi.play()

    if not bitis:
        oyuncu.hareket()
        oyuncu.ciz()

        dusmanlar.update()
        for d in dusmanlar:
            d.hareket()
            d.ciz()

        mermiler.update()
        for m in mermiler:
            m.hareket()
            m.ciz()

       
        vurulanlar = sprite.groupcollide(dusmanlar, mermiler, True, True)
        for _ in vurulanlar:
            skor += 1
            yeni = Dusman(random.randint(0, genislik - 60), random.randint(-100, -40), random.randint(2, 5))
            dusmanlar.add(yeni)

        
        for d in dusmanlar:
            if d.rect.top > yukseklik:
                kacan += 1
                d.rect.y = random.randint(-100, -40)
                d.rect.x = random.randint(0, genislik - d.rect.width)

       
        if sprite.spritecollide(oyuncu, dusmanlar, False):
            bitis = True
            sonuc = yazi.render("KAYBETTİN! Çarpışma oldu.", True, (255, 0, 0))
        elif skor > 10:
            bitis = True
            sonuc = yazi.render("TEBRİKLER! Kazandın!", True, (0, 255, 0))
        elif kacan >= 3:
            bitis = True
            sonuc = yazi.render("KAYBETTİN! 3 düşman kaçtı.", True, (255, 0, 0))
    else:
        pencere.blit(sonuc, (150, 200))

   
    pencere.blit(yazi.render(f"Skor: {skor}", True, (255, 255, 255)), (10, 10))
    pencere.blit(yazi.render(f"Kaçan: {kacan}", True, (255, 255, 255)), (10, 50))

    display.update()
    saat.tick(60)

pygame.quit()
