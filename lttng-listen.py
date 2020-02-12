#!/usr/bin/env python3

import signal
import argparse
from cffi import FFI


class Color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


ffi = FFI()
ctl = ffi.dlopen('liblttng-ctl.so')

# endpoint.h
ffi.cdef("""
struct lttng_endpoint *lttng_session_daemon_notification_endpoint;
""")

# notification/channel.h
ffi.cdef("""

enum lttng_notification_channel_status {
	LTTNG_NOTIFICATION_CHANNEL_STATUS_NOTIFICATIONS_DROPPED = 1,
	LTTNG_NOTIFICATION_CHANNEL_STATUS_INTERRUPTED = 2,
	LTTNG_NOTIFICATION_CHANNEL_STATUS_OK = 0,
	LTTNG_NOTIFICATION_CHANNEL_STATUS_ERROR = -1,
	LTTNG_NOTIFICATION_CHANNEL_STATUS_CLOSED = -2,
	LTTNG_NOTIFICATION_CHANNEL_STATUS_ALREADY_SUBSCRIBED = -3,
	/* Condition unknown. */
	LTTNG_NOTIFICATION_CHANNEL_STATUS_UNKNOWN_CONDITION = -4,
	LTTNG_NOTIFICATION_CHANNEL_STATUS_INVALID = -5,
	LTTNG_NOTIFICATION_CHANNEL_STATUS_UNSUPPORTED_VERSION = -6,
};

struct lttng_notification_channel *lttng_notification_channel_create(
		struct lttng_endpoint *endpoint);

enum lttng_notification_channel_status
lttng_notification_channel_get_next_notification(
		struct lttng_notification_channel *channel,
		struct lttng_notification **notification);

enum lttng_notification_channel_status
lttng_notification_channel_has_pending_notification(
		struct lttng_notification_channel *channel,
		bool *notification_pending);

enum lttng_notification_channel_status
lttng_notification_channel_subscribe(
		struct lttng_notification_channel *channel,
		const struct lttng_condition *condition);

enum lttng_notification_channel_status
lttng_notification_channel_unsubscribe(
		struct lttng_notification_channel *channel,
		const struct lttng_condition *condition);

void lttng_notification_channel_destroy(
		struct lttng_notification_channel *channel);

""")

# notification/notification.h
ffi.cdef("""
const struct lttng_condition *lttng_notification_get_condition(
		struct lttng_notification *notification);

const struct lttng_evaluation *lttng_notification_get_evaluation(
		struct lttng_notification *notification);

void lttng_notification_destroy(struct lttng_notification *notification);
""")

# condition/condition.h
ffi.cdef("""
enum lttng_condition_type {
	LTTNG_CONDITION_TYPE_UNKNOWN = -1,
	LTTNG_CONDITION_TYPE_SESSION_CONSUMED_SIZE = 100,
	LTTNG_CONDITION_TYPE_BUFFER_USAGE_HIGH = 101,
	LTTNG_CONDITION_TYPE_BUFFER_USAGE_LOW = 102,
	LTTNG_CONDITION_TYPE_SESSION_ROTATION_ONGOING = 103,
	LTTNG_CONDITION_TYPE_SESSION_ROTATION_COMPLETED = 104,
};

enum lttng_condition_status {
	LTTNG_CONDITION_STATUS_OK = 0,
	LTTNG_CONDITION_STATUS_ERROR = -1,
	LTTNG_CONDITION_STATUS_UNKNOWN = -2,
	LTTNG_CONDITION_STATUS_INVALID = -3,
	LTTNG_CONDITION_STATUS_UNSET = -4,
};

enum lttng_condition_type lttng_condition_get_type(
		const struct lttng_condition *condition);

void lttng_condition_destroy(struct lttng_condition *condition);
""")

# evaluation.h
ffi.cdef("""
enum lttng_evaluation_status {
	LTTNG_EVALUATION_STATUS_OK = 0,
	LTTNG_EVALUATION_STATUS_ERROR = -1,
	LTTNG_EVALUATION_STATUS_INVALID = -2,
	LTTNG_EVALUATION_STATUS_UNKNOWN = -3,
	LTTNG_EVALUATION_STATUS_UNSET = -4,
};

enum lttng_condition_type lttng_evaluation_get_type(
		const struct lttng_evaluation *evaluation);

void lttng_evaluation_destroy(struct lttng_evaluation *evaluation);
""")

