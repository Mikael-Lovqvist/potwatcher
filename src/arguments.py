from .arguments_support import Push_Token
from . import defaults as D
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from argcomplete import autocomplete
from collections import namedtuple
from pathlib import Path

Arg_Switch = namedtuple('Arg_Switch', 'key'.split())
Arg_Option = namedtuple('Arg_Option', 'key value'.split())


def interpret_arguments(arguments):
	result = list()
	push_setting = Push_Token(Arg_Option, result)
	push_switch = Push_Token(Arg_Switch, result)
	parser = ArgumentParser(
		description='Hot reload utility configuration',
		formatter_class=RawDescriptionHelpFormatter,

		epilog=(
			'Glob patterns\n'
			'  *\tMatches all files in the immediate directory\n'
			'  **\tMatches all files in this directoriy and any child directories\n'
			'\n'
			'Application function\n'
			'  The application first looks for LOCAL_CONFIG and if present loads the selected PROFILE or the default one.\n'
			'  Then it connects to the socket at EVENT_PATH where it currently creates a promiscious subscription and locally filters for file update events.\n'
			'  Once a file update event is detected, all include/exclude patterns are run in order of definition and this might trigger the hot- or support event channel.\n'
			'\n'
			'  Event channels\n'
			'    hot\t\tSet HOT_FILE and HOT_PATTERN, and HOT_INVERTED to file and pattern that matched and then run the trigger.\n'
			'    support\tSet SUPPORT_FILE and SUPPORT_PATTERN, SUPPORT_INVERTED to file and pattern that matched and then run the trigger if also HOT_FILE is set.\n'
			'\n'
			'    Note: You can preset HOT_FILE using DEFAULT_HOT_FILE.\n'
			'\n'
			'  Trigger\n'
			'    Once the trigger occurs all actions are run in definition order\n'
			'\n'
			'    Example: --clear --cmd \'my_command $HOT_FILE\' --show-stats\n'
			'      When triggered the screen will clear and my_command will be called with $HOT_FILE as its sole argument, then some runstats will be displayed\n'
		)
	)

	def Define_Option(*pos, **named):
		named.update(dict(
			action = push_setting,
			nargs = 1,
		))
		parser.add_argument(*pos, **named)

	def Define_Switch(*pos, **named):
		named.update(dict(
			action = push_switch,
			nargs = 0,
		))
		parser.add_argument(*pos, **named)


	Define_Option('--include-hot-glob', 		help='Glob for hot files')

	Define_Option('--exclude-hot-glob', 		help='Glob to exclude from hot files')
	Define_Option('--include-support-glob', 	help='Glob for support files')
	Define_Option('--exclude-support-glob', 	help='Glob to exclude from support files')
	Define_Option('--default-hot-file', 		help='Path to default hot file')
	Define_Option('--profile', 					help='Profile name to use or modify, if no profile is chosen, operate on default profile')

	Define_Option('--local-config',			 	help=f'Set local config file, defaults to "{D.LOCAL_CONFIG_PATH}"',
													type=Path, default=D.LOCAL_CONFIG_PATH)

	Define_Switch('--save', 					help='Immediate action: Save current configuration to profile')

	Define_Option('--cmd', 						help='Trigger Action: Run command')
	Define_Switch('--clear', 					help='Trigger action: Clear terminal')

	Define_Switch('--show-stats', 				help='Post trigger action: Show timing and stats after command')



	Define_Option('--event-path', 				help=f'Path to UNIX socket for the event stream. Defaults to "{D.MSG_PATH}"',
													type=Path, default=D.MSG_PATH)
	Define_Option('--environment', 				help=f'Sets FRESH or INHERITED environment for sub process. Defaults to "{D.ENVIRONMENT.name}"',
													default=D.ENVIRONMENT)
	Define_Option('--max-message-size', 		help=f'Sets maximum message size. Defaults to {D.MAX_MESSAGE_SIZE}',
													type=int, default=D.MAX_MESSAGE_SIZE)


	autocomplete(parser)
	parser.parse_args(arguments)
	return result