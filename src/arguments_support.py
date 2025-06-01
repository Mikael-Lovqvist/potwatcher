from argparse import Action

class Push_Token:
	class _Action(Action):
		def __init__(self, token_pusher, *pos, **named):
			super().__init__(*pos, **named)
			self.token_pusher = token_pusher

		def __call__(self, parser, namespace, values, option_string=None):
			self.token_pusher.push(self.dest, *values)

	def __init__(self, token, target):
		self.token = token
		self.target = target

	def push(self, *pos):
		self.target.append(self.token(*pos))

	def __call__(self, *pos, **named):
		return self._Action(self, *pos, **named)
