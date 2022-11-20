import numpy as np
import cv2

def main():

	template = cv2.imread("template.png", cv2.IMREAD_GRAYSCALE) #cv2.Canny(template, 100, 200)
	picture = cv2.imread("picture.png", cv2.IMREAD_UNCHANGED)

	# Implementar ABC para substituir funcao abaixo!
	matches = cv2.matchTemplate(picture, template, cv2.TM_CCORR_NORMED)
	_, max_val, _, max_loc = cv2.minMaxLoc(matches)
	if max_val > 0.4:
		color = (255, 0, 0) #blue
		picture = cv2.rectangle(picture, max_loc[0], max_loc[1], color, 2)

	# Exibe o resultado na tela
	cv2.imshow("resultado", picture)

	# Pressione qualquer tecla para sair
	_ = cv2.waitKey(0)
	cv2.destroyAllWindows()

main()
