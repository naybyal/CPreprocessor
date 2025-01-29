fn divide(a: i32, b: i32) -> Result<f32, String> {
    if b == 0 {
        return Err(String::from("Error: Division by zero!"));
    }
    Ok((a as f32) / (b as f32))
}