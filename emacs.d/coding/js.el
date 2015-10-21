(defun open-line-and-indent (n)
  "Insert a newline, indent it, and leave point indented before it."
  (interactive "*p")
  (open-line n)
  (indent-according-to-mode))

(defun my-js-mode-hook()
  (setq js-indent-level 2)
  (local-set-key "\C-o" 'open-line-and-indent)
  (local-set-key "\C-m" 'newline-and-indent)
  (local-set-key [ret] 'newline-and-indent))

(add-hook 'js-mode-hook 'my-js-mode-hook)