# condition/session-rotation.h
ffi.cdef("""
struct lttng_condition *
lttng_condition_session_rotation_ongoing_create(void);

struct lttng_condition *
 lttng_condition_session_rotation_completed_create(void);

enum lttng_condition_status
lttng_condition_session_rotation_get_session_name(
		const struct lttng_condition *condition,
		const char **session_name);

enum lttng_condition_status
lttng_condition_session_rotation_set_session_name(
		struct lttng_condition *condition,
		const char *session_name);

enum lttng_evaluation_status
lttng_evaluation_session_rotation_get_id(
		const struct lttng_evaluation *evaluation, uint64_t *id);

enum lttng_evaluation_status
lttng_evaluation_session_rotation_completed_get_location(
		const struct lttng_evaluation *evaluation,
		const struct lttng_trace_archive_location **location);
""")

# trigger/trigger.h
ffi.cdef("""
struct lttng_trigger *lttng_trigger_create(
		struct lttng_condition *condition, struct lttng_action *action);

struct lttng_condition *lttng_trigger_get_condition(
		struct lttng_trigger *trigger);

struct lttng_action *lttng_trigger_get_action(
		struct lttng_trigger *trigger);

void lttng_trigger_destroy(struct lttng_trigger *trigger);

int lttng_register_trigger(struct lttng_trigger *trigger);

int lttng_unregister_trigger(struct lttng_trigger *trigger);
""")

# action/action.h
ffi.cdef("""
enum lttng_action_type lttng_action_get_type(
		struct lttng_action *action);

void lttng_action_destroy(struct lttng_action *action);
""")

# action/notify.h
ffi.cdef("""
struct lttng_action *lttng_action_notify_create(void);
""")

