// Usable by Windows and UNIX
const LINE_SPLIT = (/\r?\n/);

function priority(chr: string) {
	if (chr.length != 1) {
		throw Error('Expecting character');
	}

	const ord = (v: string) => v.charCodeAt(0);
	return (ord('a') <= ord(chr) && ord(chr) <= ord('z'))
		? (ord(chr) - ord('a') + 1)
		: (ord(chr) - ord('A') + 27);
}

if (Deno.args.length < 1) {
	throw Error(
		'd3_deno.ts expects a single argument that points to AOC\'s day 3 input file',
	);
}

async function main(fileLoc: string) {
	// part 1
	const text = await Deno.readTextFile(fileLoc);
	const prioritized = text.split(LINE_SPLIT) // split by each line, basically iterates through each rucksack
		.map((line) => line.trim()).filter((line) => line.length != 0) // pre-proc: remove "falsy lines"
		.map((s) => [...s].map(priority)) // translate each character into respective priority
	;
	const sumPrioOfShared = prioritized
		.map((v) => [v.slice(0, v.length / 2), v.slice(v.length / 2, v.length)]) // splits by 2 compartments
		.map(([left, right]) => {
			// Finds the value on the right compartment that also exists in left compartment
			const left_set = new Set(left);
			// by the prompt, we're pretty guaranteed to have a solution
			const shared = right.find((e) => left_set.has(e))!;
			// console.log('shared:', shared);
			return shared;
		}).reduce((a, b) => a + b); // find its sum

	console.log('part 1:', sumPrioOfShared);

	// part 2
	// eventually was not used. part 2
	const setDiff = <T>(a: Set<T>, b: Set<T>) =>
		new Set([...a].filter((e) => !b.has(e)));
	const setRetain = <T>(a: Set<T>, b: Set<T>) =>
		new Set([...a].filter(e => b.has(e)))

	const groupBy = <T, K>(arr: T[], groupFn: (e: T, idx: number) => K) => {
		return arr.reduce<Map<K, T[]>>((ret, e, idx) => {
			const groupId = groupFn(e, idx);
			const last = ret.get(groupId) ?? [];
			last.push(e);
			ret.set(groupId, last);
			return ret;
		}, new Map());
	};
	const toGroupPair = <K, V>(groupMap: Map<K, V[]>) =>
		Array.from(groupMap.entries());

	const groupByThree = (_: unknown, idx: number) => Math.floor(idx / 3);
	
	const threeGrouped = groupBy(prioritized, groupByThree)
	// console.log("threeGrouped", threeGrouped);
	const badges = toGroupPair(threeGrouped)
		.map(([_, group]) => group)
		.map((group) =>
			group.map((bag) => new Set(bag))
				.reduce((left, right) => setRetain(left, right))
		).map((e) => [...e][0]); // get the only element in the set for each group

	console.log('part 2:', badges.reduce((a,b)=>a+b));
}

const fileLoc = Deno.args[0];
await main(fileLoc);

