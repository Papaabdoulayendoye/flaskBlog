'''
	import secrets
	import os
	a = secrets.token_hex(17) # donne une nouvelle valeur au hasard de 17 mais en HEXDECIMALE
	b = os.urandom(17)
	print(f"a =>{a}")
	print(f"b =>{b}")
	posts = [
		{
			'author':'Corey Schafer',
			'title':'Blog Post 1',
			'content':'First Post content',
			'date_posted': 'April 20, 2018'
		},
		{
			'author':'Jane Doe',
			'title':'Blog Post 2',
			'content':'second Post content',
			'date_posted': 'October 2, 2016'
		}
	]
	from flask_bcrypt import Bcrypt
	bcrypt = Bcrypt()
	x = "HelloWorld"

	c = bcrypt.generate_password_hash(x)
	print(f"C => {c}")
	d = bcrypt.check_password_hash(c,x)
	print(f"d is => {d}")
'''


# a = "SASAworld"
# print(a)
# # print(a.lower())
# print(a.casefold())
# b = 'sasa xorld'
# print(b)
# print(b.replace(" ", ""))



# count = 0
# def increment():
# 	global count 
# 	count += 1 

# print(count)
# increment()
# print(count)

'''
La fonction os.path.splitext() est une fonction de la bibliothèque os de Python qui permet de séparer le nom d'un fichier et son extension.

La fonction prend en entrée une chaîne de caractères représentant le chemin complet d'un fichier et retourne un tuple contenant deux éléments : le nom de fichier sans extension et l'extension du fichier.

Voici un exemple d'utilisation de la fonction os.path.splitext() :
'''


# filename = "mon_fichier.txt"
# name, extension = os.path.splitext(filename)

# print("Nom de fichier : ", name)
# print("Extension de fichier : ", extension)
import os

# print(os.environ.get('MAIL_USERNAME'))
# print(os.environ.get('MAIL_PASSWORD'))

a = 'Papa Abdoulaye Pipo @gmail.com'
print(a)
print("a.replace(' ', '') => ",a.replace(' ', ''))
print("a.casefold() => ",a.casefold())
print("a.lower() => ",a.lower())
print("a.replace(' ', '').casefold() => ",a.replace(' ', '').casefold())
