import numpy as np
import cv2
import random

def similarity(pic1, pic2): # same size pictures
	dessim_max = 255 * number_pixels
	dessim = sum(pix_pic1 - pix_pic2) # subtrair as imagens e somar todos os pixels
	return 1 - (dessim / dessim_max)

def randPosition(max_x, max_y):
	return (random.randrange(0, max_x), random.randrange(0, max_y))

class Bee:
	"""docstring for Bee"""
	def __init__(self, job, start_position):
		self.job = job
		self.current_pos = start_position
		self.best = 0
		self.repeats = 0

	def __eq__(self, other):
		if self.current_pos == other.current_pos:
			return True
		return False

	def get_x(self):
		return self.current_pos[0]

	def get_y(self):
		return self.current_pos[1]

	def test_improve(self, value):
		if value > self.best:
			self.best = max(value, self.best)
			repeats = 0
		else:
			repeats += 1

	def test_around(self, value, other_position):
		if value > self.best:
			self.best = max(value, self.best)
			self.current_pos = other_position
			repeats = 0
		else:
			repeats += 1

	def rand_around(self):
		return (self.current_pos[0] + random.randint(-2, 2), self.current_pos[1], random.randint(-2, 2))

	def pick(self, emp, bs):
		weights = [x.best / bs for x in emp]
		chosen = random.choices(emp, weights)
		self.current_pos = chosen.current_pos
		self.best = chosen.best


def myMatch(pic, temp):

	pic_height, pic_width, _ = pic.shape
	temp_height, temp_width, _ = temp.shape

	employed = [Bee("employed", randPosition(pic_width, pic_height)) for _ in range(200)]
	onlooker = [Bee("onlooker", (0,0)) for _ in range(200)]
	scout = []
	
	best_bee = Bee("placeholder", (0,0))

	iteracoes = 0
	while iteracoes < 100:

		best_sum = 0

		# search phase
		for bee in employed:
			cropped_pic = pic[bee.get_y():bee.get_y() + temp_height, bee.get_x():bee.get_x() + temp_width]
			bee.test_improve(similarity(temp, cropped_pic))

			# olhar a vizinhanca
			novo = bee.rand_around()
			cropped_pic = pic[novo[1]:novo[1] + temp_height, novo[0]:novo[0] + temp_width]
			bee.test_around(similarity(temp, cropped_pic), novo)

			best_sum += bee.best

			if bee.best > best_bee.best:
				best_bee = bee

			if bee.repeats >= 5:
				scout.append(bee)

		# dance phase
		for bee in onlooker:
			bee.pick(employed, best_sum)

			# olhar a vizinhanca
			novo = bee.rand_around()
			cropped_pic = pic[novo[1]:novo[1] + temp_height, novo[0]:novo[0] + temp_width]
			bee.test_around(similarity(temp, cropped_pic), novo)

			if bee.best > best_bee.best:
				best_bee = bee

			if bee.repeats >= 5:
				scout.append(bee)

		for bee in scout[:]:
			if bee in onlooker:
				onlooker.remove(bee)
			if bee in employed:
				onlooker.remove(bee)

			if bee != best_bee:
				employed.append(Bee("employed", randPosition(pic_width, pic_height)))
				scout.remove(bee)

		iteracoes += 1

	return best_bee.current_pos


def main():

	print(randPosition(20, 30))

	template = cv2.imread("template.png", cv2.IMREAD_UNCHANGED) #cv2.Canny(template, 100, 200)
	picture = cv2.imread("picture.png", cv2.IMREAD_UNCHANGED)
	h, w, _ = template.shape

	# Match Template do CV2 pra comparar
	'''
	matches = cv2.matchTemplate(picture, template, cv2.TM_CCOEFF_NORMED)
	_, max_val, _, max_loc = cv2.minMaxLoc(matches)
	color = (255, 0, 0) #blue
	picture = cv2.rectangle(picture, max_loc, (max_loc[0] + w, max_loc[1] + h), color, 2)
	'''
	match = myMatch(picture, template)
	print(match)
	# Exibe o resultado na tela
	#cv2.imshow("resultado", picture)

	# Pressione qualquer tecla para sair
	_ = cv2.waitKey(0)
	cv2.destroyAllWindows()

main()