# lttng-error.h
ffi.cdef("""
enum lttng_error_code {
	LTTNG_OK                         = 10,  /* Ok */
	LTTNG_ERR_UNK                    = 11,  /* Unknown Error */
	LTTNG_ERR_UND                    = 12,  /* Undefined command */
	LTTNG_ERR_SESSION_STARTED        = 13,  /* Session is running */
	LTTNG_ERR_UNKNOWN_DOMAIN         = 14,  /* Tracing domain not known */
	LTTNG_ERR_NOT_SUPPORTED          = 15,  /* Operation not supported */
	LTTNG_ERR_NO_SESSION             = 16,  /* No session found */
	LTTNG_ERR_CREATE_DIR_FAIL        = 17,  /* Create directory fail */
	LTTNG_ERR_SESSION_FAIL           = 18,  /* Create session fail */
	LTTNG_ERR_NO_SESSIOND            = 19,  /* No session daemon available */
	LTTNG_ERR_SET_URL                = 20,  /* Error setting URL */
	LTTNG_ERR_URL_EXIST              = 21,  /* URL already exists. */
	LTTNG_ERR_BUFFER_NOT_SUPPORTED   = 22,  /* Buffer type not supported. */
	LTTNG_ERR_SESS_NOT_FOUND         = 23,  /* Session by name not found */
	LTTNG_ERR_BUFFER_TYPE_MISMATCH   = 24,  /* Buffer type mismatched. */
	LTTNG_ERR_FATAL                  = 25,  /* Fatal error */
	LTTNG_ERR_NOMEM                  = 26,  /* Not enough memory. */
	LTTNG_ERR_SELECT_SESS            = 27,  /* Must select a session */
	LTTNG_ERR_EXIST_SESS             = 28,  /* Session name already exist */
	LTTNG_ERR_NO_EVENT               = 29,  /* No event found */
	LTTNG_ERR_CONNECT_FAIL           = 30,  /* Unable to connect to unix socket */
	LTTNG_ERR_SNAPSHOT_OUTPUT_EXIST  = 31,  /* Snapshot output already exists */
	LTTNG_ERR_EPERM                  = 32,  /* Permission denied */
	LTTNG_ERR_KERN_NA                = 33,  /* Kernel tracer unavalable */
	LTTNG_ERR_KERN_VERSION           = 34,  /* Kernel tracer not compatible */
	LTTNG_ERR_KERN_EVENT_EXIST       = 35,  /* Kernel event already exists */
	LTTNG_ERR_KERN_SESS_FAIL         = 36,  /* Kernel create session failed */
	LTTNG_ERR_KERN_CHAN_EXIST        = 37,  /* Kernel channel already exists */
	LTTNG_ERR_KERN_CHAN_FAIL         = 38,  /* Kernel create channel failed */
	LTTNG_ERR_KERN_CHAN_NOT_FOUND    = 39,  /* Kernel channel not found */
	LTTNG_ERR_KERN_CHAN_DISABLE_FAIL = 40,  /* Kernel disable channel failed */
	LTTNG_ERR_KERN_CHAN_ENABLE_FAIL  = 41,  /* Kernel enable channel failed */
	LTTNG_ERR_KERN_CONTEXT_FAIL      = 42,  /* Kernel add context failed */
	LTTNG_ERR_KERN_ENABLE_FAIL       = 43,  /* Kernel enable event failed */
	LTTNG_ERR_KERN_DISABLE_FAIL      = 44,  /* Kernel disable event failed */
	LTTNG_ERR_KERN_META_FAIL         = 45,  /* Kernel open metadata failed */
	LTTNG_ERR_KERN_START_FAIL        = 46,  /* Kernel start trace failed */
	LTTNG_ERR_KERN_STOP_FAIL         = 47,  /* Kernel stop trace failed */
	LTTNG_ERR_KERN_CONSUMER_FAIL     = 48,  /* Kernel consumer start failed */
	LTTNG_ERR_KERN_STREAM_FAIL       = 49,  /* Kernel create stream failed */
	LTTNG_ERR_START_SESSION_ONCE     = 50,  /* Session needs to be started once. */
	LTTNG_ERR_SNAPSHOT_FAIL          = 51,  /* Snapshot record failed. */
	LTTNG_ERR_NO_STREAM              = 52,  /* Index without stream on relay. */
	LTTNG_ERR_KERN_LIST_FAIL         = 53,  /* Kernel listing events failed */
	LTTNG_ERR_UST_CALIBRATE_FAIL     = 54,  /* UST calibration failed */
	LTTNG_ERR_UST_EVENT_ENABLED      = 55,  /* UST event already enabled. */
	LTTNG_ERR_UST_SESS_FAIL          = 56,  /* UST create session failed */
	LTTNG_ERR_UST_CHAN_EXIST         = 57,  /* UST channel already exist */
	LTTNG_ERR_UST_CHAN_FAIL          = 58,  /* UST create channel failed */
	LTTNG_ERR_UST_CHAN_NOT_FOUND     = 59,  /* UST channel not found */
	LTTNG_ERR_UST_CHAN_DISABLE_FAIL  = 60,  /* UST disable channel failed */
	LTTNG_ERR_UST_CHAN_ENABLE_FAIL   = 61,  /* UST enable channel failed */
	LTTNG_ERR_CHAN_EXIST             = 62,  /* Channel already exists. */
	LTTNG_ERR_UST_ENABLE_FAIL        = 63,  /* UST enable event failed */
	LTTNG_ERR_UST_DISABLE_FAIL       = 64,  /* UST disable event failed */
	LTTNG_ERR_UST_META_FAIL          = 65,  /* UST open metadata failed */
	LTTNG_ERR_UST_START_FAIL         = 66,  /* UST start trace failed */
	LTTNG_ERR_UST_STOP_FAIL          = 67,  /* UST stop trace failed */
	LTTNG_ERR_UST_CONSUMER64_FAIL    = 68,  /* 64-bit UST consumer start failed */
	LTTNG_ERR_UST_CONSUMER32_FAIL    = 69,  /* 32-bit UST consumer start failed */
	LTTNG_ERR_UST_STREAM_FAIL        = 70,  /* UST create stream failed */
	LTTNG_ERR_SNAPSHOT_NODATA        = 71,  /* No data in snapshot. */
	LTTNG_ERR_NO_CHANNEL             = 72,  /* No channel found in the session. */
	LTTNG_ERR_SESSION_INVALID_CHAR   = 73,  /* Invalid characters found in session name. */
	LTTNG_ERR_UST_LIST_FAIL          = 74,  /* UST listing events failed */
	LTTNG_ERR_UST_EVENT_EXIST        = 75,  /* UST event exist */
	LTTNG_ERR_UST_EVENT_NOT_FOUND    = 76,  /* UST event not found */
	LTTNG_ERR_UST_CONTEXT_EXIST      = 77,  /* UST context exist */
	LTTNG_ERR_UST_CONTEXT_INVAL      = 78,  /* UST context invalid */
	LTTNG_ERR_NEED_ROOT_SESSIOND     = 79,  /* root sessiond is needed */
	LTTNG_ERR_TRACE_ALREADY_STARTED  = 80,  /* Tracing already started */
	LTTNG_ERR_TRACE_ALREADY_STOPPED  = 81,  /* Tracing already stopped */
	LTTNG_ERR_KERN_EVENT_ENOSYS      = 82,  /* Kernel event type not supported */
	LTTNG_ERR_NEED_CHANNEL_NAME      = 83,	/* Non-default channel exists within session: channel name needs to be specified with '-c name' */
	LTTNG_ERR_NO_UST                 = 84,  /* LTTng-UST tracer is not supported. Please rebuild lttng-tools with lttng-ust support enabled. */
	LTTNG_ERR_SAVE_FILE_EXIST        = 85,  /* Session file already exists. */
	LTTNG_ERR_SAVE_IO_FAIL           = 86,  /* IO error while writing session configuration */
	LTTNG_ERR_LOAD_INVALID_CONFIG    = 87,  /* Invalid session configuration */
	LTTNG_ERR_LOAD_IO_FAIL           = 88,  /* IO error while reading a session configuration */
	LTTNG_ERR_LOAD_SESSION_NOENT     = 89,  /* Session file not found */
	LTTNG_ERR_MAX_SIZE_INVALID       = 90,  /* Snapshot max size is invalid. */
	LTTNG_ERR_MI_OUTPUT_TYPE         = 91,  /* Invalid MI output format */
	LTTNG_ERR_MI_IO_FAIL             = 92,  /* IO error while writing machine interface output */
	LTTNG_ERR_MI_NOT_IMPLEMENTED     = 93,  /* Mi feature not implemented */
	/* 94 */
	/* 95 */
	/* 96 */
	LTTNG_ERR_INVALID                = 97,  /* Invalid parameter */
	LTTNG_ERR_NO_USTCONSUMERD        = 98,  /* No UST consumer detected */
	LTTNG_ERR_NO_KERNCONSUMERD       = 99,  /* No Kernel consumer detected */
	LTTNG_ERR_EVENT_EXIST_LOGLEVEL   = 100, /* Event enabled with different loglevel */
	LTTNG_ERR_URL_DATA_MISS          = 101, /* Missing network data URL */
	LTTNG_ERR_URL_CTRL_MISS          = 102, /* Missing network control URL */
	LTTNG_ERR_ENABLE_CONSUMER_FAIL   = 103, /* Enabling consumer failed */
	LTTNG_ERR_RELAYD_CONNECT_FAIL    = 104, /* lttng-relayd create session failed */
	LTTNG_ERR_RELAYD_VERSION_FAIL    = 105, /* lttng-relayd not compatible */
	LTTNG_ERR_FILTER_INVAL           = 106, /* Invalid filter bytecode */
	LTTNG_ERR_FILTER_NOMEM           = 107, /* Lack of memory for filter bytecode */
	LTTNG_ERR_FILTER_EXIST           = 108, /* Filter already exist */
	LTTNG_ERR_NO_CONSUMER            = 109, /* No consumer exist for the session */
	LTTNG_ERR_EXCLUSION_INVAL        = 110, /* Invalid event exclusion data */
	LTTNG_ERR_EXCLUSION_NOMEM        = 111, /* Lack of memory while processing event exclusions */
	LTTNG_ERR_INVALID_EVENT_NAME     = 112, /* Invalid event name */
	LTTNG_ERR_INVALID_CHANNEL_NAME   = 113, /* Invalid channel name */
	LTTNG_ERR_PID_TRACKED            = 114, /* PID already tracked */
	LTTNG_ERR_PID_NOT_TRACKED        = 115, /* PID not tracked */
	LTTNG_ERR_INVALID_CHANNEL_DOMAIN = 116, /* Invalid channel domain */
	LTTNG_ERR_OVERFLOW		 = 117, /* Overflow occurred. */
	LTTNG_ERR_SESSION_NOT_STARTED    = 118, /* Session not started */
	LTTNG_ERR_LIVE_SESSION           = 119, /* Live session unsupported */
	LTTNG_ERR_PER_PID_SESSION        = 120, /* Per-PID sessions unsupported */
	LTTNG_ERR_KERN_CONTEXT_UNAVAILABLE = 121, /* Context unavailable on this kernel */
	LTTNG_ERR_REGEN_STATEDUMP_FAIL   = 122, /* Failed to regenerate the state dump */
	LTTNG_ERR_REGEN_STATEDUMP_NOMEM  = 123, /* Failed to regenerate the state dump, not enough memory */
	LTTNG_ERR_NOT_SNAPSHOT_SESSION   = 124, /* Session is not in snapshot mode. */
	LTTNG_ERR_INVALID_TRIGGER        = 125, /* Invalid trigger provided. */
	LTTNG_ERR_TRIGGER_EXISTS         = 126, /* Trigger already registered. */
	LTTNG_ERR_TRIGGER_NOT_FOUND      = 127, /* Trigger not found. */
	LTTNG_ERR_COMMAND_CANCELLED      = 128, /* Command cancelled. */
	LTTNG_ERR_ROTATION_PENDING       = 129, /* Rotate already pending for this session. */
	LTTNG_ERR_ROTATION_NOT_AVAILABLE = 130, /* Rotate feature not available for this type of session (e.g: live) */
	LTTNG_ERR_ROTATION_SCHEDULE_SET  = 131, /* Schedule type already set for this session. */
	LTTNG_ERR_ROTATION_SCHEDULE_NOT_SET = 132, /* No schedule of this type set for this session. */
	LTTNG_ERR_ROTATION_MULTIPLE_AFTER_STOP = 133, /* Already rotated once after a stop. */
	LTTNG_ERR_ROTATION_WRONG_VERSION   = 134, /* Session rotation not supported by this kernel tracer version */
	LTTNG_ERR_NO_SESSION_OUTPUT        = 135, /* Session has no output configured. */
	LTTNG_ERR_ROTATION_NOT_AVAILABLE_RELAY = 136, /* Rotate feature not available on the relay. */
	LTTNG_ERR_AGENT_TRACING_DISABLED = 137, /* Agent tracing disabled. */
	LTTNG_ERR_PROBE_LOCATION_INVAL   = 138, /* Invalid userspace probe location. */
	LTTNG_ERR_ELF_PARSING            = 139, /* ELF parsing error. */
	LTTNG_ERR_SDT_PROBE_SEMAPHORE    = 140, /* SDT probe guarded by a semaphore. */

	/* MUST be last element */
	LTTNG_ERR_NR,                           /* Last element */
};

const char *lttng_strerror(int code);
""")

