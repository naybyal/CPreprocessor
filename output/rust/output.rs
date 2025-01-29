fn add(a: i32, b: i32) -> i32 {
    a + b
}

fn subtract(a: i32, b: i32) -> Result<i32, InvalidInput> {
    Ok(a - b)
}

fn multiply(a: i32, b: i32) -> i32 {
    a * b
}

fn divide(a: i32, b: i32) -> Result<f32, String> {
    if b == 0 {
        return Err(String::from("Error: Division by zero!"));
    }
    Ok((a as f32) / (b as f32))
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    let mut x = String::new();
    let mut y = String::new();
    let mut choice = String::new();
    println!("Enter two numbers: ");
    std::io::stdin().read_line(&mut x)?;
    std::io::stdin().read_line(&mut y)?;
    println!("Choose operation:\n1 - Add\n2 - Subtract\n3 - Multiply\n4 - Divide\n");
    std::io::stdin().read_line(&mut choice)?;
    let x: i32 = x.trim().parse()?;
    let y: i32 = y.trim().parse()?;
    let choice: usize = choice.trim().parse()?;
    let result: i32;
    let result_f: f32;
    match choice {
        1 => {
            result = add(x, y);
            println!("Result: {}", result);
        }
        2 => {
            result = subtract(x, y);
            println!("Result: {}", result);
        }
        3 => {
            result = multiply(x, y);
            println!("Result: {}", result);
        }
        4 => {
            if y == 0 {
                return Err("Division by zero is not allowed!".into());
            }
            result_f = (x as f32) / (y as f32);
            println!("Result: {:.2}", result_f);
        }
        _ => println!("Invalid choice!"),
    }
    println!("Looping through numbers 1 to 5:\n");
    for i in 1..=5 {
        print!("{} ", i);
    }
    println!();
    Ok(())
}
fn add(x: i32, y: i32) -> i32 {
    x + y
}
fn subtract(x: i32, y: i32) -> i32 {
    x - y
}
fn multiply(x: i32, y: i32) -> i32 {
    x * y
}
fn divide(x: i32, y: i32) -> f32 {
    (x as f32) / (y as f32)
}

