from dataclasses import dataclass, field

@dataclass(frozen=True)
class symbol:
	name: str

def singleton_record(cls):
	return dataclass(cls)()

SUPPORT =	symbol('SUPPORT')
HOT =		symbol('HOT')

INHERITED =	symbol('INHERITED')
FRESH =		symbol('FRESH')
