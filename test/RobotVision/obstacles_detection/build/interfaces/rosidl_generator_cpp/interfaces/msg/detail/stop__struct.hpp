// generated from rosidl_generator_cpp/resource/idl__struct.hpp.em
// with input from interfaces:msg/Stop.idl
// generated code does not contain a copyright notice

#ifndef INTERFACES__MSG__DETAIL__STOP__STRUCT_HPP_
#define INTERFACES__MSG__DETAIL__STOP__STRUCT_HPP_

#include <rosidl_runtime_cpp/bounded_vector.hpp>
#include <rosidl_runtime_cpp/message_initialization.hpp>
#include <algorithm>
#include <array>
#include <memory>
#include <string>
#include <vector>


#ifndef _WIN32
# define DEPRECATED__interfaces__msg__Stop __attribute__((deprecated))
#else
# define DEPRECATED__interfaces__msg__Stop __declspec(deprecated)
#endif

namespace interfaces
{

namespace msg
{

// message struct
template<class ContainerAllocator>
struct Stop_
{
  using Type = Stop_<ContainerAllocator>;

  explicit Stop_(rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->stop = false;
      this->lspeed = 0ll;
      this->rspeed = 0ll;
    }
  }

  explicit Stop_(const ContainerAllocator & _alloc, rosidl_runtime_cpp::MessageInitialization _init = rosidl_runtime_cpp::MessageInitialization::ALL)
  {
    (void)_alloc;
    if (rosidl_runtime_cpp::MessageInitialization::ALL == _init ||
      rosidl_runtime_cpp::MessageInitialization::ZERO == _init)
    {
      this->stop = false;
      this->lspeed = 0ll;
      this->rspeed = 0ll;
    }
  }

  // field types and members
  using _stop_type =
    bool;
  _stop_type stop;
  using _lspeed_type =
    int64_t;
  _lspeed_type lspeed;
  using _rspeed_type =
    int64_t;
  _rspeed_type rspeed;

  // setters for named parameter idiom
  Type & set__stop(
    const bool & _arg)
  {
    this->stop = _arg;
    return *this;
  }
  Type & set__lspeed(
    const int64_t & _arg)
  {
    this->lspeed = _arg;
    return *this;
  }
  Type & set__rspeed(
    const int64_t & _arg)
  {
    this->rspeed = _arg;
    return *this;
  }

  // constant declarations

  // pointer types
  using RawPtr =
    interfaces::msg::Stop_<ContainerAllocator> *;
  using ConstRawPtr =
    const interfaces::msg::Stop_<ContainerAllocator> *;
  using SharedPtr =
    std::shared_ptr<interfaces::msg::Stop_<ContainerAllocator>>;
  using ConstSharedPtr =
    std::shared_ptr<interfaces::msg::Stop_<ContainerAllocator> const>;

  template<typename Deleter = std::default_delete<
      interfaces::msg::Stop_<ContainerAllocator>>>
  using UniquePtrWithDeleter =
    std::unique_ptr<interfaces::msg::Stop_<ContainerAllocator>, Deleter>;

  using UniquePtr = UniquePtrWithDeleter<>;

  template<typename Deleter = std::default_delete<
      interfaces::msg::Stop_<ContainerAllocator>>>
  using ConstUniquePtrWithDeleter =
    std::unique_ptr<interfaces::msg::Stop_<ContainerAllocator> const, Deleter>;
  using ConstUniquePtr = ConstUniquePtrWithDeleter<>;

  using WeakPtr =
    std::weak_ptr<interfaces::msg::Stop_<ContainerAllocator>>;
  using ConstWeakPtr =
    std::weak_ptr<interfaces::msg::Stop_<ContainerAllocator> const>;

  // pointer types similar to ROS 1, use SharedPtr / ConstSharedPtr instead
  // NOTE: Can't use 'using' here because GNU C++ can't parse attributes properly
  typedef DEPRECATED__interfaces__msg__Stop
    std::shared_ptr<interfaces::msg::Stop_<ContainerAllocator>>
    Ptr;
  typedef DEPRECATED__interfaces__msg__Stop
    std::shared_ptr<interfaces::msg::Stop_<ContainerAllocator> const>
    ConstPtr;

  // comparison operators
  bool operator==(const Stop_ & other) const
  {
    if (this->stop != other.stop) {
      return false;
    }
    if (this->lspeed != other.lspeed) {
      return false;
    }
    if (this->rspeed != other.rspeed) {
      return false;
    }
    return true;
  }
  bool operator!=(const Stop_ & other) const
  {
    return !this->operator==(other);
  }
};  // struct Stop_

// alias to use template instance with default allocator
using Stop =
  interfaces::msg::Stop_<std::allocator<void>>;

// constant definitions

}  // namespace msg

}  // namespace interfaces

#endif  // INTERFACES__MSG__DETAIL__STOP__STRUCT_HPP_
