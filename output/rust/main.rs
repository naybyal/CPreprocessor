fn main() -> Result<(), Box<dyn Error>> {
    call_me()?;
    println!("Hello, Nabiel! {}", 3.14);
    Ok(())
}