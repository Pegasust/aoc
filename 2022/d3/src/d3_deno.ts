if(Deno.args.length < 1) {
    throw Error("d3_deno.ts expects a single argument that points to AOC's day 3 input file");
}
const fileLoc = Deno.args[0];
const text = await Deno.readTextFile(fileLoc);

// Usable by Windows and UNIX
const LINE_SPLIT = (/\r?\n/);

function priority(chr: string) {
    if(chr.length != 1) {
        throw Error("Expecting character");
    }

    const ord = (v: string) => v.charCodeAt(0);
    return (ord('a') <= ord(chr) && ord(chr) <= ord('z'))? (ord(chr) - ord('a') + 1):
        (ord(chr) - ord('A') + 1);
}

const sumPrioOfShared = text.split(LINE_SPLIT) // split by each line, basically iterates through each rucksack
    .map(s=>[...s].map(priority)) // translate each character into respective priority
    .map((v)=> [v.slice(0, v.length/2), v.slice(v.length/2, v.length) ]) // splits by 2 compartments
    .map(([left, right])=> {
        // Finds the value on the right compartment that also exists in left compartment
        const left_set = new Set(left);
        // by the prompt, we're pretty guaranteed to have a solution
        const shared =  right.find(e => left_set.has(e))!;
        console.log("shared:", shared);
        return shared;
    }).reduce((a,b)=>a+b); // find its sum

console.log(sumPrioOfShared);
