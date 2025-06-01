#!/bin/env python
# PYTHON_ARGCOMPLETE_OK

#TODO - figure out how to package this, especially so argcomplete works

#TODO - not all features implemented yet

from . import rules as R, actions as A
from .arguments import interpret_arguments, Arg_Option, Arg_Switch
from .defaults import config
from .types import HOT, SUPPORT, INHERITED, FRESH

from pathlib import Path
import sys, os, socket, pickle, time, subprocess

arguments = interpret_arguments(sys.argv[1:] or ['--help'])	#Default to --help

#Prepare configuration
for arg in arguments:
	match arg:
		case Arg_Option(key='include_hot_glob', value=value):
			config.rules.append(R.glob(value, HOT, False))

		case Arg_Option(key='include_support_glob', value=value):
			config.rules.append(R.glob(value, SUPPORT, False))

		case Arg_Option(key='cmd', value=value):
			config.trigger_action.append(A.cmd(value))

		case Arg_Switch(key='show_stats'):
			config.trigger_action.append(A.show_stats)

		case Arg_Switch(key='clear'):
			config.trigger_action.append(A.clear)

		case other:
			raise NotImplementedError(f'The argument option "{other.key}" has not yet been implemented')



#Prepare environment
match config.environment:
	case value if value is INHERITED:
		env = os.environ.copy()
	case value if value is FRESH:
		env = dict()
	case other:
		raise ValueError(f'No such environment: {other!r}')


#Tidy enviroment
for key in ('HOT_FILE', 'HOT_PATTERN', 'HOT_INVERTED', 'SUPPORT_FILE', 'SUPPORT_PATTERN', 'SUPPORT_INVERTED'):
	env.pop(key, None)



def trigger_action():

	times = list()

	for action in config.trigger_action:
		match action:
			case action if action is A.clear:
				print(end='\x1b[H\x1b[2J\x1b[3J')

			case action if action is A.show_stats:
				print(times)

			case A.cmd(command):
				start_time = time.monotonic()
				print(command)
				subprocess.run((command,), shell=True, env=env)
				end_time = time.monotonic()
				delta_time = end_time - start_time
				times.append((action, delta_time))

			case other:
				raise NotImplementedError(f'Action not implemented: {other}')


#Make connection - handle events
with socket.socket(socket.AF_UNIX, socket.SOCK_SEQPACKET) as s:
	s.connect(bytes(config.event_path))

	msg = ('subscribe', None)
	s.sendmsg([pickle.dumps(msg)])

	while True:
		data, ancdata, flags, addr = s.recvmsg(config.max_message_size)
		msg_type, msg_data = pickle.loads(data)

		if msg_type == 'file_updated':
			filename = Path(msg_data)

			for rule in config.rules:
				if filename_match := rule.match(filename):
					match rule.channel:
						#TODO - add more drysoot
						case channel if channel is SUPPORT:
							env.update(
								SUPPORT_FILE = filename,
								SUPPORT_PATTERN = rule.pattern,
								SUPPORT_INVERTED = str(int(rule.inverted)),
							)

							if env.get('HOT_FILE'):
								trigger_action()

						case channel if channel is HOT:
							env.update(
								HOT_FILE = filename,
								HOT_PATTERN = rule.pattern,
								HOT_INVERTED = str(int(rule.inverted)),
							)

							if env.get('HOT_FILE'):
								trigger_action()

						case other:
							raise ValueError(f'Unknown channel: {other}')

					#print(rule.channel.name, filename)
					break