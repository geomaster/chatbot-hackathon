from forum import search

questions = [
	'kakve telefone imate za 1din',
	'roming planovi za grcku sta imate',
	'besplatan internet za facebook',
	'kako da podesim 4g',
	'kako da kupim novi telefon kad obnavljam ugovor']

for q in questions:
	p = search(q)
	print('\n\n\nQUESTION:\n', q)
	if p == None:
		print('\n\n NOTHING FOUND ON FORUM!')
		continue
	print('\n\nMATCHED QUESTION:\n', p['q'])
	print('\n\nANSWER: ', p['a'])

