from .types import symbol
from .glob import translate_pattern

from dataclasses import dataclass, field

@dataclass
class glob:
	pattern: str
	channel: symbol
	inverted: bool = False

	_translated = None

	def match(self, path):
		if not self._translated:
			self._translated = translate_pattern(self.pattern)[1]

		if match := self._translated.fullmatch(str(path)):
			if not self.inverted:
				return match
		elif self.inverted:
			raise NotImplementedError('This feature is not yet implemneted')
			#return re.fullmatch(r'.*', str(path))