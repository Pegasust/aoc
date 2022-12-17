fn main() {
    // let test = include_str!("../data/example.txt");
    let sub = inlcude_str!("../data/submission.txt");
    let commands = sub.lines()
        .map(|line| line.split(" "))
}
