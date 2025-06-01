from dataclasses import dataclass, field
from .types import symbol, singleton_record

@singleton_record
class clear:
	pass

@singleton_record
class show_stats:
	pass

@dataclass
class cmd:
	command: str