# location.h
ffi.cdef("""
enum lttng_trace_archive_location_type {
	LTTNG_TRACE_ARCHIVE_LOCATION_TYPE_UNKNOWN = 0,
	LTTNG_TRACE_ARCHIVE_LOCATION_TYPE_LOCAL = 1,
	LTTNG_TRACE_ARCHIVE_LOCATION_TYPE_RELAY = 2,
};

enum lttng_trace_archive_location_status {
	LTTNG_TRACE_ARCHIVE_LOCATION_STATUS_OK = 0,
	LTTNG_TRACE_ARCHIVE_LOCATION_STATUS_INVALID = -1,
	LTTNG_TRACE_ARCHIVE_LOCATION_STATUS_ERROR = -2,
};

enum lttng_trace_archive_location_relay_protocol_type {
	LTTNG_TRACE_ARCHIVE_LOCATION_RELAY_PROTOCOL_TYPE_TCP = 0,
};

enum lttng_trace_archive_location_type
lttng_trace_archive_location_get_type(
		const struct lttng_trace_archive_location *location);

enum lttng_trace_archive_location_status
lttng_trace_archive_location_local_get_absolute_path(
		const struct lttng_trace_archive_location *location,
		const char **absolute_path);

enum lttng_trace_archive_location_status
lttng_trace_archive_location_relay_get_host(
		const struct lttng_trace_archive_location *location,
		const char **relay_host);

enum lttng_trace_archive_location_status
lttng_trace_archive_location_relay_get_control_port(
		const struct lttng_trace_archive_location *location,
		uint16_t *control_port);

enum lttng_trace_archive_location_status
lttng_trace_archive_location_relay_get_data_port(
		const struct lttng_trace_archive_location *location,
		uint16_t *data_port);

enum lttng_trace_archive_location_status
lttng_trace_archive_location_relay_get_protocol_type(
		const struct lttng_trace_archive_location *location,
		enum lttng_trace_archive_location_relay_protocol_type *protocol);

enum lttng_trace_archive_location_status
lttng_trace_archive_location_relay_get_relative_path(
		const struct lttng_trace_archive_location *location,
		const char **relative_path);
""")

