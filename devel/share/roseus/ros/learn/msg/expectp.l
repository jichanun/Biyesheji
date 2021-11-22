;; Auto-generated. Do not edit!


(when (boundp 'learn::expectp)
  (if (not (find-package "LEARN"))
    (make-package "LEARN"))
  (shadow 'expectp (find-package "LEARN")))
(unless (find-package "LEARN::EXPECTP")
  (make-package "LEARN::EXPECTP"))

(in-package "ROS")
;;//! \htmlinclude expectp.msg.html


(defclass learn::expectp
  :super ros::object
  :slots (_x _y ))

(defmethod learn::expectp
  (:init
   (&key
    ((:x __x) (make-array 6 :initial-element 0.0 :element-type :float))
    ((:y __y) (make-array 6 :initial-element 0.0 :element-type :float))
    )
   (send-super :init)
   (setq _x __x)
   (setq _y __y)
   self)
  (:x
   (&optional __x)
   (if __x (setq _x __x)) _x)
  (:y
   (&optional __y)
   (if __y (setq _y __y)) _y)
  (:serialization-length
   ()
   (+
    ;; float32[6] _x
    (* 4    6)
    ;; float32[6] _y
    (* 4    6)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float32[6] _x
     (dotimes (i 6)
       (sys::poke (elt _x i) (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
       )
     ;; float32[6] _y
     (dotimes (i 6)
       (sys::poke (elt _y i) (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
       )
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float32[6] _x
   (dotimes (i (length _x))
     (setf (elt _x i) (sys::peek buf ptr- :float)) (incf ptr- 4)
     )
   ;; float32[6] _y
   (dotimes (i (length _y))
     (setf (elt _y i) (sys::peek buf ptr- :float)) (incf ptr- 4)
     )
   ;;
   self)
  )

(setf (get learn::expectp :md5sum-) "d75c2d0ec0230fe2d3e3aa96f78888c9")
(setf (get learn::expectp :datatype-) "learn/expectp")
(setf (get learn::expectp :definition-)
      "float32[6] x
float32[6] y

")



(provide :learn/expectp "d75c2d0ec0230fe2d3e3aa96f78888c9")


