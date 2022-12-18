use core::result;
use std::collections::VecDeque;
use std::iter::Iterator;
use std::num::Wrapping;
use std::ops::{Add, Div, Mul, Sub};

use itertools::Itertools;

fn ex_case() -> &'static str {
    include_str!("../data/example.txt")
}
fn sub_case() -> &'static str {
    include_str!("../data/submission.txt")
}

fn process_input(input_str: &str) -> Result<Vec<Monkey>> {
    Ok(collect_errs(parse_universe(input_str))
        .map_err(|e| e.collect_vec().join("\n"))?
        .collect_vec())
}

fn main() -> Result<()> {
    // let test = include_str!("../data/example.txt");
    let sub = sub_case();
    let universe = process_input(sub)?;

    println!("part1: {}", part1(universe.iter()));
    part2(universe.iter());
    Ok(())
}

/// If there exists an [`Err`] in [`results`], this function filters out so that
/// it only returns Err values. Otherwise, returns [`Ok`]
fn collect_errs<T, E, ResultIter: Iterator<Item = core::result::Result<T, E>>>(
    results: ResultIter,
) -> result::Result<impl Iterator<Item = T>, impl Iterator<Item = E>> {
    let v = results.collect_vec();
    let has_err = v.iter().any(|res| res.is_err());
    if has_err {
        Err(v.into_iter().filter_map(|e| e.err()))
    } else {
        Ok(v.into_iter().filter_map(|e| e.ok()))
    }
}

/// Allows for lazy results
trait CanResult {
    type T;
    type E;
    fn result(self) -> result::Result<Self::T, Self::E>;
}

impl <T, E> CanResult for core::result::Result<T, E> {
    type T = T;
    type E = E;
    fn result(self) -> result::Result<Self::T, Self::E> {self}
}

trait CollectErrs {
    type T;
    type E;
    type IterT: Iterator<Item=Self::T>;
    type IterE: Iterator<Item=Self::E>;
    type R: CanResult<T=Self::IterT, E=Self::IterE>;
    fn collect_errs(self) -> Self::R;
}

struct CollectErrsResult<T, E, ResIter: Iterator<Item=core::result::Result<T,E>>> {
    input: ResIter
}


impl <T, E, ResIter: Iterator<Item=core::result::Result<T,E>>> CanResult for CollectErrsResult<T, E, ResIter> {
    fn result(self) -> result::Result<Self::T, Self::E> {
        let v = self.input.collect_vec();
        let has_err = v.iter().any(|res| res.is_err());
        if has_err {
            Err(v.into_iter().filter_map(|e| e.err()))
        } else {
            Ok(v.into_iter().filter_map(|e| e.ok()))
        }
    }
}
impl<T, E, ResIter: Iterator<Item=core::result::Result<T,E>>>
    CollectErrs for ResIter 
{
    type T = T;
    type E = E;
    type IterT;
    type IterE;

    fn collect_errs(self) -> result::Result<Self::IterT, Self::IterE> {
        todo!()
    }
}


// <T, E, ResultIter: Iterator<Item=core::result::Result<T, E>>>
fn part1<'a>(universe: impl Iterator<Item = &'a Monkey>) -> u32 {
    todo!();
}
fn part2<'a>(universe: impl Iterator<Item = &'a Monkey>) {
    todo!();
}

type MyErr = String;
type Result<T> = core::result::Result<T, MyErr>;

type Int = Wrapping<u32>;

trait TypeContainer<T> {
    type ContainedType; // AssociatedType default is unstable
}

impl<T> TypeContainer<T> for Wrapping<T> {
    type ContainedType = T;
}

trait MonadFrom<T>: TypeContainer<T> {
    fn monad_ctor(t: T) -> Self;
}

// impl <T, Contained> MonadFrom<Contained> for T where T: TypeContainer<Contained> {
//     fn monad_ctor(t: Contained) -> Self {
//         Self(t) // The Self constructor can only be used with tuple or unit structs
//     }
// }

impl<T> MonadFrom<T> for Wrapping<T> {
    fn monad_ctor(t: T) -> Self {
        Self(t)
    }
}

