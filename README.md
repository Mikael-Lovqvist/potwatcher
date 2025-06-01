```text
usage: potwatcher [-h] [--include-hot-glob INCLUDE_HOT_GLOB] [--exclude-hot-glob EXCLUDE_HOT_GLOB] [--include-support-glob INCLUDE_SUPPORT_GLOB] [--exclude-support-glob EXCLUDE_SUPPORT_GLOB] [--default-hot-file DEFAULT_HOT_FILE] [--profile PROFILE]
                   [--local-config LOCAL_CONFIG] [--save] [--cmd CMD] [--clear] [--show-stats] [--event-path EVENT_PATH] [--environment ENVIRONMENT] [--max-message-size MAX_MESSAGE_SIZE]

Hot reload utility configuration

options:
  -h, --help            show this help message and exit
  --include-hot-glob INCLUDE_HOT_GLOB
                        Glob for hot files
  --exclude-hot-glob EXCLUDE_HOT_GLOB
                        Glob to exclude from hot files
  --include-support-glob INCLUDE_SUPPORT_GLOB
                        Glob for support files
  --exclude-support-glob EXCLUDE_SUPPORT_GLOB
                        Glob to exclude from support files
  --default-hot-file DEFAULT_HOT_FILE
                        Path to default hot file
  --profile PROFILE     Profile name to use or modify, if no profile is chosen, operate on default profile
  --local-config LOCAL_CONFIG
                        Set local config file, defaults to ".potwatcher"
  --save                Immediate action: Save current configuration to profile
  --cmd CMD             Trigger Action: Run command
  --clear               Trigger action: Clear terminal
  --show-stats          Post trigger action: Show timing and stats after command
  --event-path EVENT_PATH
                        Path to UNIX socket for the event stream. Defaults to "/tmp/msg.sock"
  --environment ENVIRONMENT
                        Sets FRESH or INHERITED environment for sub process. Defaults to "INHERITED"
  --max-message-size MAX_MESSAGE_SIZE
                        Sets maximum message size. Defaults to 4096

Glob patterns
  *     Matches all files in the immediate directory
  **    Matches all files in this directoriy and any child directories

Application function
  The application first looks for LOCAL_CONFIG and if present loads the selected PROFILE or the default one.
  Then it connects to the socket at EVENT_PATH where it currently creates a promiscious subscription and locally filters for file update events.
  Once a file update event is detected, all include/exclude patterns are run in order of definition and this might trigger the hot- or support event channel.

  Event channels
    hot         Set HOT_FILE and HOT_PATTERN, and HOT_INVERTED to file and pattern that matched and then run the trigger.
    support     Set SUPPORT_FILE and SUPPORT_PATTERN, SUPPORT_INVERTED to file and pattern that matched and then run the trigger if also HOT_FILE is set.

    Note: You can preset HOT_FILE using DEFAULT_HOT_FILE.

  Trigger
    Once the trigger occurs all actions are run in definition order

    Example: --clear --cmd 'my_command $HOT_FILE' --show-stats
      When triggered the screen will clear and my_command will be called with $HOT_FILE as its sole argument, then some runstats will be displayed
```
