from apiai_pcr import get_intent

tests = dict()
tests["Koje telefone imate?"] = 'devices'
tests["Treba mi internet za telefon?"] = 'internet'
tests["Kakve su cene roming u Crnoj Gori?"] = 'roaming'
tests["Koje pakate imate?"] = 'packages'
tests["Gde da platim racun?"] = 'bills'
tests["Koje servise nudite?"] = 'services'
tests["da"] = 'yes'
tests["ne"] = 'no'

for key in tests:
	r = get_intent(key)
	print(r == tests[key], key, r)