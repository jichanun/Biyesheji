;; Auto-generated. Do not edit!


(when (boundp 'learn::vision)
  (if (not (find-package "LEARN"))
    (make-package "LEARN"))
  (shadow 'vision (find-package "LEARN")))
(unless (find-package "LEARN::VISION")
  (make-package "LEARN::VISION"))

(in-package "ROS")
;;//! \htmlinclude vision.msg.html


(defclass learn::vision
  :super ros::object
  :slots (_x _y ))

(defmethod learn::vision
  (:init
   (&key
    ((:x __x) (make-array 7 :initial-element 0.0 :element-type :float))
    ((:y __y) (make-array 7 :initial-element 0.0 :element-type :float))
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
    ;; float32[7] _x
    (* 4    7)
    ;; float32[7] _y
    (* 4    7)
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; float32[7] _x
     (dotimes (i 7)
       (sys::poke (elt _x i) (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
       )
     ;; float32[7] _y
     (dotimes (i 7)
       (sys::poke (elt _y i) (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
       )
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; float32[7] _x
   (dotimes (i (length _x))
     (setf (elt _x i) (sys::peek buf ptr- :float)) (incf ptr- 4)
     )
   ;; float32[7] _y
   (dotimes (i (length _y))
     (setf (elt _y i) (sys::peek buf ptr- :float)) (incf ptr- 4)
     )
   ;;
   self)
  )

(setf (get learn::vision :md5sum-) "a0ae65e34517895bd1b390204c93e42d")
(setf (get learn::vision :datatype-) "learn/vision")
(setf (get learn::vision :definition-)
      "float32[7] x
float32[7] y

")



(provide :learn/vision "a0ae65e34517895bd1b390204c93e42d")


