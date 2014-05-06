from sys import argv
from mongoengine import *
from mongoengine.context_managers import switch_db

for post in argv[1:]:
	with switch_db(OriginalPost, argv[0]) as OriginalPost:
		if int(post) in OriginalPost.objects().post_id:
			OriginalPost(post_id=int(post)[0].delete()
	with switch_db(ReplyPost, argv)
	elif int(post) if ReplyPost.objects().post_id:
		ReplyPost(post_id=int(post))[0].delete()
	else:
		print("There isn't post with ID {0}".format(post))

if __name__ == '__main__':
	main()