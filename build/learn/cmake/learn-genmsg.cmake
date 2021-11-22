# generated from genmsg/cmake/pkg-genmsg.cmake.em

message(STATUS "learn: 4 messages, 0 services")

set(MSG_I_FLAGS "-Ilearn:/home/jichanun/catin_ws/src/learn/msg;-Istd_msgs:/opt/ros/melodic/share/std_msgs/cmake/../msg")

# Find all generators
find_package(gencpp REQUIRED)
find_package(geneus REQUIRED)
find_package(genlisp REQUIRED)
find_package(gennodejs REQUIRED)
find_package(genpy REQUIRED)

add_custom_target(learn_generate_messages ALL)

# verify that message/service dependencies have not changed since configure



get_filename_component(_filename "/home/jichanun/catin_ws/src/learn/msg/expectp.msg" NAME_WE)
add_custom_target(_learn_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "learn" "/home/jichanun/catin_ws/src/learn/msg/expectp.msg" ""
)

get_filename_component(_filename "/home/jichanun/catin_ws/src/learn/msg/Person.msg" NAME_WE)
add_custom_target(_learn_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "learn" "/home/jichanun/catin_ws/src/learn/msg/Person.msg" ""
)

get_filename_component(_filename "/home/jichanun/catin_ws/src/learn/msg/vision.msg" NAME_WE)
add_custom_target(_learn_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "learn" "/home/jichanun/catin_ws/src/learn/msg/vision.msg" ""
)

get_filename_component(_filename "/home/jichanun/catin_ws/src/learn/msg/earphone.msg" NAME_WE)
add_custom_target(_learn_generate_messages_check_deps_${_filename}
  COMMAND ${CATKIN_ENV} ${PYTHON_EXECUTABLE} ${GENMSG_CHECK_DEPS_SCRIPT} "learn" "/home/jichanun/catin_ws/src/learn/msg/earphone.msg" ""
)

#
#  langs = gencpp;geneus;genlisp;gennodejs;genpy
#

### Section generating for lang: gencpp
### Generating Messages
_generate_msg_cpp(learn
  "/home/jichanun/catin_ws/src/learn/msg/expectp.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/learn
)
_generate_msg_cpp(learn
  "/home/jichanun/catin_ws/src/learn/msg/Person.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/learn
)
_generate_msg_cpp(learn
  "/home/jichanun/catin_ws/src/learn/msg/vision.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/learn
)
_generate_msg_cpp(learn
  "/home/jichanun/catin_ws/src/learn/msg/earphone.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/learn
)

### Generating Services

### Generating Module File
_generate_module_cpp(learn
  ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/learn
  "${ALL_GEN_OUTPUT_FILES_cpp}"
)

