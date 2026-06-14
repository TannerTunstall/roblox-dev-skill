# Luau Language Reference

Luau = Roblox's Lua 5.1 fork with gradual typing, faster VM, extra syntax/libraries. Dynamically typed at runtime; the type system is static-analysis only (no runtime cost, never affects behavior). Single number type (`double`), 1-based arrays, `nil` for absence, truthy = everything except `false`/`nil`.

## Core values & quirks

- Types: `nil`, `boolean`, `number` (64-bit double), `string` (immutable, byte sequence), `table`, `function`, `thread`, `userdata`, plus Roblox datatypes (`Vector3`, `CFrame`, `Instance`, …) and `buffer`, `vector`.
- **Truthiness**: only `false` and `nil` are falsy. ✗ `0` and `""` are TRUTHY (unlike C/JS). `if 0 then` runs.
- **Numbers**: no int/float distinction — `1 == 1.0`. `-0 == 0`. Range ±1.7e308, ~15 digits precision. `int`/`float`/`int64` in API docs are just usage hints; APIs may round or error on non-integers. `Player.UserId` is `int64`.
- Number literals: `1_000_000` (underscores ignored), `0xFF`, `0b1010`, `12e3`, `1.25`.
- `nil` removes things: `t.key = nil` deletes key; `inst.Parent = nil` detaches; `bigVar = nil` frees for GC.
- `type(x)` → base type string; `typeof(x)` → also returns Roblox datatype names (`"Vector3"`, `"Instance"`). Prefer `typeof` on Roblox values.

```lua
print(type(workspace))    --> userdata
print(typeof(workspace))  --> Instance
```

## Variables, scope, closures

