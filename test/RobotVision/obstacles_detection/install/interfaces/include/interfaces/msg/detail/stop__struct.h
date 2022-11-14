// generated from rosidl_generator_c/resource/idl__struct.h.em
// with input from interfaces:msg/Stop.idl
// generated code does not contain a copyright notice

#ifndef INTERFACES__MSG__DETAIL__STOP__STRUCT_H_
#define INTERFACES__MSG__DETAIL__STOP__STRUCT_H_

#ifdef __cplusplus
extern "C"
{
#endif

#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>


// Constants defined in the message

// Struct defined in msg/Stop in the package interfaces.
typedef struct interfaces__msg__Stop
{
  bool stop;
  int64_t lspeed;
  int64_t rspeed;
} interfaces__msg__Stop;

// Struct for a sequence of interfaces__msg__Stop.
typedef struct interfaces__msg__Stop__Sequence
{
  interfaces__msg__Stop * data;
  /// The number of valid items in data
  size_t size;
  /// The number of allocated items in data
  size_t capacity;
} interfaces__msg__Stop__Sequence;

#ifdef __cplusplus
}
#endif

#endif  // INTERFACES__MSG__DETAIL__STOP__STRUCT_H_