should_exit = False


def signal_handler(sig, frame):
    should_exit = True


signal.signal(signal.SIGINT, signal_handler)

parser = argparse.ArgumentParser(
    description='Monitor the rotations of a set of sessions.')
parser.add_argument('sessions', metavar='s', type=str, nargs='+',
                    help='Session(s) to monitor for rotations')
args = parser.parse_args()

# Create notification channel
endpoint = ctl.lttng_session_daemon_notification_endpoint
channel = ctl.lttng_notification_channel_create(endpoint)

if channel == ffi.NULL:
    print('Unable to create notification channel... Is a sessiond running?')
    import sys
    sys.exit(-1)

# Subscribe to rotation completed conditions and create their triggers
for sessionName in args.sessions:
    rotationCompleted = ctl.lttng_condition_session_rotation_completed_create()

    bSessionName = ffi.new("char[]", bytes(sessionName, 'utf-8'))
    status = ctl.lttng_condition_session_rotation_set_session_name(
        rotationCompleted,
        bSessionName)
    if status != ctl.LTTNG_CONDITION_STATUS_OK:
        raise RuntimeError('Failed to set rotation completed condition name')

    # Register session rotation completed trigger
    notify_action = ctl.lttng_action_notify_create()
    trigger = ctl.lttng_trigger_create(
        rotationCompleted, notify_action)

    status = ctl.lttng_register_trigger(trigger)
    if status != 0 and status != -ctl.LTTNG_ERR_TRIGGER_EXISTS:
        raise RuntimeError(
            'Failed to register rotation completed trigger for session {}'.format(sessionName))

    # Subscribe to session completed notifications
    status = ctl.lttng_notification_channel_subscribe(
        channel, rotationCompleted)
    if status != ctl.LTTNG_NOTIFICATION_CHANNEL_STATUS_OK:
        raise RuntimeError(
            'Failed to subscribe to rotation completed condition')

    ctl.lttng_trigger_destroy(trigger)
    ctl.lttng_condition_destroy(rotationCompleted)
    ctl.lttng_action_destroy(notify_action)


