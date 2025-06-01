from pathlib import Path
from .types import symbol, singleton_record, INHERITED
from dataclasses import dataclass, field


LOCAL_CONFIG_PATH = 	Path('.potwatcher')
MSG_PATH = 				Path('/tmp/msg.sock')
ENVIRONMENT = 			INHERITED
MAX_MESSAGE_SIZE = 		4096


@singleton_record
class config:
	rules: 				list = 		field(default_factory=list)
	trigger_action: 	list = 		field(default_factory=list)
	event_path:			Path =		MSG_PATH
	local_config_file:	Path =		LOCAL_CONFIG_PATH
	environment:		symbol = 	ENVIRONMENT
	max_message_size:	int = 		MAX_MESSAGE_SIZE
