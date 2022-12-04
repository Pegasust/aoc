-- What we've learn:
-- - [x] Open a file as read (same signature as python's open(<file>[, mode]))
-- - [x] Read file line-by-line
-- - [x] Lua's iterator can be a generator function
-- - [x] string -> number with tonumber()
-- - [x] Syntactic sugar on collection length (or any that implements :len()): #<var>
-- - [x] `print(..args)`; printing a nil yields an empty space. print also formats as a fancy table
--             ```
--             > print(1,2,3,4)
--             1       2       3       4
--             > print(100, 200, 300, 400)
--             100     200     300     400
--             ```
-- - [x] CLI arguments are globally `arg`. arg[0] is the location of script, arg[1] is the first cli arg
-- - [x] There is no loop-`continue` in Lua

local function main(file_loc)
    counter = 0
    for group in io.lines(file_loc) do
        if #group > 0 then -- a better way is to strip the string first, idk how to do this, though
            -- despite the fact that we establish the token consists of digits
            -- Lua parses the token as "string" type.
            time_matches = group:gmatch("%d+") 
            l_begin = tonumber(time_matches())
            l_end = tonumber(time_matches())
            r_begin = tonumber(time_matches())
            r_end = tonumber(time_matches())
            -- check if one elf's time is contained within the other
            -- 4       9       10      97
            if (l_begin <= r_begin and r_end <= l_end) or 
                (r_begin <= l_begin and l_end <= r_end) then
                counter = counter + 1
            end
        end
    end
    print("part 1 " .. counter) -- print("part 1", counter) works as well. Guess it's var-args


    counter = 0
    for group in io.lines(file_loc) do
        if #group > 0 then -- a better way is to strip the string first, idk how to do this, though
            time_matches = group:gmatch("%d+")
            l_begin = tonumber(time_matches())
            l_end = tonumber(time_matches())
            r_begin = tonumber(time_matches())
            r_end = tonumber(time_matches())

            -- check if one elf's time is contained within the other
            if (l_begin >= r_begin and l_begin <= r_end) or -- l_begin within r's range
               (r_begin >= l_begin and r_begin <= l_end) or -- r_begin within l's range
               (l_end >= r_begin and l_end <= r_end) or -- l_end within r's range
               (r_end >= l_begin and r_end <= l_end) -- r_end within l's range
            then
                counter = counter + 1
            end
        end
    end
    print("part 2 " .. counter)
end

main(arg[1])

