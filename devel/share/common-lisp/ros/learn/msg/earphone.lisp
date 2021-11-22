; Auto-generated. Do not edit!


(cl:in-package learn-msg)


;//! \htmlinclude earphone.msg.html

(cl:defclass <earphone> (roslisp-msg-protocol:ros-message)
  ((name
    :reader name
    :initarg :name
    :type cl:string
    :initform "")
   (number
    :reader number
    :initarg :number
    :type cl:fixnum
    :initform 0)
   (time
    :reader time
    :initarg :time
    :type cl:float
    :initform 0.0)
   (x
    :reader x
    :initarg :x
    :type cl:float
    :initform 0.0)
   (y
    :reader y
    :initarg :y
    :type cl:float
    :initform 0.0))
)

(cl:defclass earphone (<earphone>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <earphone>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'earphone)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name learn-msg:<earphone> is deprecated: use learn-msg:earphone instead.")))

(cl:ensure-generic-function 'name-val :lambda-list '(m))
(cl:defmethod name-val ((m <earphone>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader learn-msg:name-val is deprecated.  Use learn-msg:name instead.")
  (name m))

(cl:ensure-generic-function 'number-val :lambda-list '(m))
(cl:defmethod number-val ((m <earphone>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader learn-msg:number-val is deprecated.  Use learn-msg:number instead.")
  (number m))

(cl:ensure-generic-function 'time-val :lambda-list '(m))
(cl:defmethod time-val ((m <earphone>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader learn-msg:time-val is deprecated.  Use learn-msg:time instead.")
  (time m))

(cl:ensure-generic-function 'x-val :lambda-list '(m))
(cl:defmethod x-val ((m <earphone>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader learn-msg:x-val is deprecated.  Use learn-msg:x instead.")
  (x m))

(cl:ensure-generic-function 'y-val :lambda-list '(m))
(cl:defmethod y-val ((m <earphone>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader learn-msg:y-val is deprecated.  Use learn-msg:y instead.")
  (y m))
(cl:defmethod roslisp-msg-protocol:symbol-codes ((msg-type (cl:eql '<earphone>)))
    "Constants for message type '<earphone>"
  '((:LEFT . 1)
    (:REGHT . 2))
)
(cl:defmethod roslisp-msg-protocol:symbol-codes ((msg-type (cl:eql 'earphone)))
    "Constants for message type 'earphone"
  '((:LEFT . 1)
    (:REGHT . 2))
)
(cl:defmethod roslisp-msg-protocol:serialize ((msg <earphone>) ostream)
  "Serializes a message object of type '<earphone>"
  (cl:let ((__ros_str_len (cl:length (cl:slot-value msg 'name))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) __ros_str_len) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) __ros_str_len) ostream))
  (cl:map cl:nil #'(cl:lambda (c) (cl:write-byte (cl:char-code c) ostream)) (cl:slot-value msg 'name))
  (cl:write-byte (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'number)) ostream)
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'time))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'x))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
  (cl:let ((bits (roslisp-utils:encode-single-float-bits (cl:slot-value msg 'y))))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <earphone>) istream)
  "Deserializes a message object of type '<earphone>"
    (cl:let ((__ros_str_len 0))
      (cl:setf (cl:ldb (cl:byte 8 0) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) __ros_str_len) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'name) (cl:make-string __ros_str_len))
      (cl:dotimes (__ros_str_idx __ros_str_len msg)
        (cl:setf (cl:char (cl:slot-value msg 'name) __ros_str_idx) (cl:code-char (cl:read-byte istream)))))
    (cl:setf (cl:ldb (cl:byte 8 0) (cl:slot-value msg 'number)) (cl:read-byte istream))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'time) (roslisp-utils:decode-single-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'x) (roslisp-utils:decode-single-float-bits bits)))
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:slot-value msg 'y) (roslisp-utils:decode-single-float-bits bits)))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<earphone>)))
  "Returns string type for a message object of type '<earphone>"
  "learn/earphone")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'earphone)))
  "Returns string type for a message object of type 'earphone"
  "learn/earphone")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<earphone>)))
  "Returns md5sum for a message object of type '<earphone>"
  "0e54ded6bb48427135cdde6b26c23e80")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'earphone)))
  "Returns md5sum for a message object of type 'earphone"
  "0e54ded6bb48427135cdde6b26c23e80")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<earphone>)))
  "Returns full string definition for message of type '<earphone>"
  (cl:format cl:nil "string name~%uint8 number~%float32 time~%float32 x~%float32 y~%~%~%uint8 left=1~%uint8 reght=2~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'earphone)))
  "Returns full string definition for message of type 'earphone"
  (cl:format cl:nil "string name~%uint8 number~%float32 time~%float32 x~%float32 y~%~%~%uint8 left=1~%uint8 reght=2~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <earphone>))
  (cl:+ 0
     4 (cl:length (cl:slot-value msg 'name))
     1
     4
     4
     4
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <earphone>))
  "Converts a ROS message object to a list"
  (cl:list 'earphone
    (cl:cons ':name (name msg))
    (cl:cons ':number (number msg))
    (cl:cons ':time (time msg))
    (cl:cons ':x (x msg))
    (cl:cons ':y (y msg))
))
