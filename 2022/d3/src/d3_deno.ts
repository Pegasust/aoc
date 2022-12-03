if(Deno.args.length < 1) {
    throw Error("d3_deno.ts expects a single argument that points to AOC's day 3 input file");
}
const fileLoc = Deno.args[0];
const text = await Deno.readTextFile(fileLoc);