#[derive(Clone, Debug)]
enum MonkeyOperator {
    Const(Int),
    Id,
    ConstOp {
        my_const: Int,
        op: fn(Int, Int) -> Int,
    },
    SelfOp(fn(Int, Int) -> Int),
}
impl MonkeyOperator {
    fn apply(&self, old: Int) -> Int {
        match &self {
            Self::Const(e) => *e,
            Self::Id => old,
            Self::ConstOp { my_const, op } => op(*my_const, old),
            Self::SelfOp(op) => op(old, old),
        }
    }
}
/// Parses the expression `"new"{ }"="{ }<rval_tok>[{ }<op>{ }<rval_tok>]`
fn parse_monkey_op(input: &str) -> Result<MonkeyOperator> {
    // should be in the following format: old <op> <rval>
    fn _op_parse(op: &str) -> Result<fn(Int, Int) -> Int> {
        match op {
            "*" => Ok(Int::mul),
            "/" => Ok(Int::div),
            "+" => Ok(Int::add),
            "-" => Ok(Int::sub),
            e => Err(format!("idk wtf is the case with {e}")),
        }
    }
    fn _parse(v: Vec<&str>) -> Result<MonkeyOperator> {
        match &v[..2] {
            ["new", "="] => Ok(()),
            _ => Err(format!(
                "monkey operation expr should start with \"new = \""
            )),
        }?;
        match &v[2..] {
            ["old"] => Ok(MonkeyOperator::Id),
            // I want Int::ContainedType so bad :(
            [e] => e
                .parse::<<Int as TypeContainer<_>>::ContainedType>()
                .map(|e| MonkeyOperator::Const(Int::monad_ctor(e)))
                .map_err(|e| e.to_string()),
            e => Err(format!("idk wtf is the case with {:?}", e)),
        }
    }
    _parse(input.split_whitespace().collect_vec())
}

#[derive(Clone, Debug)]
struct Monkey {
    monkey_id: u8,
    worry_q: VecDeque<u32>,
    operation: MonkeyOperator,
    worry_divcheck: u32,
    dest_div: usize,     // if divisble by worry_divcheck, which monkey to throw to?
    dest_not_div: usize, // if not divisible, which monkey to throw to?
}

/// Turns the monkey's input as specified in ../data/example.txt
/// into Monkey
fn parse_monkey(monkey_input: &str) -> Result<Monkey> {
    let mut spl = monkey_input.lines();
    // "Monkey 0"
    let monkey_id = spl
        .next()
        .and_then(|id_str| id_str.split(' ').last())
        // "0:" \in possible(id)
        .map(|id| id.chars().take(id.len() - 1))
        .ok_or_else(|| "Failed to parse monkey id input".to_string())
        // "0"
        .and_then(|id| {
            id.collect::<String>()
                .parse::<u8>()
                .map_err(|e| e.to_string())
        })?;
    // |  Starting items: [item{, item}]
    let worry_q = spl
        .next()
        .and_then(|id_str| id_str.split(": ").last())
        .map(|s| s.split(", "))
        .ok_or_else(|| "Failed to parse worry_q".to_string())?;
        .and_then(|int_spl| int_spl.map(|int_s| int_s.parse::<u32>()))
        .map(|worries| worries.collect::<VecDeque<_>>())
    let operation = spl
        .next()
        .and_then(|op_line| op_line.split(": ").last())
        .ok_or_else(|| "Failed to parse monkey operation".to_string())
        .and_then(|op_str| parse_monkey_op(op_str))?;
    let worry_divcheck = spl
        .next()
        .and_then(|div_test_ln| div_test_ln.split_whitespace().last())
        .ok_or_else(|| "Failed to parse divisible test value".to_string())
        .and_then(|div_str| div_str.parse::<u32>().map_err(|e| e.to_string()))?;
    let mut parse_monkey_idx_div = || {
        spl.next()
            .and_then(|ln| ln.split_whitespace().last())
            .ok_or_else(|| "Failed to parse which monkey index to throw if divisible".to_string())
            .and_then(|div_str| div_str.parse::<usize>().map_err(|e| e.to_string()))
    };
    let dest_div = parse_monkey_idx_div()?;
    let dest_no_div = parse_monkey_idx_div()?;
    Monkey {
        monkey_id,
        worry_q,
        operation,
        worry_divcheck,
        dest_div,
        dest_no_div,
    }
}

fn parse_universe<'a>(input: &'a str) -> impl Iterator<Item = Result<Monkey>> + 'a + Clone {
    input.split("\n\n").map(parse_monkey)
}

#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn part1_example() {
        assert_eq!(part1((process_input(ex_case())).unwrap()));
    }
    #[test]
    fn part2_example() {}

    #[rstest::rstest]
    #[case(0)]
    #[case(1)]
    #[case(2)]
    #[case(3)]
    #[case(414)]
    fn parse_monkeyop_id(#[case] input: u32) {
        let id = parse_monkey_op("new = old").unwrap();
        assert_eq!(id.apply(Int::monad_ctor(input)), Int::monad_ctor(input));
    }
    #[rstest::rstest]
    #[case(0, 14)]
    #[case(0, 1)]
    #[case(0, 7)]
    #[case(7, 14)]
    #[case(7, 69)]
    fn parse_monkey_op_const(#[case] my_const: u32, #[case] ignored_old_val: u32) {
        let const_ret = parse_monkey_op(format!("new = {my_const}").as_str()).unwrap();
        assert_eq!(
            const_ret.apply(Int::monad_ctor(ignored_old_val)),
            Int::monad_ctor(my_const)
        );
    }

    // #[test]
    // fn panic() {
    //     panic!("lol")
    // }
}
