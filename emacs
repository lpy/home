;;;;;;;;;; lpy's Emacs DOT file

;; auto-to-list
(add-to-list 'load-path "~/.emacs.d/plugins")
(add-to-list 'load-path "~/.emacs.d/plugins/autopair")
;(add-to-list 'load-path "~/.emacs.d/plugins/powerline")


;(which-function-mode)
(setq default-fill-column 88)
(setq max-lisp-eval-depth 9999)
(ido-mode t)
(show-paren-mode t)
(setq show-paren-style 'parentheses)
(setq skeleton-pair t)
(setq x-select-enable-clipboard t)
;; line number
(setq column-number-mode t)
(global-linum-mode 1)
(setq-default kill-whole-line t)
(setq-default indent-tabs-mode nil)

(setq-default truncate-lines 1) ;; no wrap

(if (eq system-type 'darwin)
  (set-keyboard-coding-system nil))
(when window-system
  (tool-bar-mode -1))

;; For copy and paste with system clipboard on Unix
(defun copy-from-osx ()
  (shell-command-to-string "pbpaste"))
(defun paste-to-osx (text &optional push)
  (let ((process-connection-type nil))
    (let ((proc (start-process"pbcopy" "*Messages*" "pbcopy"))) 
      (process-send-string proc text) 
      (process-send-eof proc))))
(if (eq system-type 'darwin)
  (unless window-system
    (setq interprogram-cut-function 'paste-to-osx)))
(if (eq system-type 'darwin)
  (unless window-system
    (setq interprogram-paste-function 'copy-from-osx)))

(put 'scroll-left 'disabled nil) ;; remove scroll
(mouse-avoidance-mode 'animate)
(auto-image-file-mode t) 
(setq frame-title-format "%n%F/%b")
(setq kill-ring-max 250)
(if (eq system-type 'darwin)
  (set-default-font "Monaco-16")) ;; font
(setq inhibit-startup-message t)
;; windows size when launched
(add-to-list 'default-frame-alist '(fullscreen . maximized))
;;(setq default-frame-alist
;;      '((height . 50) (width . 150) (menu-bar-lines . 20) (tool-bar-lines . 0))) 

(setq display-time-24hr-format t)
(setq display-time-day-and-date t)
(display-time)
(setq display-time-default-load-average nil)
(setq-default make-backup-files nil) ;; Don't create the temp file
(setq auto-save-mode nil) ;; turn offf auto save
(setq auto-save-default nil) ;; turn off temporary file
(fset 'yes-or-no-p 'y-or-n-p) ;; using 'y' and 'n' to replace 'yes' and 'no'

;; autopair-configuration
(require 'autopair)
(autopair-global-mode 1)

;; Cursor-change
(require 'cursor-chg)
(change-cursor-mode) ; On for overwrite/read-only/input mode
(toggle-cursor-type-when-idle 1) ; On when idle

;; for colorful parentheses
(require 'rainbow-delimiters)
(add-hook 'lisp-mode-hook 'rainbow-delimiters-mode)
(add-hook 'scheme-mode-hook 'rainbow-delimiters-mode)
(add-hook 'emacs-lisp-mode-hook 'rainbow-delimiters-mode)
(custom-set-faces
 '(default ((t (:inherit nil :stipple nil :background "Black" :foreground "SteelBlue" :inverse-video nil :box nil :strike-through nil :overline nil :underline nil :slant normal :weight normal :height 128 :width normal :foundry "unknown" :family "monaco"))))
 '(rainbow-delimiters-depth-1-face ((t (:foreground "green"))))
 '(rainbow-delimiters-depth-2-face ((t (:foreground "gold"))))
 '(rainbow-delimiters-depth-3-face ((t (:foreground "deep sky blue"))))
 '(rainbow-delimiters-depth-4-face ((t (:foreground "green yellow"))))
 '(rainbow-delimiters-depth-5-face ((t (:foreground "dark violet"))))
 '(rainbow-delimiters-depth-6-face ((t (:foreground "magenta"))))
 '(rainbow-delimiters-depth-7-face ((t (:foreground "light coral"))))
 '(rainbow-delimiters-depth-8-face ((t (:foreground "RosyBrown2"))))
 '(rainbow-delimiters-depth-9-face ((t (:foreground "gray100"))))
 '(rainbow-delimiters-unmatched-face ((t (:foreground "red")))))

;; Emacs Package Manager
(setq package-list '(company flycheck flycheck-google-cpplint neotree powerline company-jedi))

(require 'package)
(add-to-list 'package-archives
             '("melpa-stable" . "https://stable.melpa.org/packages/"))
(add-to-list 'package-archives '("elpa" . "https://elpa.gnu.org/packages/"))

;; (if (>= emacs-major-version 24)
;;   (progn (require 'package)
;;     (add-to-list 'package-archives
;;       '("melpa" . "http://melpa.milkbox.net/packages/") t)))
    ;(add-to-list 'package-archives
    ;  '("marmalade" . "http://marmalade-repo.org/packages/") t)
    ;(add-to-list 'package-archives
    ;  '("org". "http://orgmode.org/elpa/") t)))
(package-initialize)
; fetch the list of packages available 
(unless package-archive-contents
  (package-refresh-contents))

; install the missing packages
(dolist (package package-list)
  (unless (package-installed-p package)
      (package-install package)))

;(require 'powerline)
(add-hook 'after-init-hook 'powerline-default-theme)


(add-hook 'after-init-hook 'global-company-mode) ;; company-mode
(setq company-idle-delay 0.2)
(setq company-minimum-prefix-length 1)
(setq company-dabbrev-ignore-case nil)

(load "~/.emacs.d/coding/cc.el")
(load "~/.emacs.d/coding/js.el")
(load "~/.emacs.d/coding/py.el")

;; flycheck
(add-hook 'after-init-hook #'global-flycheck-mode)

;;;;;;;;;; Self-customized function Begin


(defadvice comment-or-uncomment-region (before slickcomment activate compile)
  "When called interactively with no active region, toggle comment on current line instead."
  (interactive
   (if mark-active (list (region-beginning) (region-end))
     (list (line-beginning-position)
           (line-beginning-position 2)))))
(global-set-key (kbd "C-c C-c") 'comment-or-uncomment-region)


;; Original idea from
;; http://www.opensubscriber.com/message/emacs-devel@gnu.org/10971693.html
(defun comment-dwim-line (&optional arg)
  "Replacement for the comment-dwim command.
        If no region is selected and current line is not blank and we are not at the end of the line,
        then comment current line.
        Replaces default behaviour of comment-dwim, when it inserts comment at the end of the line."
  (interactive "*P")
  (comment-normalize-vars)
  (if (and (not (region-active-p)) (not (looking-at "[ \t]*$")))
      (comment-or-uncomment-region (line-beginning-position) (line-end-position))
    (comment-dwim arg)))
(global-set-key (kbd "C-;") 'comment-dwim-line)


(defun mykillbuffer ()
  (interactive)
  (kill-buffer))
(global-set-key (kbd "C-Q") 'mykillbuffer)


(defun my-replace-regexp (replacedstring replacestring)
  (interactive "MReplaced Regexp: \nMReplace Regexp: ")
  (mark-whole-buffer)
  (replace-regexp replacedstring replacestring))
(define-key global-map (kbd "C-x ?") 'my-replace-regexp)


(defun indent-whole-buffer ()
  "indent whole buffer"
  (interactive)
  (delete-trailing-whitespace)
  (indent-region (point-min) (point-max) nil)
  (untabify (point-min) (point-max)))
(defun indent-current-paragraph ()
  "indent current paragraph"
  (interactive)
  (save-excursion
    (delete-trailing-whitespace)
    (mark-paragraph)
    (indent-region (region-beginning) (region-end) nil)))

(load "~/.emacs.d/plugins/quickopen/elisp/quickopen.el")

;;;;;;;;;; Self-customized function End
