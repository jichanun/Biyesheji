; Auto-generated. Do not edit!


(cl:in-package learn-msg)


;//! \htmlinclude vision.msg.html

(cl:defclass <vision> (roslisp-msg-protocol:ros-message)
  ((x
    :reader x
    :initarg :x
    :type (cl:vector cl:float)
   :initform (cl:make-array 7 :element-type 'cl:float :initial-element 0.0))
   (y
    :reader y
    :initarg :y
    :type (cl:vector cl:float)
   :initform (cl:make-array 7 :element-type 'cl:float :initial-element 0.0)))
)

(cl:defclass vision (<vision>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <vision>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'vision)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name learn-msg:<vision> is deprecated: use learn-msg:vision instead.")))

(cl:ensure-generic-function 'x-val :lambda-list '(m))
(cl:defmethod x-val ((m <vision>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader learn-msg:x-val is deprecated.  Use learn-msg:x instead.")
  (x m))

(cl:ensure-generic-function 'y-val :lambda-list '(m))
(cl:defmethod y-val ((m <vision>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader learn-msg:y-val is deprecated.  Use learn-msg:y instead.")
  (y m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <vision>) ostream)
  "Serializes a message object of type '<vision>"
  (cl:map cl:nil #'(cl:lambda (ele) (cl:let ((bits (roslisp-utils:encode-single-float-bits ele)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)))
   (cl:slot-value msg 'x))
  (cl:map cl:nil #'(cl:lambda (ele) (cl:let ((bits (roslisp-utils:encode-single-float-bits ele)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 8) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 16) bits) ostream)
    (cl:write-byte (cl:ldb (cl:byte 8 24) bits) ostream)))
   (cl:slot-value msg 'y))
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <vision>) istream)
  "Deserializes a message object of type '<vision>"
  (cl:setf (cl:slot-value msg 'x) (cl:make-array 7))
  (cl:let ((vals (cl:slot-value msg 'x)))
    (cl:dotimes (i 7)
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:aref vals i) (roslisp-utils:decode-single-float-bits bits)))))
  (cl:setf (cl:slot-value msg 'y) (cl:make-array 7))
  (cl:let ((vals (cl:slot-value msg 'y)))
    (cl:dotimes (i 7)
    (cl:let ((bits 0))
      (cl:setf (cl:ldb (cl:byte 8 0) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 8) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 16) bits) (cl:read-byte istream))
      (cl:setf (cl:ldb (cl:byte 8 24) bits) (cl:read-byte istream))
    (cl:setf (cl:aref vals i) (roslisp-utils:decode-single-float-bits bits)))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<vision>)))
  "Returns string type for a message object of type '<vision>"
  "learn/vision")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'vision)))
  "Returns string type for a message object of type 'vision"
  "learn/vision")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<vision>)))
  "Returns md5sum for a message object of type '<vision>"
  "a0ae65e34517895bd1b390204c93e42d")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'vision)))
  "Returns md5sum for a message object of type 'vision"
  "a0ae65e34517895bd1b390204c93e42d")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<vision>)))
  "Returns full string definition for message of type '<vision>"
  (cl:format cl:nil "float32[7] x~%float32[7] y~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'vision)))
  "Returns full string definition for message of type 'vision"
  (cl:format cl:nil "float32[7] x~%float32[7] y~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <vision>))
  (cl:+ 0
     0 (cl:reduce #'cl:+ (cl:slot-value msg 'x) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ 4)))
     0 (cl:reduce #'cl:+ (cl:slot-value msg 'y) :key #'(cl:lambda (ele) (cl:declare (cl:ignorable ele)) (cl:+ 4)))
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <vision>))
  "Converts a ROS message object to a list"
  (cl:list 'vision
    (cl:cons ':x (x msg))
    (cl:cons ':y (y msg))
))
