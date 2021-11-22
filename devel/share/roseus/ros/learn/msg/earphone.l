;; Auto-generated. Do not edit!


(when (boundp 'learn::earphone)
  (if (not (find-package "LEARN"))
    (make-package "LEARN"))
  (shadow 'earphone (find-package "LEARN")))
(unless (find-package "LEARN::EARPHONE")
  (make-package "LEARN::EARPHONE"))

(in-package "ROS")
;;//! \htmlinclude earphone.msg.html


(intern "*LEFT*" (find-package "LEARN::EARPHONE"))
(shadow '*LEFT* (find-package "LEARN::EARPHONE"))
(defconstant learn::earphone::*LEFT* 1)
(intern "*REGHT*" (find-package "LEARN::EARPHONE"))
(shadow '*REGHT* (find-package "LEARN::EARPHONE"))
(defconstant learn::earphone::*REGHT* 2)
(defclass learn::earphone
  :super ros::object
  :slots (_name _number _time _x _y ))

(defmethod learn::earphone
  (:init
   (&key
    ((:name __name) "")
    ((:number __number) 0)
    ((:time __time) 0.0)
    ((:x __x) 0.0)
    ((:y __y) 0.0)
    )
   (send-super :init)
   (setq _name (string __name))
   (setq _number (round __number))
   (setq _time (float __time))
   (setq _x (float __x))
   (setq _y (float __y))
   self)
  (:name
   (&optional __name)
   (if __name (setq _name __name)) _name)
  (:number
   (&optional __number)
   (if __number (setq _number __number)) _number)
  (:time
   (&optional __time)
   (if __time (setq _time __time)) _time)
  (:x
   (&optional __x)
   (if __x (setq _x __x)) _x)
  (:y
   (&optional __y)
   (if __y (setq _y __y)) _y)
  (:serialization-length
   ()
   (+
    ;; string _name
    4 (length _name)
    ;; uint8 _number
    1
    ;; float32 _time
    4
    ;; float32 _x
    4
    ;; float32 _y
    4
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; string _name
       (write-long (length _name) s) (princ _name s)
     ;; uint8 _number
       (write-byte _number s)
     ;; float32 _time
       (sys::poke _time (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _x
       (sys::poke _x (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;; float32 _y
       (sys::poke _y (send s :buffer) (send s :count) :float) (incf (stream-count s) 4)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; string _name
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _name (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;; uint8 _number
     (setq _number (sys::peek buf ptr- :char)) (incf ptr- 1)
   ;; float32 _time
     (setq _time (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _x
     (setq _x (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;; float32 _y
     (setq _y (sys::peek buf ptr- :float)) (incf ptr- 4)
   ;;
   self)
  )

(setf (get learn::earphone :md5sum-) "0e54ded6bb48427135cdde6b26c23e80")
(setf (get learn::earphone :datatype-) "learn/earphone")
(setf (get learn::earphone :definition-)
      "string name
uint8 number
float32 time
float32 x
float32 y


uint8 left=1
uint8 reght=2

")



(provide :learn/earphone "0e54ded6bb48427135cdde6b26c23e80")


