// Generated by gencpp from file learn/vision.msg
// DO NOT EDIT!


#ifndef LEARN_MESSAGE_VISION_H
#define LEARN_MESSAGE_VISION_H


#include <string>
#include <vector>
#include <map>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>


namespace learn
{
template <class ContainerAllocator>
struct vision_
{
  typedef vision_<ContainerAllocator> Type;

  vision_()
    : x()
    , y()  {
      x.assign(0.0);

      y.assign(0.0);
  }
  vision_(const ContainerAllocator& _alloc)
    : x()
    , y()  {
  (void)_alloc;
      x.assign(0.0);

      y.assign(0.0);
  }



   typedef boost::array<float, 6>  _x_type;
  _x_type x;

   typedef boost::array<float, 6>  _y_type;
  _y_type y;





  typedef boost::shared_ptr< ::learn::vision_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::learn::vision_<ContainerAllocator> const> ConstPtr;

}; // struct vision_

typedef ::learn::vision_<std::allocator<void> > vision;

typedef boost::shared_ptr< ::learn::vision > visionPtr;
typedef boost::shared_ptr< ::learn::vision const> visionConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::learn::vision_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::learn::vision_<ContainerAllocator> >::stream(s, "", v);
return s;
}


template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator==(const ::learn::vision_<ContainerAllocator1> & lhs, const ::learn::vision_<ContainerAllocator2> & rhs)
{
  return lhs.x == rhs.x &&
    lhs.y == rhs.y;
}

template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator!=(const ::learn::vision_<ContainerAllocator1> & lhs, const ::learn::vision_<ContainerAllocator2> & rhs)
{
  return !(lhs == rhs);
}


} // namespace learn

namespace ros
{
namespace message_traits
{





template <class ContainerAllocator>
struct IsFixedSize< ::learn::vision_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::learn::vision_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::learn::vision_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::learn::vision_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::learn::vision_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::learn::vision_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::learn::vision_<ContainerAllocator> >
{
  static const char* value()
  {
    return "d75c2d0ec0230fe2d3e3aa96f78888c9";
  }

  static const char* value(const ::learn::vision_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0xd75c2d0ec0230fe2ULL;
  static const uint64_t static_value2 = 0xd3e3aa96f78888c9ULL;
};

template<class ContainerAllocator>
struct DataType< ::learn::vision_<ContainerAllocator> >
{
  static const char* value()
  {
    return "learn/vision";
  }

  static const char* value(const ::learn::vision_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::learn::vision_<ContainerAllocator> >
{
  static const char* value()
  {
    return "float32[6] x\n"
"float32[6] y\n"
;
  }

  static const char* value(const ::learn::vision_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::learn::vision_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.x);
      stream.next(m.y);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct vision_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::learn::vision_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::learn::vision_<ContainerAllocator>& v)
  {
    s << indent << "x[]" << std::endl;
    for (size_t i = 0; i < v.x.size(); ++i)
    {
      s << indent << "  x[" << i << "]: ";
      Printer<float>::stream(s, indent + "  ", v.x[i]);
    }
    s << indent << "y[]" << std::endl;
    for (size_t i = 0; i < v.y.size(); ++i)
    {
      s << indent << "  y[" << i << "]: ";
      Printer<float>::stream(s, indent + "  ", v.y[i]);
    }
  }
};

} // namespace message_operations
} // namespace ros

#endif // LEARN_MESSAGE_VISION_H