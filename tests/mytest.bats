load harness

@test "mytest-1" {
  check 'x := -1' '⇒ skip, {x → -1}'
}

@test "mytest-2" {
  check '{ a := 1 ; b := 2 ; c := 3 ; d := 4}' '⇒ skip; b := 2; c := 3; d := 4, {a → 1}
⇒ b := 2; c := 3; d := 4, {a → 1}
⇒ skip; c := 3; d := 4, {a → 1, b → 2}
⇒ c := 3; d := 4, {a → 1, b → 2}
⇒ skip; d := 4, {a → 1, b → 2, c → 3}
⇒ d := 4, {a → 1, b → 2, c → 3}
⇒ skip, {a → 1, b → 2, c → 3, d → 4}'
}

@test "mytest-3" {
  check 'if 3 < -3 * 1 then g := 3 + -2 else h := 009 + 900' '⇒ h := (9+900), {}
⇒ skip, {h → 909}'
}

@test "mytest-4" {
  check 'while false do c := aaa * bbb' '⇒ skip, {}'
}

@test "mytest-5" {
  check 'z := 3; while z > 0 do z := z - 1' '⇒ skip; while (z>0) do { z := (z-1) }, {z → 3}
⇒ while (z>0) do { z := (z-1) }, {z → 3}
⇒ z := (z-1); while (z>0) do { z := (z-1) }, {z → 3}
⇒ skip; while (z>0) do { z := (z-1) }, {z → 2}
⇒ while (z>0) do { z := (z-1) }, {z → 2}
⇒ z := (z-1); while (z>0) do { z := (z-1) }, {z → 2}
⇒ skip; while (z>0) do { z := (z-1) }, {z → 1}
⇒ while (z>0) do { z := (z-1) }, {z → 1}
⇒ z := (z-1); while (z>0) do { z := (z-1) }, {z → 1}
⇒ skip; while (z>0) do { z := (z-1) }, {z → 0}
⇒ while (z>0) do { z := (z-1) }, {z → 0}
⇒ skip, {z → 0}'
}