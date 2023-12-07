from random import choice

from src.target import GenericTarget
from src.consts import CAT_ANIMATIONS, WIDTH, HEIGHT


# Эта штука создаёт и обрабатывает массив котов (в голове это звучит лучше чем в тексте)
class CatFactory:
	def __init__(self, screen, gun, count):
		self._cat_types = [
			CatOne,
			CatTwo,
			CatThree,
		]
		self._gun = gun # Используется для движения "целей"
		self._screen = screen
		self._cats = [self._spawn_cat() for _ in range(count)]

	def __iter__(self):
		return self._cats.__iter__()

	def __len__(self):
		return self._cats.__len__()

	def increase(self):
		self._cats.append(self._spawn_cat())

	def _spawn_cat(self):
		return choice([
			CatOne, CatTwo, CatThree
		])(self._screen, self._gun)

	def draw(self):
		# enumerate оч медленная, потому так
		for i in range(len(self._cats)):
			if self._cats[i].finished:
				self._cats[i] = self._spawn_cat()
			self._cats[i].move()
			self._cats[i].draw()


# Наши существа
class CatOne(GenericTarget):
  animation = CAT_ANIMATIONS[0]
  standby_frames_count = 7

  def __init__(self, screen, gun):
    super().__init__(screen, gun)


class CatTwo(GenericTarget):
  animation = CAT_ANIMATIONS[1]
  standby_frames_count = 7

  def __init__(self, screen, gun):
    super().__init__(screen, gun)

  def move(self):
    pass


class CatThree(GenericTarget):
  animation = CAT_ANIMATIONS[2]
  standby_frames_count = 7

  def __init__(self, screen, gun):
    super().__init__(screen, gun)

  def move(self):
    if self.tick % 2 != 0 or self.live < 1:
      return

    # О НЕТ ДЖОННИ ОНИ НА ДЕРЕВЬЯХ
    step = self.step
    o = round(self.r / 2)
    if self.x > WIDTH - self.r or self.y > HEIGHT - self.r:
      return
    if self.gun.x - o < self.x:
      self.x += round(step / 2)
      step = round(step / 2)
    elif self.gun.x + o > self.x:
      self.x -= round(step / 2)
      step = round(step / 2)
    if self.gun.y - o < self.y:
      self.y += step
    elif self.gun.y + o > self.y:
      self.y -= step
