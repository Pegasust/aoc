// Usable by Windows and UNIX
const LINE_SPLIT = (/\r?\n/);

async function main(fileLoc: string) {
	const input = await Deno.readTextFile(fileLoc);
	const ord = (s: string) => s.charCodeAt(0);
	const prioritized = input.split(LINE_SPLIT).map((line) => line.trim())
		.filter((line) => line.length != 0)
		.map((line) =>
			[...line].map((e) => e.charCodeAt(0))
				.map((e) =>
					e - ((ord('a') <= e && e <= ord('z'))
						? (ord('a') - 1)
						: (ord('A') - 27))
				)
		);
	const retain = <T>(a: T[], b: T[]) => {
		const bSet = new Set(b);
		return a.filter((e) => bSet.has(e));
	};
	const halves = <T>(a: T[]) =>
		[a.slice(0, a.length / 2), a.slice(a.length / 2, a.length)] as const;
	console.log(
		'part 1',
		prioritized
			.map((sack) => retain(...halves(sack))[0]).reduce((a, b) => a + b),
	);
	const arrayGroupBy = <T, F>(a: T[], groupFn: (elem: T, idx: number) => F) =>
		a.reduce((ret, e, idx) => {
			const identity = groupFn(e, idx);
			if (!ret.groupMap.has(identity)) {
				ret.groupMap.set(identity, ret.groupKeys.length);
				ret.groupKeys.push(identity);
				ret.groups.push([identity, []]);
			}
			ret.groups[ret.groupMap.get(identity)!][1].push(e);
			return ret;
		}, {
			groupKeys: new Array<F>(),
			groupMap: new Map<F, number>(),
			groups: new Array<[F, T[]]>(),
		}).groups;

	console.log(
		'part 2',
		arrayGroupBy(prioritized, (_, idx) => Math.floor(idx / 3))
			.map(([_idx, sacks]) => sacks)
			.map((groupOf3) => groupOf3.reduce((a, b) => retain(a, b))[0])
			.reduce((a, b) => a + b),
	);
}

if (Deno.args.length < 1) {
	throw Error(
		'd3_deno.ts expects a single argument that points to AOC\'s day 3 input file',
	);
}

const fileLoc = Deno.args[0];
await main(fileLoc);
