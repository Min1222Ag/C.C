# generated from rosidl_generator_py/resource/_idl.py.em
# with input from interfaces:msg/Stop.idl
# generated code does not contain a copyright notice


# Import statements for member types

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_Stop(type):
    """Metaclass of message 'Stop'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
    }

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('interfaces')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'interfaces.msg.Stop')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__msg__stop
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__msg__stop
            cls._CONVERT_TO_PY = module.convert_to_py_msg__msg__stop
            cls._TYPE_SUPPORT = module.type_support_msg__msg__stop
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__msg__stop

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class Stop(metaclass=Metaclass_Stop):
    """Message class 'Stop'."""

    __slots__ = [
        '_stop',
        '_lspeed',
        '_rspeed',
    ]

    _fields_and_field_types = {
        'stop': 'boolean',
        'lspeed': 'boolean',
        'rspeed': 'boolean',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.stop = kwargs.get('stop', bool())
        self.lspeed = kwargs.get('lspeed', bool())
        self.rspeed = kwargs.get('rspeed', bool())

    def __repr__(self):
        typename = self.__class__.__module__.split('.')
        typename.pop()
        typename.append(self.__class__.__name__)
        args = []
        for s, t in zip(self.__slots__, self.SLOT_TYPES):
            field = getattr(self, s)
            fieldstr = repr(field)
            # We use Python array type for fields that can be directly stored
            # in them, and "normal" sequences for everything else.  If it is
            # a type that we store in an array, strip off the 'array' portion.
            if (
                isinstance(t, rosidl_parser.definition.AbstractSequence) and
                isinstance(t.value_type, rosidl_parser.definition.BasicType) and
                t.value_type.typename in ['float', 'double', 'int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64']
            ):
                if len(field) == 0:
                    fieldstr = '[]'
                else:
                    assert fieldstr.startswith('array(')
                    prefix = "array('X', "
                    suffix = ')'
                    fieldstr = fieldstr[len(prefix):-len(suffix)]
            args.append(s[1:] + '=' + fieldstr)
        return '%s(%s)' % ('.'.join(typename), ', '.join(args))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.stop != other.stop:
            return False
        if self.lspeed != other.lspeed:
            return False
        if self.rspeed != other.rspeed:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @property
    def stop(self):
        """Message field 'stop'."""
        return self._stop

    @stop.setter
    def stop(self, value):
        if __debug__:
            assert \
                isinstance(value, bool), \
                "The 'stop' field must be of type 'bool'"
        self._stop = value

    @property
    def lspeed(self):
        """Message field 'lspeed'."""
        return self._lspeed

    @lspeed.setter
    def lspeed(self, value):
        if __debug__:
            assert \
                isinstance(value, bool), \
                "The 'lspeed' field must be of type 'bool'"
        self._lspeed = value

    @property
    def rspeed(self):
        """Message field 'rspeed'."""
        return self._rspeed

    @rspeed.setter
    def rspeed(self, value):
        if __debug__:
            assert \
                isinstance(value, bool), \
                "The 'rspeed' field must be of type 'bool'"
        self._rspeed = value
