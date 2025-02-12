# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: greeter.proto
# Protobuf Python Version: 5.29.0
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    29,
    0,
    '',
    'greeter.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\rgreeter.proto\x12\x07greeter\"1\n\x0bUserRequest\x12\x10\n\x08username\x18\x01 \x01(\t\x12\x10\n\x08password\x18\x02 \x01(\t\"D\n\x10RegisterResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x0f\n\x07message\x18\x02 \x01(\t\x12\x0e\n\x06status\x18\x03 \x01(\t\"/\n\x0c\x41uthResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x0e\n\x06status\x18\x02 \x01(\t\"%\n\x11\x44\x65leteUserRequest\x12\x10\n\x08username\x18\x01 \x01(\t\"6\n\x12\x44\x65leteUserResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x0f\n\x07message\x18\x02 \x01(\t\"\"\n\rBackupRequest\x12\x11\n\tjson_data\x18\x01 \x01(\t\"2\n\x0e\x42\x61\x63kupResponse\x12\x0f\n\x07success\x18\x01 \x01(\x08\x12\x0f\n\x07message\x18\x02 \x01(\t\"\"\n\x11HeartbeatResponse\x12\r\n\x05\x61live\x18\x01 \x01(\x08\"\x07\n\x05\x45mpty2\x81\x03\n\x07Greeter\x12;\n\x08Register\x12\x14.greeter.UserRequest\x1a\x19.greeter.RegisterResponse\x12;\n\x0c\x41uthenticate\x12\x14.greeter.UserRequest\x1a\x15.greeter.AuthResponse\x12\x45\n\nDeleteUser\x12\x1a.greeter.DeleteUserRequest\x1a\x1b.greeter.DeleteUserResponse\x12=\n\nBackupData\x12\x16.greeter.BackupRequest\x1a\x17.greeter.BackupResponse\x12<\n\x0e\x43heckHeartbeat\x12\x0e.greeter.Empty\x1a\x1a.greeter.HeartbeatResponse\x12\x38\n\rRequestBackup\x12\x0e.greeter.Empty\x1a\x17.greeter.BackupResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'greeter_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_USERREQUEST']._serialized_start=26
  _globals['_USERREQUEST']._serialized_end=75
  _globals['_REGISTERRESPONSE']._serialized_start=77
  _globals['_REGISTERRESPONSE']._serialized_end=145
  _globals['_AUTHRESPONSE']._serialized_start=147
  _globals['_AUTHRESPONSE']._serialized_end=194
  _globals['_DELETEUSERREQUEST']._serialized_start=196
  _globals['_DELETEUSERREQUEST']._serialized_end=233
  _globals['_DELETEUSERRESPONSE']._serialized_start=235
  _globals['_DELETEUSERRESPONSE']._serialized_end=289
  _globals['_BACKUPREQUEST']._serialized_start=291
  _globals['_BACKUPREQUEST']._serialized_end=325
  _globals['_BACKUPRESPONSE']._serialized_start=327
  _globals['_BACKUPRESPONSE']._serialized_end=377
  _globals['_HEARTBEATRESPONSE']._serialized_start=379
  _globals['_HEARTBEATRESPONSE']._serialized_end=413
  _globals['_EMPTY']._serialized_start=415
  _globals['_EMPTY']._serialized_end=422
  _globals['_GREETER']._serialized_start=425
  _globals['_GREETER']._serialized_end=810
# @@protoc_insertion_point(module_scope)
