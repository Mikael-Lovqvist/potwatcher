from .improved_fnmatch import translate
from pathlib import Path
import re

def translate_pattern(original_pattern):
	p = Path(original_pattern).resolve()

	if p.is_dir():	#Assume recursive if no pattern is given
		p = Path(p, '**').resolve()

	return original_pattern, re.compile(translate(str(p), True))
