(add-hook 'c-mode-common-hook 'google-set-c-style)
(add-hook 'c++-mode-hook 'google-set-c-style)
(add-hook 'c-mode-common-hook 'google-make-newline-indent)
(add-hook 'c++-mode-hook 'google-make-newline-indent)

(defconst my-c-style
  '((c-tab-alwyas-indent . t)
    (c-offsets-alist . ((access-label . /))))
  "Google Style Indentation")

(defun my-gcpp-style-hook ()
  (c-add-style "gcppstyle" my-c-style t)
  (setq c-default-style
        '((c-mode . "gcppstyle") (c++-mode . "gcppstyle"))))

(add-hook 'c++-mode-hook 'my-gcpp-style-hook)

(defconst my-cc-style
  '("cc-mode"
    (c-offsets-alist . ((innamespace . 0)))))
(c-add-style "my-cc-mode" my-cc-style)

(setq auto-mode-alist
  (cons '("\.h$" . c++-mode) auto-mode-alist))

;;(add-to-list 'load-path "~/source/rtags/src")
;;(require 'rtags)
;;(load "~/source/rtags/src/company-rtags.el")
;; (require 'company-rtags)
;;(setq rtags-completions-enabled t)
;;(define-key c-mode-base-map (kbd "M-.") (function rtags-find-symbol-at-point))
;;(define-key c-mode-base-map (kbd "M-,") (function rtags-find-references-at-point))
;;(define-key c-mode-base-map (kbd "M-;") (function rtags-find-file))
;;(define-key c-mode-base-map (kbd "C-.") (function rtags-find-symbol))
;;(define-key c-mode-base-map (kbd "C-,") (function rtags-find-references))
;;(define-key c-mode-base-map (kbd "C-<") (function rtags-find-virtuals-at-point))
;;(define-key c-mode-base-map (kbd "M-i") (function rtags-imenu))
;;(define-key c-mode-base-map (kbd "M-u") (function rtags-location-stack-back))
;;(define-key c-mode-base-map (kbd "M-n") (function rtags-location-stack-forward))