print('Monitoring session' + ('' if len(args.sessions) == 1 else 's') + ' {} for rotations'.format(
    ', '.join([(Color.WHITE + s + Color.END) for s in args.sessions])))


while not should_exit:
    notification_p = ffi.new('struct lttng_notification **')

    status = ctl.lttng_notification_channel_get_next_notification(
        channel, notification_p)
    if status != ctl.LTTNG_NOTIFICATION_CHANNEL_STATUS_OK:
        raise RuntimeError('Failed to get next notification from channel')

    notification = notification_p[0]
    condition = ctl.lttng_notification_get_condition(notification)
    evaluation = ctl.lttng_notification_get_evaluation(notification)

    if ctl.lttng_condition_get_type(condition) != ctl.LTTNG_CONDITION_TYPE_SESSION_ROTATION_COMPLETED:
        raise RuntimeError('Unexpected condition type')

    session_name_c_str = ffi.new('char **')
    status = ctl.lttng_condition_session_rotation_get_session_name(
        condition, session_name_c_str)
    if status != ctl.LTTNG_CONDITION_STATUS_OK:
        raise RuntimeError('Failed to get session name')

    session_name = ffi.string(session_name_c_str[0]).decode('utf-8')
    location_c_str = ffi.new('char **')
    location_out_c = ffi.new('struct lttng_trace_archive_location**')
    status = ctl.lttng_evaluation_session_rotation_completed_get_location(
        evaluation, location_out_c)
    location_c = location_out_c[0]
    if ctl.lttng_trace_archive_location_get_type(location_c) == ctl.LTTNG_TRACE_ARCHIVE_LOCATION_TYPE_LOCAL:
        status = ctl.lttng_trace_archive_location_local_get_absolute_path(
            location_c, location_c_str)
        if status != ctl.LTTNG_TRACE_ARCHIVE_LOCATION_STATUS_OK:
            raise RuntimeError('Failed to get local location absolute path')
        archive_path = ffi.string(location_c_str[0]).decode('utf-8')
    else:
        raise RuntimeError('Unsupported trace achive location type')

    print('Completed trace archive chunk for session {} available at: {}'.format(
        session_name, archive_path))

    ctl.lttng_notification_destroy(notification)


# Destroy notification channel
ctl.lttng_notification_channel_destroy(channel)
