import pygame

class Sapling(pygame.sprite.Sprite):
  def __init__(self, x, y, img_file):
      '''
      Initializes the sapling sprite.
      '''
      pygame.sprite.Sprite.__init__(self)
      self.image = pygame.image.load(img_file).convert_alpha()
      self.rect = self.image.get_rect()
      self.rect.x = x
      self.rect.y = y
