fn call_me() {
    println!("sorted!");
}

fn add(a: i32, b: i32) -> i32 {
    a + b
}

fn main() -> Result<(), Box<dyn Error>> {
    call_me()?;
    println!("Hello, Nabiel! {}", 3.14);
    Ok(())
}

