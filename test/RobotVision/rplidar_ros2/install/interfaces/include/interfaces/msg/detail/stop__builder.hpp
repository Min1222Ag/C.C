// generated from rosidl_generator_cpp/resource/idl__builder.hpp.em
// with input from interfaces:msg/Stop.idl
// generated code does not contain a copyright notice

#ifndef INTERFACES__MSG__DETAIL__STOP__BUILDER_HPP_
#define INTERFACES__MSG__DETAIL__STOP__BUILDER_HPP_

#include "interfaces/msg/detail/stop__struct.hpp"
#include <rosidl_runtime_cpp/message_initialization.hpp>
#include <algorithm>
#include <utility>


namespace interfaces
{

namespace msg
{

namespace builder
{

class Init_Stop_stop
{
public:
  Init_Stop_stop()
  : msg_(::rosidl_runtime_cpp::MessageInitialization::SKIP)
  {}
  ::interfaces::msg::Stop stop(::interfaces::msg::Stop::_stop_type arg)
  {
    msg_.stop = std::move(arg);
    return std::move(msg_);
  }

private:
  ::interfaces::msg::Stop msg_;
};

}  // namespace builder

}  // namespace msg

template<typename MessageType>
auto build();

template<>
inline
auto build<::interfaces::msg::Stop>()
{
  return interfaces::msg::builder::Init_Stop_stop();
}

}  // namespace interfaces

#endif  // INTERFACES__MSG__DETAIL__STOP__BUILDER_HPP_
