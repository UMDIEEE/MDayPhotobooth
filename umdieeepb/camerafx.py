def camera_effect(camera, effect):
		
		n = effect.lower()
		
		if n == 'negative':
			camera.image_effect = 'negative'
		elif n == 'sketch':
			camera.image_effect = 'sketch'
		elif n == 'colorswap':
			camera.image_effect = 'colorswap'
		elif n == 'cartoon':
			camera.image_effect = 'cartoon'
		elif n == 'oilpaint':
			camera.image_effect = 'oilpaint'
		elif n == 'emboss':
			camera.image_effect = 'emboss'
		else:
			camera.image_effect = 'none'
			
