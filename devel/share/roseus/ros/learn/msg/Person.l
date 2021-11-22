;; Auto-generated. Do not edit!


(when (boundp 'learn::Person)
  (if (not (find-package "LEARN"))
    (make-package "LEARN"))
  (shadow 'Person (find-package "LEARN")))
(unless (find-package "LEARN::PERSON")
  (make-package "LEARN::PERSON"))

(in-package "ROS")
;;//! \htmlinclude Person.msg.html


(intern "*UNKNOWN*" (find-package "LEARN::PERSON"))
(shadow '*UNKNOWN* (find-package "LEARN::PERSON"))
(defconstant learn::Person::*UNKNOWN* 0)
(intern "*MALE*" (find-package "LEARN::PERSON"))
(shadow '*MALE* (find-package "LEARN::PERSON"))
(defconstant learn::Person::*MALE* 1)
(intern "*FEMALE*" (find-package "LEARN::PERSON"))
(shadow '*FEMALE* (find-package "LEARN::PERSON"))
(defconstant learn::Person::*FEMALE* 2)
(defclass learn::Person
  :super ros::object
  :slots (_name _sex _age ))

(defmethod learn::Person
  (:init
   (&key
    ((:name __name) "")
    ((:sex __sex) 0)
    ((:age __age) 0)
    )
   (send-super :init)
   (setq _name (string __name))
   (setq _sex (round __sex))
   (setq _age (round __age))
   self)
  (:name
   (&optional __name)
   (if __name (setq _name __name)) _name)
  (:sex
   (&optional __sex)
   (if __sex (setq _sex __sex)) _sex)
  (:age
   (&optional __age)
   (if __age (setq _age __age)) _age)
  (:serialization-length
   ()
   (+
    ;; string _name
    4 (length _name)
    ;; uint8 _sex
    1
    ;; uint8 _age
    1
    ))
  (:serialize
   (&optional strm)
   (let ((s (if strm strm
              (make-string-output-stream (send self :serialization-length)))))
     ;; string _name
       (write-long (length _name) s) (princ _name s)
     ;; uint8 _sex
       (write-byte _sex s)
     ;; uint8 _age
       (write-byte _age s)
     ;;
     (if (null strm) (get-output-stream-string s))))
  (:deserialize
   (buf &optional (ptr- 0))
   ;; string _name
     (let (n) (setq n (sys::peek buf ptr- :integer)) (incf ptr- 4) (setq _name (subseq buf ptr- (+ ptr- n))) (incf ptr- n))
   ;; uint8 _sex
     (setq _sex (sys::peek buf ptr- :char)) (incf ptr- 1)
   ;; uint8 _age
     (setq _age (sys::peek buf ptr- :char)) (incf ptr- 1)
   ;;
   self)
  )

(setf (get learn::Person :md5sum-) "8361f88618d6779bd872f0ba928ced56")
(setf (get learn::Person :datatype-) "learn/Person")
(setf (get learn::Person :definition-)
      "string name
uint8 sex 
uint8 age

uint8 unknown=0
uint8 male=1
uint8 female=2

")



(provide :learn/Person "8361f88618d6779bd872f0ba928ced56")