- Declare `local` always — globals use a hash lookup and are >10% slower in hot loops, leak across the script, and never GC until script dies. ✗ never rely on implicit globals.
- Multiple assignment: `local a, b, c = 1, 2, 3`. Extra vars → `nil`; extra values dropped. Swap: `a, b = b, a`.
- Scope nests; child blocks read parent locals (capture/**upvalue**), not vice-versa. `do ... end` makes a bare scope block (like `{}` in C#).
- **Shadowing** allowed: inner `local x` is a new variable, doesn't mutate outer.
- `repeat ... until cond` — the condition CAN see locals declared inside the body (unique to Lua).

```lua
local function counter()        -- closures capture by reference
    local n = 0
    return function() n += 1; return n end
end
local c = counter(); print(c(), c())  --> 1  2
```

## Operators

- Arithmetic: `+ - * / ^ %`, and `//` **floor division** (`-10 // 4 == -3`, rounds toward −∞). `^` and `%` exist; no `**`.
- Compound: `+= -= *= /= //= %= ^= ..=`. RHS evaluated once. ✗ no `++`/`--`.
- Comparison: `==` `~=` (not `!=`) `< > <= >=`. Concatenate with `..`. Length with `#`.
- Logical `and`/`or`/`not` return operands, not booleans:
  - `a and b` → `a` if falsy else `b`; `a or b` → `a` if truthy else `b`.
  - Default value: `local x = arg or 10`. ⚠ breaks if a valid value is `false`/`0`... but `0` is truthy so `count or 5` is safe; `flag or true` is NOT (use explicit `if flag == nil`).
  - Ternary: `local m = if x > y then x else y` (Luau `if`-expression; no `?:`).
  - Guard: `local v = t and t.field` (nil-safe-ish chaining).
- `==` on tables/functions/threads/userdata is **identity** (reference equality), not structural — two different tables with same contents are `~=`. Override with `__eq` metamethod (both operands need same metamethod).
- String relational ops are lexicographic by byte/ASCII: `"100" < "20"` is `true`.

## Strings

Immutable. Single or double quotes; `[[ ... ]]` for multi-line/raw (use `[=[ ]=]` to nest). Backslash escapes `\n \t \" \'`. Interpolation with backticks: `` `Hello {name}, {n+1}!` `` (any expression inside `{}`).

```lua
local s = `Pi≈{string.format("%.2f", math.pi)}`
print(#s)              -- byte length
print(("abc"):upper()) -- methods callable on string literals via metatable
```

- Arithmetic coerces string→number (`"55" + 10 == 65`); errors if not numeric. `..` coerces number→string. `tonumber("123")`→number or nil; `tostring(x)`. For controlled formatting use `string.format` not coercion.

### string library (use `s:method(...)` or `string.method(s,...)`)
```
string.format(fmt, ...) -> string        -- %d %s %f %.2f %x %q etc.
string.sub(s, i, j) -> string            -- 1-based; negatives count from end. s:sub(-3)
string.len(s) / #s -> number
string.find(s, pat, init?, plain?) -> startIdx, endIdx, captures...
string.match(s, pat, init?) -> captures... | nil
string.gmatch(s, pat) -> iterator        -- for w in s:gmatch("%a+") do
string.gsub(s, pat, repl, n?) -> result, count   -- repl: string/table/function
string.split(s, sep) -> {string}         -- Luau extension
string.rep(s, n, sep?) ; string.reverse(s)
string.upper / string.lower
string.byte(s, i?, j?) -> codes... ; string.char(...) -> string
string.pack/unpack/packsize               -- binary; prefer buffer for new code
```

### Patterns (NOT regex)
Classes: `%a` letter `%d` digit `%s` space `%w` alphanumeric `%p` punct `%l`/`%u` lower/upper `%x` hex `.` any. Uppercase = complement (`%A` = non-letter). Quantifiers: `*` 0+, `+` 1+, `-` lazy 0+, `?` 0/1. Anchors `^` start, `$` end. Sets `[abc]`, `[^abc]`, ranges `[a-z]`. Captures `()`; empty `()` captures position (number). Magic chars `^$()%.[]*+-?` escape with `%`. Back-reference `%1`; balanced `%b()`. In `gsub` replacement use `%1`..`%9`.

```lua
for k, v in string.gmatch("a=1, b=2", "(%a+)%s*=%s*(%d+)") do print(k, v) end
```

## Tables

One structure for arrays, dicts, objects, sets. Construct `{}`. Stored/passed by **reference**, never copied.

### Arrays (1-based!)
```lua
local a = {"x", 3.14, true}      -- a[1] == "x"
for i, v in a do ... end          -- generalized iteration (preferred)
for i = 1, #a do ... end
table.insert(a, v)                -- append; or a[#a+1] = v
table.insert(a, pos, v)           -- insert at pos, shifts up
table.remove(a, pos?)             -- remove & shift down; returns removed
```
- **`#` only valid on sequences** (1..n, no holes). On sparse arrays (a `nil` gap) `#` returns ANY border — undefined. ✗ never store `nil` inside an array; setting `a[i]=nil` mid-array creates a hole. Track length yourself or use `table.remove`.
- Iterate arrays with generalized `for i,v in a` or `ipairs` (stops at first nil). `ipairs` order guaranteed; `pairs`/generalized over dicts is arbitrary order.

### Dictionaries
```lua
local d = {fruitName = "Lemon", [part] = true}  -- any non-nil key
d.fruitName ; d["fruitName"] ; d[part]
d.newKey = 10 ; d.fruitName = nil               -- nil deletes key
for k, v in d do ... end                         -- arbitrary order
```

### table library
```
table.create(n, v?) -> table     -- preallocate n slots (=v); FAST for hot fills
table.insert / table.remove
table.find(t, value, init?) -> index | nil
table.concat(t, sep?, i?, j?) -> string
table.sort(t, comp?)             -- in place; comp(a,b) returns a<b
table.clone(t) -> table          -- shallow copy
table.move(src, a, b, t, dst?) -> dst   -- copy range src[a..b] to dst[t..]
table.freeze(t) -> t ; table.isfrozen(t)  -- read-only, permanent
table.clear(t)                   -- remove all keys, keep capacity
table.pack(...) -> {n=count, ...} ; table.unpack(t, i?, j?) -> values...
-- DEPRECATED: table.getn, table.foreach, table.foreachi, table.maxn
```

### Performance idioms ✓/✗
```lua
-- ✓ preallocate + index-assign in hot loops
local t = table.create(1000)
for i = 1, 1000 do t[i] = i*i end
-- ✗ table.insert in a tight loop (re-reads #t each call, slower)
-- ✓ localize hot globals/library funcs
local insert, sqrt = table.insert, math.sqrt
-- ✓ reuse one table with table.clear instead of reallocating each frame
```

## Functions

```lua
local function add(a, b) return a + b end     -- prefer local
local f = function() end                       -- anonymous (always local)
```
- Missing args → `nil`; extra args ignored. **Multiple returns**: `return sum, diff`; `local s, d = f()`.
- Multi-returns truncate to 1 unless last in an expression list: `print((f()))` → 1 value; `t = {f(), g()}` keeps all of `g()` only.
- **Methods**: `function T:m(x)` ≡ `function T.m(self, x)`; call `obj:m(x)` passes `self`. Dot call needs explicit self: `T.m(obj, x)`.
- **Varargs** `...`: `local args = {...}` (or `table.pack(...)` to keep `n`). Forward with `f(...)`. `select("#", ...)` counts, `select(i, ...)` slices. `...` isn't a real variable — only pass/return/pack it. Inner functions can't reuse the outer `...`.
- `unpack(t)`/`table.unpack(t)` spreads an array into args.
- Named-arg idiom: single table literal, call without parens: `build{name="Bob", hp=100}`.

```lua
local function variadic(label, ...)
    for i, v in {...} do print(label, i, v) end
end
```

## OOP via metatables

Metatables attach **metamethods** to tables. `setmetatable(t, mt)` (returns `t`); `getmetatable(t)`; `rawget/rawset/rawequal/rawlen` bypass metamethods.

Key metamethods: `__index` (read miss → table to delegate to, or `fn(t,k)`), `__newindex` (write to missing key), `__call`, `__tostring`, `__len`, `__iter`, `__eq __lt __le`, arithmetic `__add __sub __mul __div __idiv __mod __pow __unm __concat`, `__metatable` (lock), `__mode` (weak keys/values `"k"`/`"v"`/`"kv"`).

### Idiomatic class pattern
```lua
local Animal = {}
Animal.__index = Animal           -- instances delegate field/method lookup here

function Animal.new(name, sound)
    local self = setmetatable({}, Animal)
    self.name = name
    self.sound = sound
    return self
end

function Animal:speak()
    print(`{self.name} says {self.sound}`)
end

local dog = Animal.new("Rex", "Woof")
dog:speak()
```

### Inheritance (chain `__index`)
```lua
local Dog = setmetatable({}, {__index = Animal})
Dog.__index = Dog
function Dog.new(name)
    local self = Animal.new(name, "Woof")
    return setmetatable(self, Dog)
end
function Dog:fetch() print(`{self.name} fetches`) end
```

Notes:
- `__index`/`__newindex` only fire when the key is **absent**. To populate from inside `__index` while `__newindex` blocks normal writes, use `rawset(self, k, v)` to avoid infinite recursion / stack overflow.
- Relational: implement `__lt` (drives `< > <= >=`); add `__le` only for special unordered semantics (e.g. NaN). `__eq` requires both operands share the metamethod.
- Arithmetic metamethods are commutative-ambiguous: either operand may be the table — branch on `type(a)`/`type(b)` (e.g. scalar*vector).
- **Set** = dict with `value → true`; membership `set[x] == true`, no order, no dupes.

## Type system (`--!strict`)

Modes (first line): `--!nocheck`, `--!nonstrict` (default-ish; only annotated vars checked), `--!strict` (infer + check everything). Use `--!strict` for new code. Mismatches are editor warnings only — never runtime errors.

```lua
--!strict
local x: number = 5
local name: string? = nil          -- optional: string | nil
local parts: {Instance} = {}        -- array type
local scores: {[string]: number} = {}  -- map type

type Vector2 = { x: number, y: number }      -- alias
type Handler = (msg: string) -> ()           -- function type
type Result = (string, number)               -- N/A as var; use in fn return
local function find(s: string): (string, number) return s, #s end

-- generics
type List<T> = {T}
type Map<K, V> = {[K]: V}
local function id<T>(v: T): T return v end

-- unions & intersections
type Shape = "circle" | "square"             -- literal union
type AB = {a: number} & {b: number}

-- casts (analysis only): value :: Type   (everything casts to `any`)
local n = (val :: any) :: number

-- typeof for inferred / metatable types
type Animal = typeof(setmetatable({} :: {name: string}, {} :: {__index: any}))
```
- Variadic type: `type F = (...number) -> number` (NOT `(...: number)`).
- Export types from ModuleScripts: `export type Cat = {...}` then `Types.Cat` after `require`. Annotate function params/returns for clarity and to help `--!native`.

## Coroutines & the task library

### task (use this for scheduling/yielding — ✓ over legacy globals)
```
task.spawn(fnOrThread, ...) -> thread   -- resume IMMEDIATELY (synchronously)
task.defer(fnOrThread, ...) -> thread   -- resume at end of current resumption cycle
task.delay(sec, fnOrThread, ...) -> thread  -- resume after sec, no throttle
task.wait(sec?) -> elapsed              -- yield ~sec (default 0 = next Heartbeat)
task.cancel(thread)                     -- cancel a scheduled thread
task.synchronize() / task.desynchronize()   -- Parallel Luau (inside Actor only)
```
- ✓ **`task.wait` not `wait`**: `wait()` is deprecated, throttles (clamps to ~30Hz, can over-delay), returns extra junk. `task.wait` guarantees resume on the first eligible Heartbeat and returns only elapsed time. Same for `task.spawn`/`task.delay` over deprecated `spawn`/`delay`/`spawn(fn)` which throttle.
- ✗ Never an infinite loop without a yield (`task.wait`) — freezes/crashes the VM.
- `task.spawn(fn)` runs `fn` now and continues your code after `fn` yields/returns; great for fire-and-forget. `task.defer` for "run after current frame work."

### coroutine (lower level)
```
coroutine.create(fn) -> thread
coroutine.resume(co, ...) -> ok, results...   -- starts/continues; ok=false on error
coroutine.yield(...) -> args-from-next-resume
coroutine.wrap(fn) -> function    -- auto-resume wrapper (errors propagate)
coroutine.status(co) -> "suspended"|"running"|"normal"|"dead"
coroutine.running() ; coroutine.isyieldable() ; coroutine.close(co)
```
Prefer `task.*` for engine-scheduled work; `coroutine` for hand-rolled generators/state machines. `pcall(fn, ...)` → `ok, err` is the try/catch idiom; `error(msg, level)` raises; `xpcall(fn, handler)` for custom handling.

## buffer (low-level binary, little-endian)

Fixed-size mutable byte block; replaces `string.pack`. Offsets are **0-based** bytes; out-of-range errors. Max 1 GiB. NOT shareable across Actors; copied (identity lost) through Roblox events.
```
buffer.create(size) -> buffer            -- zero-filled
buffer.fromstring(s) / buffer.tostring(b)
buffer.len(b)
buffer.readi8/u8/i16/u16/i32/u32/f32/f64(b, offset) -> number
buffer.writei8/u8/i16/u16/i32/u32/f32/f64(b, offset, value)
buffer.readbits(b, bitOffset, bitCount) / buffer.writebits(b, bitOffset, bitCount, value)  -- 0..32 bits
buffer.readstring(b, offset, count) / buffer.writestring(b, offset, s, count?)
buffer.copy(target, tOff, source, sOff?, count?)
buffer.fill(b, offset, value, count?)
```
Use for compact networking payloads, serialization, tight numeric storage; pairs well with `--!native`.

## vector (native 3-component float)

Distinct from `Vector3`; SIMD-backed primitive with operator overloads. Components `v.x/v.X` etc. **Immutable**.
```
vector.create(x, y, z) -> vector ; vector.zero ; vector.one
vector.magnitude(v) ; vector.normalize(v) ; vector.dot(a,b) ; vector.cross(a,b)
vector.angle(a, b, axis?) -> radians
vector.floor/ceil/abs/sign(v) ; vector.clamp(v, min, max) ; vector.lerp(a, b, alpha)
vector.max(...) ; vector.min(...)
```

## math / bit32 / os / utf8 / debug (selected)

```
math.floor/ceil/round(x) ; math.modf(x) -> int, frac ; math.abs/sign
math.clamp(x, lo, hi) ; math.min/max(...) ; math.lerp(a, b, t) ; math.map(x, i0,i1, o0,o1)
math.sqrt/exp/log(x, base?)/pow ; math.random(m?, n?) ; math.randomseed(x)
math.noise(x, y?, z?) -- Perlin ; math.huge ; math.pi ; math.isnan/isfinite
-- integer test: math.floor(x) == x
bit32.band/bor/bxor/bnot/btest ; bit32.lshift/rshift/arshift/lrotate/rrotate(x, disp)
bit32.extract(n, field, width) ; bit32.replace(n, v, field, width) ; bit32.countlz/countrz
os.time(t?) -> unix ; os.clock() -> high-res seconds (use for timing/deltas) ; os.date(fmt?, t?)
utf8.char(...) ; utf8.codepoint(s, i?, j?) ; utf8.len(s) ; utf8.offset ; utf8.charpattern
for _, cp in utf8.codes(s) do ... end   -- iterate codepoints, not bytes
debug.traceback(msg?, lvl?) ; debug.profilebegin(label)/profileend()
debug.setmemorycategory(tag) ; debug.dumpcodesize()  -- native size audit
```
✓ Use `os.clock()` (monotonic, sub-ms) for benchmarking, not `os.time()` (whole seconds).

## Native code generation (`--!native`)

First line `--!native` compiles the script's functions to machine code; or per-function `@native`. Behavior identical, only faster — best for heavy numeric loops over numbers/`buffer`/`vector` called many times (e.g. every frame). Server-side.

```lua
--!native
local function sumComponents(v: Vector3)   -- ANNOTATE: specialized vector path
    return v.X + v.Y + v.Z                 -- untyped v → assumed table → slower checks
end
```
- Top-level scope (runs once) benefits little; functions do. Measure with Script Profiler (`<native>` tag).
- ✗ De-opts / falls back: `getfenv`/`setfenv`, mistyped args to typed funcs, some builtins with non-numeric args.
- Costs: longer server startup, extra memory, a total native-code size cap. Don't blanket-apply; use `@native` selectively. Breakpoints disable native execution for that function.

## Luau vs vanilla Lua vs C#

- **vs Lua**: `+=`/compound ops, `//` floor div, string interpolation, `continue`, generalized `for x in t`, type annotations, `table.create/clone/move/freeze`, `string.split`, `task`/`buffer`/`vector` libs, `0b` binaries, underscores in literals. No `goto`. `setfenv`/`getfenv` deprecated. `unpack` global still works (also `table.unpack`).
- **vs C#**: 1-based indexing (C# 0-based); `nil` not `null`; `~=` not `!=`; `and/or/not` not `&&/||/!`; `^` exponent not XOR; `..` concat not `+`; no classes (use metatables); no `try/catch` (use `pcall`); no `new` (use `.new` convention); dynamic typing; multiple return values are native; `--` comments, `--[[ ]]` blocks; no semicolons needed; everything-but-`false`/`nil` is truthy; `local` instead of access modifiers (`_name` = "private" by convention).
- Naming: `PascalCase` for classes/enums/Roblox APIs; `camelCase` for locals/functions; `LOUD_SNAKE_CASE` for constants. Avoid `_ALLCAPS` (reserved).

## Sharp-edge checklist ✓/✗

- ✗ `0`/`""` are NOT falsy. ✓ test `x == nil` explicitly when `false`/falsy values are valid.
- ✗ `nil` holes in arrays break `#` and `ipairs`. ✓ use `table.remove`, never `a[i]=nil` mid-array.
- ✗ `a[0]` — arrays start at `1`.
- ✗ table `==` is identity, not value equality. ✓ compare fields or add `__eq`.
- ✗ globals in hot loops. ✓ `local` everything; localize library functions.
- ✗ `table.insert` per element when count known. ✓ `table.create` + index assign.
- ✗ `wait()`/`spawn()`/`delay()` (throttled, deprecated). ✓ `task.wait`/`task.spawn`/`task.delay`.
- ✗ infinite loop without `task.wait` → crash.
- ✓ buffer/vector offsets are 0-based even though Lua tables are 1-based.
- ✓ annotate types (esp. `Vector3`/numbers) under `--!native` and `--!strict`.