add_custom_target(learn_generate_messages_cpp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_cpp}
)
add_dependencies(learn_generate_messages learn_generate_messages_cpp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/jichanun/catin_ws/src/learn/msg/expectp.msg" NAME_WE)
add_dependencies(learn_generate_messages_cpp _learn_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/jichanun/catin_ws/src/learn/msg/Person.msg" NAME_WE)
add_dependencies(learn_generate_messages_cpp _learn_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/jichanun/catin_ws/src/learn/msg/vision.msg" NAME_WE)
add_dependencies(learn_generate_messages_cpp _learn_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/jichanun/catin_ws/src/learn/msg/earphone.msg" NAME_WE)
add_dependencies(learn_generate_messages_cpp _learn_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(learn_gencpp)
add_dependencies(learn_gencpp learn_generate_messages_cpp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS learn_generate_messages_cpp)

### Section generating for lang: geneus
### Generating Messages
_generate_msg_eus(learn
  "/home/jichanun/catin_ws/src/learn/msg/expectp.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/learn
)
_generate_msg_eus(learn
  "/home/jichanun/catin_ws/src/learn/msg/Person.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/learn
)
_generate_msg_eus(learn
  "/home/jichanun/catin_ws/src/learn/msg/vision.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/learn
)
_generate_msg_eus(learn
  "/home/jichanun/catin_ws/src/learn/msg/earphone.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/learn
)

### Generating Services

### Generating Module File
_generate_module_eus(learn
  ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/learn
  "${ALL_GEN_OUTPUT_FILES_eus}"
)

add_custom_target(learn_generate_messages_eus
  DEPENDS ${ALL_GEN_OUTPUT_FILES_eus}
)
add_dependencies(learn_generate_messages learn_generate_messages_eus)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/jichanun/catin_ws/src/learn/msg/expectp.msg" NAME_WE)
add_dependencies(learn_generate_messages_eus _learn_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/jichanun/catin_ws/src/learn/msg/Person.msg" NAME_WE)
add_dependencies(learn_generate_messages_eus _learn_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/jichanun/catin_ws/src/learn/msg/vision.msg" NAME_WE)
add_dependencies(learn_generate_messages_eus _learn_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/jichanun/catin_ws/src/learn/msg/earphone.msg" NAME_WE)
add_dependencies(learn_generate_messages_eus _learn_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(learn_geneus)
add_dependencies(learn_geneus learn_generate_messages_eus)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS learn_generate_messages_eus)

### Section generating for lang: genlisp
### Generating Messages
_generate_msg_lisp(learn
  "/home/jichanun/catin_ws/src/learn/msg/expectp.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/learn
)
_generate_msg_lisp(learn
  "/home/jichanun/catin_ws/src/learn/msg/Person.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/learn
)
_generate_msg_lisp(learn
  "/home/jichanun/catin_ws/src/learn/msg/vision.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/learn
)
_generate_msg_lisp(learn
  "/home/jichanun/catin_ws/src/learn/msg/earphone.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/learn
)

### Generating Services

### Generating Module File
_generate_module_lisp(learn
  ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/learn
  "${ALL_GEN_OUTPUT_FILES_lisp}"
)

add_custom_target(learn_generate_messages_lisp
  DEPENDS ${ALL_GEN_OUTPUT_FILES_lisp}
)
add_dependencies(learn_generate_messages learn_generate_messages_lisp)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/jichanun/catin_ws/src/learn/msg/expectp.msg" NAME_WE)
add_dependencies(learn_generate_messages_lisp _learn_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/jichanun/catin_ws/src/learn/msg/Person.msg" NAME_WE)
add_dependencies(learn_generate_messages_lisp _learn_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/jichanun/catin_ws/src/learn/msg/vision.msg" NAME_WE)
add_dependencies(learn_generate_messages_lisp _learn_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/jichanun/catin_ws/src/learn/msg/earphone.msg" NAME_WE)
add_dependencies(learn_generate_messages_lisp _learn_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(learn_genlisp)
add_dependencies(learn_genlisp learn_generate_messages_lisp)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS learn_generate_messages_lisp)

### Section generating for lang: gennodejs
### Generating Messages
_generate_msg_nodejs(learn
  "/home/jichanun/catin_ws/src/learn/msg/expectp.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/learn
)
_generate_msg_nodejs(learn
  "/home/jichanun/catin_ws/src/learn/msg/Person.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/learn
)
_generate_msg_nodejs(learn
  "/home/jichanun/catin_ws/src/learn/msg/vision.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/learn
)
_generate_msg_nodejs(learn
  "/home/jichanun/catin_ws/src/learn/msg/earphone.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/learn
)

### Generating Services

### Generating Module File
_generate_module_nodejs(learn
  ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/learn
  "${ALL_GEN_OUTPUT_FILES_nodejs}"
)

add_custom_target(learn_generate_messages_nodejs
  DEPENDS ${ALL_GEN_OUTPUT_FILES_nodejs}
)
add_dependencies(learn_generate_messages learn_generate_messages_nodejs)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/jichanun/catin_ws/src/learn/msg/expectp.msg" NAME_WE)
add_dependencies(learn_generate_messages_nodejs _learn_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/jichanun/catin_ws/src/learn/msg/Person.msg" NAME_WE)
add_dependencies(learn_generate_messages_nodejs _learn_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/jichanun/catin_ws/src/learn/msg/vision.msg" NAME_WE)
add_dependencies(learn_generate_messages_nodejs _learn_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/jichanun/catin_ws/src/learn/msg/earphone.msg" NAME_WE)
add_dependencies(learn_generate_messages_nodejs _learn_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(learn_gennodejs)
add_dependencies(learn_gennodejs learn_generate_messages_nodejs)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS learn_generate_messages_nodejs)

### Section generating for lang: genpy
### Generating Messages
_generate_msg_py(learn
  "/home/jichanun/catin_ws/src/learn/msg/expectp.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/learn
)
_generate_msg_py(learn
  "/home/jichanun/catin_ws/src/learn/msg/Person.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/learn
)
_generate_msg_py(learn
  "/home/jichanun/catin_ws/src/learn/msg/vision.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/learn
)
_generate_msg_py(learn
  "/home/jichanun/catin_ws/src/learn/msg/earphone.msg"
  "${MSG_I_FLAGS}"
  ""
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/learn
)

### Generating Services

### Generating Module File
_generate_module_py(learn
  ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/learn
  "${ALL_GEN_OUTPUT_FILES_py}"
)

add_custom_target(learn_generate_messages_py
  DEPENDS ${ALL_GEN_OUTPUT_FILES_py}
)
add_dependencies(learn_generate_messages learn_generate_messages_py)

# add dependencies to all check dependencies targets
get_filename_component(_filename "/home/jichanun/catin_ws/src/learn/msg/expectp.msg" NAME_WE)
add_dependencies(learn_generate_messages_py _learn_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/jichanun/catin_ws/src/learn/msg/Person.msg" NAME_WE)
add_dependencies(learn_generate_messages_py _learn_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/jichanun/catin_ws/src/learn/msg/vision.msg" NAME_WE)
add_dependencies(learn_generate_messages_py _learn_generate_messages_check_deps_${_filename})
get_filename_component(_filename "/home/jichanun/catin_ws/src/learn/msg/earphone.msg" NAME_WE)
add_dependencies(learn_generate_messages_py _learn_generate_messages_check_deps_${_filename})

# target for backward compatibility
add_custom_target(learn_genpy)
add_dependencies(learn_genpy learn_generate_messages_py)

# register target for catkin_package(EXPORTED_TARGETS)
list(APPEND ${PROJECT_NAME}_EXPORTED_TARGETS learn_generate_messages_py)



if(gencpp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/learn)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gencpp_INSTALL_DIR}/learn
    DESTINATION ${gencpp_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_cpp)
  add_dependencies(learn_generate_messages_cpp std_msgs_generate_messages_cpp)
endif()

if(geneus_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/learn)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${geneus_INSTALL_DIR}/learn
    DESTINATION ${geneus_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_eus)
  add_dependencies(learn_generate_messages_eus std_msgs_generate_messages_eus)
endif()

if(genlisp_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/learn)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genlisp_INSTALL_DIR}/learn
    DESTINATION ${genlisp_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_lisp)
  add_dependencies(learn_generate_messages_lisp std_msgs_generate_messages_lisp)
endif()

if(gennodejs_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/learn)
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${gennodejs_INSTALL_DIR}/learn
    DESTINATION ${gennodejs_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_nodejs)
  add_dependencies(learn_generate_messages_nodejs std_msgs_generate_messages_nodejs)
endif()

if(genpy_INSTALL_DIR AND EXISTS ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/learn)
  install(CODE "execute_process(COMMAND \"/usr/bin/python2\" -m compileall \"${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/learn\")")
  # install generated code
  install(
    DIRECTORY ${CATKIN_DEVEL_PREFIX}/${genpy_INSTALL_DIR}/learn
    DESTINATION ${genpy_INSTALL_DIR}
  )
endif()
if(TARGET std_msgs_generate_messages_py)
  add_dependencies(learn_generate_messages_py std_msgs_generate_messages_py)
endif()
