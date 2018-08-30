import uuid as uuid_package
from sqlalchemy.dialects.postgresql import UUID as PG_UUID, ENUM
from sqlalchemy import TypeDecorator, CHAR


class GUID(TypeDecorator):
    impl = CHAR

    def load_dialect_impl(self, dialect):
        if dialect.name == 'postgresql':
            return dialect.type_descriptor(PG_UUID())
        else:
            return dialect.type_descriptor(CHAR(50))

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        elif dialect.name == 'postgresql':
            return str(value)
        else:
            if not isinstance(value, uuid_package.UUID):
                return "%.32x" % uuid_package.UUID(value)
            else:
                # hexstring
                return "%.32x" % value

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        else:
            return uuid_package.UUID(value)


def create_enum_types(enum_spec_dict, bind):
    enums_dict = {}
    for name, values in enum_spec_dict.items():
        enum_type = ENUM(*values, create_type=False,
                         name=name)

        enums_dict[name] = enum_type

        enum_type.create(bind, checkfirst=False)

    return enums_dict


def drop_enum_types(enum_spec_dict, bind):
    for name, values in enum_spec_dict.items():
        ENUM(name=name).drop(bind, checkfirst=False)
