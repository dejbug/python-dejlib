import sys, re

IDWRD = r'[_a-zA-Z0-9]'
IDSTR = r'[_a-zA-Z0-9][-_a-zA-Z0-9]*'
SOPT = re.compile(rf'({IDWRD})' r'(:{,2})')
LOPT = re.compile(rf'({IDSTR})' r'(:{,2})')

def parseOptionsString(regex, text):
	'''
	>>> parseOptionsString(SOPT, 'ab:c:de::f')
	{'a': 0, 'b': 1, 'c': 1, 'd': 0, 'e': 2, 'f': 0}
	>>> parseOptionsString(SOPT, '  a,b:,c:!de:::::f')
	{'a': 0, 'b': 1, 'c': 1, 'd': 0, 'e': 2, 'f': 0}
	>>> parseOptionsString(LOPT, 'when:,verbosity::,version')
	{'when': 1, 'verbosity': 2, 'version': 0}
	>>> parseOptionsString(LOPT, ',,,,!!when:,,,,verbosity::!!?? -version')
	{'when': 1, 'verbosity': 2, 'version': 0}
	'''
	# TODO: Treat leading '+' and '-' specially.
	out = {}
	for m in regex.finditer(text):
		out[m.group(1)] = len(m.group(2))
	return out

def parseArg(arg):
	'''
	>>> parseArg('-a')
	(1, 'a', None)
	>>> parseArg('-b')
	(1, 'b', None)
	>>> parseArg('do it')
	'do it'
	>>> parseArg('fetch')
	'fetch'
	>>> parseArg('--when=now1')
	(2, 'when', 'now1')
	>>> parseArg('--w')
	(2, 'w', None)
	>>> parseArg('now2')
	'now2'
	>>> parseArg('--verbosity')
	(2, 'verbosity', None)
	>>> parseArg('--verbosity')
	(2, 'verbosity', None)
	>>> parseArg('3')
	'3'
	>>> parseArg('--verbosity=5')
	(2, 'verbosity', '5')
	>>> parseArg('-d')
	(1, 'd', None)
	>>> parseArg('-c=hello world')
	(1, 'c', 'hello world')
	'''
	if arg == '--': return arg
	elif not arg.startswith('-'): return arg
	m = re.match(r'(-{0,2})(' + IDSTR + ')(?:=(.*))?', arg)
	# NOTE: shlex.split will pre-unquote for us, so no need for this:
	# return len(m.group(1)), m.group(2), unquote(m.group(3))
	return len(m.group(1)), m.group(2), m.group(3)

# def unquote(text):
# 	if text:
# 		if text.startswith('"') and text.endswith('"'):
# 			return text[1:-1]
# 		if text.startswith("'") and text.endswith("'"):
# 			return text[1:-1]
# 	return text

def resolveLongOption(prefix, names):
	'''
	>>> resolveLongOption('w', ['where', 'when', 'willingly'])
	>>> resolveLongOption('wh', ['where', 'when', 'willingly'])
	>>> resolveLongOption('whe', ['where', 'when', 'willingly'])
	>>> resolveLongOption('wher', ['where', 'when', 'willingly'])
	'where'
	>>> resolveLongOption('wi', ['where', 'when', 'willingly'])
	'willingly'
	'''
	candidates = [name for name in names if name.startswith(prefix)]
	return candidates[0] if len(candidates) == 1 else None

if __name__ == '__main__':
	sopt = parseOptionsString(SOPT, 'ab:c:de::f')
	lopt = parseOptionsString(LOPT, 'when:,verbosity::,version')
	print(sopt)
	print(lopt)

	args = sys.argv[1:]
	for arg in args:
		parg = parseArg(arg)
		print(f'{arg:>10} : {parg}')
