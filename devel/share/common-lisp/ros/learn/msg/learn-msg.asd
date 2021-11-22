
(cl:in-package :asdf)

(defsystem "learn-msg"
  :depends-on (:roslisp-msg-protocol :roslisp-utils )
  :components ((:file "_package")
    (:file "Person" :depends-on ("_package_Person"))
    (:file "_package_Person" :depends-on ("_package"))
    (:file "earphone" :depends-on ("_package_earphone"))
    (:file "_package_earphone" :depends-on ("_package"))
    (:file "expectp" :depends-on ("_package_expectp"))
    (:file "_package_expectp" :depends-on ("_package"))
    (:file "vision" :depends-on ("_package_vision"))
    (:file "_package_vision" :depends-on ("_package"))
  ))