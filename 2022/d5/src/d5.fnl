(local fennel (require :fennel)) 

(fn pp [x] 
  (print (fennel.view x)))

(fn get-crates-insns [fileloc]
  (let [file (assert (io.open fileloc :r))
      contents (file:read "*a")
      (crates instrs) ((string.gmatch contents "(.+)\n\n(.+)"))
      ]
    (file:close)
    [crates instrs]))
  
(let [fileloc (. _G.arg 1)
      (crates instrs) (get-crates-insns fileloc)
      ]
  ;; (pp contents)
  ;; (print split)
  (pp crates)
  (pp instrs)
)

; REPL helpers
(tset _G :arg ["./data/example.txt"]) ; provides hint for arg[1] to the REPL
(assert (= (. _G.arg 1) "../data/example.txt"))
(local fennel (require :fennel))

(fn _G.pp [x]
  (print (fennel.view x)))
;; (_G.pp _G.arg)


;; REPL sandbox
; Function vs lambda: failure to pass a specific or nil variable
;; (fn nilable [a b c]
;;   (print a b c))
;; (nilable 10 12)
;;
;; (lambda non-nilable [a b c]
;;   (print a b c))
;; (non-nilable 10 12)


;; (let [(a b) ((string.gmatch "hello\nmy\nrandom\nstranger\n\nin\nthis\nsmall\nworld" "(.+)\n\n(.+)"))]
;;   (_G.pp a)
;;   (_G.pp b))

;; (let [split ((string.gmatch "hello\nmy\nrandom\nstranger\n\nin\nthis\nsmall\nworld" "(.+)\n"))]
;;   (_G.pp split)
;;   )

;; (fn overpass [a]
;;   (print a)) (overpass "hello" "world")
;;
;; (lambda overpass [a]
;;   (print a)) (overpass "hello" "world")

